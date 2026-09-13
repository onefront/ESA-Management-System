let deferredPrompt = null;

const installCard = document.getElementById("installCard");
const installBtn = document.getElementById("installBtn");


/*
 * Check whether ESA CONNECT is currently
 * running as an installed PWA.
 */
function isESAInstalled() {

    return (
        window.matchMedia("(display-mode: standalone)").matches ||
        window.matchMedia("(display-mode: fullscreen)").matches ||
        window.matchMedia("(display-mode: minimal-ui)").matches ||
        window.navigator.standalone === true
    );

}


/*
 * Show the installation card.
 */
function showInstallCard() {

    if (!installCard) return;

    if (isESAInstalled()) {

        hideInstallCard();

        return;

    }

    installCard.style.display = "block";

}


/*
 * Hide the installation card.
 */
function hideInstallCard() {

    if (installCard) {

        installCard.style.display = "none";

    }

}


/*
 * Browser provides the native installation
 * prompt.
 */
window.addEventListener("beforeinstallprompt", (event) => {

    console.log("✅ ESA PWA installation available");

    event.preventDefault();

    deferredPrompt = event;

    showInstallCard();

});


/*
 * Install button.
 */
if (installBtn) {

    installBtn.addEventListener("click", async () => {

        /*
         * Native installation prompt available.
         */
        if (deferredPrompt) {

            deferredPrompt.prompt();

            const choiceResult =
                await deferredPrompt.userChoice;

            console.log(
                "ESA installation choice:",
                choiceResult.outcome
            );

            if (choiceResult.outcome === "accepted") {

                console.log(
                    "✅ ESA CONNECT installation accepted"
                );

                /*
                 * The appinstalled event will
                 * hide the card.
                 */

            } else {

                console.log(
                    "ℹ️ ESA CONNECT installation cancelled"
                );

                /*
                 * Keep the card visible.
                 */
                showInstallCard();

            }

            deferredPrompt = null;

            return;

        }


        /*
         * Native prompt is unavailable.
         */
        showInstallHelp();

    });

}


/*
 * Manual installation instructions.
 */
function showInstallHelp() {

    if (!installCard) return;

    let help =
        document.getElementById("installHelp");


    if (!help) {

        help = document.createElement("div");

        help.id = "installHelp";

        help.className =
            "alert alert-info mt-3 mb-0 small";

        help.innerHTML =
            "<strong>Installation:</strong><br>" +
            "Open the browser menu and select " +
            "<strong>Install ESA CONNECT</strong> " +
            "or <strong>Install app</strong>.";

        installCard.appendChild(help);

    }

    help.style.display = "block";

}


/*
 * Fired when the PWA has actually been installed.
 */
window.addEventListener("appinstalled", () => {

    console.log(
        "🎉 ESA CONNECT installed successfully"
    );

    deferredPrompt = null;

    hideInstallCard();

});


/*
 * Initial check.
 */
window.addEventListener("load", () => {

    setTimeout(() => {

        if (isESAInstalled()) {

            hideInstallCard();

        } else {

            showInstallCard();

        }

    }, 500);

});


/*
 * Check again whenever the page becomes visible.
 */
document.addEventListener("visibilitychange", () => {

    if (isESAInstalled()) {

        hideInstallCard();

    } else {

        showInstallCard();

    }

});