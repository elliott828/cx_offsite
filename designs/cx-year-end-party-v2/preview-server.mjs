import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';

const root = new URL('.', import.meta.url).pathname.slice(1).replaceAll('/', '\\');
const types = {'.html':'text/html; charset=utf-8','.png':'image/png','.webp':'image/webp','.json':'application/json','.jpg':'image/jpeg','.jpeg':'image/jpeg','.css':'text/css','.js':'text/javascript'};

http.createServer(async (req,res)=>{
  try {
    const clean = decodeURIComponent((req.url || '/').split('?')[0]);
    const relative = clean === '/' ? 'index.html' : clean.replace(/^\/+/, '');
    const file = normalize(join(root, relative));
    if (!file.startsWith(root)) throw new Error('Invalid path');
    const data = await readFile(file);
    res.writeHead(200, {'Content-Type': types[extname(file).toLowerCase()] || 'application/octet-stream','Cache-Control':'no-store'});
    res.end(data);
  } catch { res.writeHead(404); res.end('Not found'); }
}).listen(4173,'127.0.0.1',()=>console.log('Preview: http://127.0.0.1:4173'));
