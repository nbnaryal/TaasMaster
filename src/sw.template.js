/* TaasMaster service worker: precache the whole site, serve from cache first, refresh in the background. */
const CACHE = 'taasmaster-__VERSION__';
const PRECACHE = __PRECACHE__;
const ROOT = '__ROOT__';

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((k) => k.startsWith('taasmaster-') && k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    // Pages are cached as "/x/" — match "/x/?source=pwa" etc. too. Assets keep their ?v= version.
    const isPage = req.mode === 'navigate';
    const hit = await cache.match(req, { ignoreSearch: isPage });
    const network = fetch(req).then((res) => {
      if (res && res.ok && res.type === 'basic') cache.put(isPage ? url.pathname : req, res.clone());
      return res;
    }).catch(() => null);
    if (hit) { e.waitUntil(network); return hit; }
    const res = await network;
    if (res) return res;
    if (isPage) {
      const home = url.pathname.startsWith(ROOT + 'ne/') ? ROOT + 'ne/' : ROOT;
      return (await cache.match(home)) || (await cache.match(ROOT + '404.html'));
    }
    return Response.error();
  })());
});
