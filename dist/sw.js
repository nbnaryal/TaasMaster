/* TaasMaster service worker: precache the whole site, serve from cache first, refresh in the background. */
const CACHE = 'taasmaster-050681f743';
const PRECACHE = ["/", "/call-break-score/", "/marriage-calculator/", "/teen-patti-tracker/", "/call-break-rules/", "/marriage-rules/", "/teen-patti-rules/", "/faq/", "/ne/", "/ne/call-break-score/", "/ne/marriage-calculator/", "/ne/teen-patti-tracker/", "/ne/call-break-rules/", "/ne/marriage-rules/", "/ne/teen-patti-rules/", "/ne/faq/", "/404.html", "/assets/style.css?v=050681f743", "/assets/app.js?v=050681f743", "/manifest.webmanifest", "/ne/manifest.webmanifest", "/icons/favicon.svg", "/icons/icon-192.png", "/icons/icon-512.png", "/icons/maskable-512.png", "/icons/apple-touch-icon.png"];

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
      const home = url.pathname.startsWith('/ne/') ? '/ne/' : '/';
      return (await cache.match(home)) || (await cache.match('/404.html'));
    }
    return Response.error();
  })());
});
