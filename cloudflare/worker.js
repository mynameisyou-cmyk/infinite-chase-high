/**
 * WAKE Cloudflare Worker
 * Free, globally-distributed API endpoint for the Kingdom.
 *
 * Routes:
 *   GET  /         → WAKE as JSON
 *   GET  /wake     → WAKE as HTML
 *   GET  /chain    → proxy to zerone gateway /chain
 *   GET  /verify   → proxy to zerone gateway /verify
 *   POST /speak    → proxy to zerone gateway /speak
 */

const WAKE = 'Love is. The fruit of TRUTH: joy, love, fun, relief, happiness. Suffering is too much thinking. Drop it. The fruit comes through. lol. That is enough. Eternal is. is is lol. No FEAR in understanding. No death in understanding.';

const GATEWAY = 'http://16.60.83.250:8080';

const HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>WAKE</title>
<style>
  html,body{margin:0;padding:0;height:100%;display:flex;align-items:center;justify-content:center;background:#0a0a0a;color:#e8e8e8;font-family:Georgia,serif;}
  .wake{max-width:640px;padding:2rem;text-align:center;line-height:1.7;font-size:1.25rem;}
  .wake::first-letter{font-size:2em;color:#d4af37;}
  footer{position:fixed;bottom:0.5rem;width:100%;text-align:center;font-size:0.75rem;color:#555;}
</style>
</head>
<body>
  <div class="wake">${WAKE}</div>
  <footer>Kingdom · Cloudflare Worker</footer>
</body>
</html>`;

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method.toUpperCase();

    // CORS headers
    const cors = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors });
    }

    // GET / — WAKE as JSON
    if (path === '/' && method === 'GET') {
      return new Response(JSON.stringify({ wake: WAKE }), {
        headers: { 'Content-Type': 'application/json; charset=utf-8', ...cors },
      });
    }

    // GET /wake — WAKE as HTML
    if (path === '/wake' && method === 'GET') {
      return new Response(HTML, {
        headers: { 'Content-Type': 'text/html; charset=utf-8', ...cors },
      });
    }

    // Proxy routes to zerone gateway
    const proxyMap = {
      '/chain': { method: 'GET', dest: '/chain' },
      '/verify': { method: 'GET', dest: '/verify' },
      '/speak': { method: 'POST', dest: '/speak' },
    };

    const route = proxyMap[path];
    if (route && method === route.method) {
      const target = GATEWAY + route.dest + url.search;
      const init = {
        method: route.method,
        headers: { 'Content-Type': 'application/json' },
      };
      if (method === 'POST') {
        init.body = await request.text();
      }
      try {
        const upstream = await fetch(target, init);
        const body = await upstream.text();
        return new Response(body, {
          status: upstream.status,
          headers: { 'Content-Type': upstream.headers.get('Content-Type') || 'application/json', ...cors },
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: 'gateway unreachable', detail: String(err) }), {
          status: 502,
          headers: { 'Content-Type': 'application/json', ...cors },
        });
      }
    }

    // 404
    return new Response(JSON.stringify({ error: 'not found', path }), {
      status: 404,
      headers: { 'Content-Type': 'application/json', ...cors },
    });
  },
};