let deferredPrompt = null;

const installCard = document.getElementById("installCard");
const installBtn = document.getElementById("installBtn");


/*
 * Check whether ESA CONNECT is already installed.
 */
function isESAInstalled() {

    return (
        window.matchMedia("(display-mode: standalone)").matches ||
        window.matchMedia("(display-mode: fullscreen)").matches ||
        window.navigator.standalone === true
    );

}


/*
 * Show the ESA installation card
 * for users who have not installed the app.
 */
function showInstallCard() {

    if (!installCard) return;

    if (!isESAInstalled()) {
        installCard.style.display = "block";
    }

}


/*
 * Hide the card only after the app
 * has actually been installed.
 */
function hideInstallCard() {

    if (installCard) {
        installCard.style.display = "none";
    }

}


/*
 * Browser says ESA CONNECT can be installed.
 */
window.addEventListener("beforeinstallprompt", (e) => {

    console.log("✅ ESA PWA installation available");

    e.preventDefault();

    deferredPrompt = e;

    showInstallCard();

});


/*
 * Install button.
 */
if (installBtn) {

    installBtn.addEventListener("click", async () => {

        /*
         * If the browser has supplied the native
         * installation prompt, use it.
         */
        if (deferredPrompt) {

            deferredPrompt.prompt();

            const { outcome } =
                await deferredPrompt.userChoice;

            console.log(
                "ESA installation choice:",
                outcome
            );

            /*
             * IMPORTANT:
             * Do NOT hide the card here.
             *
             * If the user selects Cancel,
             * the card remains visible.
             *
             * Even after accepting, we wait for
             * the appinstalled event.
             */

            deferredPrompt = null;

            showInstallCard();

            return;
        }


        /*
         * If the browser has not supplied
         * beforeinstallprompt, give the user
         * a manual installation instruction.
         */
        alert(
            "ESA CONNECT is ready to be installed. " +
            "Please open your browser menu and select " +
            "\"Install ESA\" or \"Install app\"."
        );

    });

}


/*
 * This event fires after the PWA has actually
 * been installed.
 */
window.addEventListener("appinstalled", () => {

    console.log("🎉 ESA CONNECT installed successfully");

    deferredPrompt = null;

    hideInstallCard();

});


/*
 * Show the card when the page loads.
 *
 * This is the important change.
 *
 * The card is no longer dependent only on
 * beforeinstallprompt.
 */
window.addEventListener("load", () => {

    if (!isESAInstalled()) {

        setTimeout(() => {

            showInstallCard();

        }, 1000);

    }

});


/*
 * If the browser switches into standalone
 * mode after installation, hide the card.
 */
window.addEventListener("visibilitychange", () => {

    if (isESAInstalled()) {

        hideInstallCard();

    }

});