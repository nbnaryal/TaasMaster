/* Call Break Ledger — service worker.
   Keeps a copy of the app on the device so it opens and works with no internet.
   Your games are stored separately (in the browser's local storage) and are never touched here.

   Releasing an update: just upload the new files. The page itself is always fetched fresh
   when online; bump VERSION below only if you add or rename files in SHELL. */

const VERSION = 'v1';
const CACHE = `callbreak-${VERSION}`;
const SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/icon.svg',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/maskable-192.png',
  './icons/maskable-512.png',
  './icons/apple-touch-icon.png',
  './icons/favicon-32.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k.startsWith('callbreak-') && k !== CACHE).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  if (req.mode === 'navigate') event.respondWith(pageNetworkFirst(req));
  else event.respondWith(assetCacheFirst(req, event));
});

// The app page: use the network when it answers within 4 s (so updates appear straight away),
// otherwise the saved copy.
async function pageNetworkFirst(req) {
  const cache = await caches.open(CACHE);
  const network = fetch(req, { cache: 'no-cache' }).then(async (res) => {
    if (res.ok) await cache.put('./index.html', await cleanCopy(res.clone()));
    return res;
  });
  network.catch(() => {}); // handled below
  const cached = cache.match('./index.html');
  try {
    return await Promise.race([
      network,
      wait(4000).then(async () => (await cached) || network),
    ]);
  } catch (e) {
    return (await cached) || (await cache.match('./')) ||
      new Response('Call Break Ledger is offline and has not been saved on this device yet.', {
        status: 503, headers: { 'Content-Type': 'text/plain; charset=utf-8' },
      });
  }
}

// Icons, manifest: saved copy first, refreshed quietly in the background.
async function assetCacheFirst(req, event) {
  const cache = await caches.open(CACHE);
  const cached = await cache.match(req, { ignoreSearch: true });
  const network = fetch(req)
    .then((res) => { if (res.ok) cache.put(req, res.clone()); return res; })
    .catch(() => cached || Response.error());
  if (cached) { event.waitUntil(network); return cached; }
  return network;
}

// A redirected response can't be replayed for a page load, so store a plain copy.
async function cleanCopy(res) {
  if (!res.redirected) return res;
  return new Response(await res.blob(), { status: res.status, statusText: res.statusText, headers: res.headers });
}

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
