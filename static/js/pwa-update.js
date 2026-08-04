let newWorker = null;

// Listen for Service Worker updates
if ("serviceWorker" in navigator) {

    navigator.serviceWorker.ready.then((registration) => {

        // Wait a moment for Chrome to move the worker into "waiting"
        setTimeout(() => {

            if (registration.waiting) {

                console.log("✅ Waiting worker found");

                showUpdateBanner(registration.waiting);

            } else {

                console.log("❌ No waiting worker");

            }

        }, 500);

        // Detect future updates
        registration.addEventListener("updatefound", () => {

            const installingWorker = registration.installing;

            installingWorker.addEventListener("statechange", () => {

                if (
                    installingWorker.state === "installed" &&
                    navigator.serviceWorker.controller
                ) {

                    console.log("🚀 New update installed");

                    showUpdateBanner(installingWorker);

                }

            });

        });

    });

}

function showUpdateBanner(worker) {

    console.log("Worker object:", worker);
    console.log("Type:", typeof worker);
    console.log("Has postMessage:", typeof worker.postMessage);

    newWorker = worker;

    const banner = document.getElementById("updateBanner");

    if (banner) {
        banner.style.display = "block";
    }

}

// User clicks Update
document.addEventListener("DOMContentLoaded", () => {

    const btn = document.getElementById("updateNow");

    if (!btn) return;

    btn.addEventListener("click", () => {

        if (!newWorker) return;

        newWorker.postMessage({
            type: "SKIP_WAITING"
        });

    });

});

// Reload automatically after activation
navigator.serviceWorker.addEventListener("controllerchange", () => {

    window.location.reload();

});