const CACHE_NAME = "esa-v2.1.2";

const STATIC_ASSETS = [
    "/",
    "/static/manifest.json",
    "/static/css/main.css",
    "/static/css/dashboard.css",
    "/static/css/member.css",
    "/static/css/forms.css",
    "/static/css/tables.css",
    "/static/css/messages.css",
    "/static/images/logo.png",
    "/offline"
];

// Install
self.addEventListener("install", event => {

    event.waitUntil(

        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(STATIC_ASSETS))

    );

});
// Activate
self.addEventListener("activate", event => {

    event.waitUntil(

        caches.keys().then(keys =>

            Promise.all(

                keys
                    .filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))

            )

        )

    );

    self.clients.claim();

});

// Fetch
self.addEventListener("fetch", event => {

    if (event.request.method !== "GET") return;

    event.respondWith(

        fetch(event.request)

            .then(response => {

                const clone = response.clone();

                caches.open(CACHE_NAME)

                    .then(cache => cache.put(event.request, clone));

                return response;

            })

            .catch(() =>

                caches.match(event.request)

                    .then(response => {

                        return response || caches.match("/offline");

                    })

            )

    );

});

// Listen for update requests
self.addEventListener("message", event => {

    if (event.data && event.data.type === "SKIP_WAITING") {

        self.skipWaiting();

    }

});