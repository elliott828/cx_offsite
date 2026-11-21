import { readFile, access } from 'node:fs/promises';
import { join } from 'node:path';

const root = new URL('.', import.meta.url).pathname.slice(1).replaceAll('/', '\\');
const html = await readFile(join(root, 'index.html'), 'utf8');
const refs = [...new Set([...html.matchAll(/(?:src|image:)=["']?([^"' }]+)|image:'([^']+)'/g)].map(m => m[1] || m[2]).filter(v => v?.startsWith('assets/') && !v.includes('${')))];
const missing = [];
for (const ref of refs) {
  try { await access(join(root, ref.replaceAll('/', '\\'))); } catch { missing.push(ref); }
}
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
for (const [, code] of scripts) new Function(code);
const required = ['The Age of Discovery','Open Map','House Challenge','Dinner + Team Awards Announcement','House of the','Emerald · Teal · Gold','Winning Team'];
const absent = required.filter(text => !html.includes(text));
if (missing.length || absent.length) {
  console.error({ missing, absent });
  process.exit(1);
}
console.log(`Validated ${refs.length} local assets, ${scripts.length} inline script, and ${required.length} required content checks.`);
