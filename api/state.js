import { BlobPreconditionFailedError, get, put } from '@vercel/blob';

const STATE_PATH = 'cx-offsite/live-state.json';
const ORGANIZERS = new Set(['Organizer 1', 'Organizer 2', 'Organizer 3']);
const WRITABLE_ROOTS = new Set([
  'teams', 'bowling', 'specialNames', 'specialScores', 'multipliers',
  'manualMultiplier', 'cookingFixed', 'cookingSpecial', 'revealedPrizes',
]);

const DEFAULT_STATE = {
  teams: [1, 2, 3, 4].map((number) => ({
    name: `Team 0${number}`,
    members: [1, 2, 3, 4, 5, 6].map((member) => `Member 0${member}`),
  })),
  bowling: [0, 0, 0, 0],
  specialNames: ['Wildcard 01', 'Wildcard 02', 'Wildcard 03', 'Wildcard 04'],
  specialScores: [0, 0, 0, 0],
  multipliers: [1.5, 1.2, 1.1, 1.0],
  manualMultiplier: [false, false, false, false],
  cookingFixed: [0, 0, 0, 0],
  cookingSpecial: [0, 0, 0, 0],
  revealedPrizes: [],
  updatedAt: null,
  updatedBy: null,
};

function json(response, data, status = 200) {
  response.statusCode = status;
  response.setHeader('Content-Type', 'application/json; charset=utf-8');
  response.setHeader('Cache-Control', 'no-store, max-age=0');
  response.end(JSON.stringify(data));
}

function cloneDefault() {
  return JSON.parse(JSON.stringify(DEFAULT_STATE));
}

async function readState() {
  const result = await get(STATE_PATH, { access: 'private' });
  if (!result || result.statusCode !== 200) return { state: cloneDefault(), etag: null };
  const state = await new Response(result.stream).json();
  return { state: { ...cloneDefault(), ...state }, etag: result.blob.etag };
}

function isAuthorized(request) {
  const name = request.headers['x-organizer-name'] || '';
  const code = request.headers['x-organizer-code'] || '';
  return ORGANIZERS.has(name) && code.length > 0 && code === process.env.ORGANIZER_CODE;
}

async function readBody(request) {
  if (request.body && typeof request.body === 'object') return request.body;
  let raw = '';
  for await (const chunk of request) raw += chunk;
  return JSON.parse(raw);
}

function setPath(target, path, value) {
  const parts = String(path).split('.');
  if (!parts.length || !WRITABLE_ROOTS.has(parts[0]) || parts.length > 4) {
    throw new Error('Unsupported state path');
  }
  let cursor = target;
  for (let index = 0; index < parts.length - 1; index += 1) {
    const key = /^\d+$/.test(parts[index]) ? Number(parts[index]) : parts[index];
    if (cursor[key] == null || typeof cursor[key] !== 'object') throw new Error('Invalid state path');
    cursor = cursor[key];
  }
  const finalKey = /^\d+$/.test(parts.at(-1)) ? Number(parts.at(-1)) : parts.at(-1);
  cursor[finalKey] = value;
}

export default async function handler(request, response) {
  if (request.method === 'GET') {
    try {
      const { state } = await readState();
      return json(response, { state });
    } catch (error) {
      return json(response, { error: 'Shared scorecard is temporarily unavailable.' }, 503);
    }
  }

  if (request.method !== 'POST') return json(response, { error: 'Method not allowed' }, 405);
  if (!isAuthorized(request)) return json(response, { error: 'Organizer access denied.' }, 401);

  let body;
  try {
    body = await readBody(request);
  } catch {
    return json(response, { error: 'Invalid request body.' }, 400);
  }
  if (body.action === 'auth') return json(response, { ok: true });
  if (typeof body.path !== 'string' || JSON.stringify(body.value).length > 20000) {
    return json(response, { error: 'Invalid update.' }, 400);
  }

  for (let attempt = 0; attempt < 6; attempt += 1) {
    try {
      const { state, etag } = await readState();
      setPath(state, body.path, body.value);
      if (/^multipliers\.\d+$/.test(body.path)) {
        state.manualMultiplier[Number(body.path.split('.')[1])] = true;
      }
      state.updatedAt = new Date().toISOString();
      state.updatedBy = request.headers['x-organizer-name'];
      const options = {
        access: 'private',
        allowOverwrite: true,
        contentType: 'application/json',
        cacheControlMaxAge: 0,
      };
      if (etag) options.ifMatch = etag;
      await put(STATE_PATH, JSON.stringify(state), options);
      return json(response, { ok: true, state });
    } catch (error) {
      if (error instanceof BlobPreconditionFailedError && attempt < 5) continue;
      if (error?.message === 'Unsupported state path' || error?.message === 'Invalid state path') {
        return json(response, { error: error.message }, 400);
      }
      return json(response, { error: 'The update could not be saved. Please try again.' }, 503);
    }
  }
  return json(response, { error: 'The scorecard changed at the same time. Please try again.' }, 409);
}
