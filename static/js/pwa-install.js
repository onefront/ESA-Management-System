let deferredPrompt = null;

const installCard = document.getElementById("installCard");
const installBtn = document.getElementById("installBtn");


function isESAInstalled() {

    return (
        window.matchMedia("(display-mode: standalone)").matches ||
        window.matchMedia("(display-mode: fullscreen)").matches ||
        window.matchMedia("(display-mode: minimal-ui)").matches ||
        window.navigator.standalone === true
    );

}


function showInstallCard() {

    if (!installCard) return;

    if (isESAInstalled()) {
        hideInstallCard();
        return;
    }

    installCard.style.display = "block";

}


function hideInstallCard() {

    if (installCard) {
        installCard.style.display = "none";
    }

}


/*
 * Capture the browser installation event.
 *
 * Store it in both the local variable and window so the
 * Install App button can access the same event reliably.
 */
window.addEventListener("beforeinstallprompt", (event) => {

    console.log("✅ ESA PWA installation available");

    event.preventDefault();

    deferredPrompt = event;
    window.esaDeferredPrompt = event;

    showInstallCard();

});


if (installBtn) {

    installBtn.addEventListener("click", async () => {

        const installEvent =
            deferredPrompt || window.esaDeferredPrompt;

        console.log(
            "ESA install event available:",
            !!installEvent
        );

        if (!installEvent) {

            showInstallHelp();

            return;

        }


        try {

            await installEvent.prompt();

            const choiceResult =
                await installEvent.userChoice;

            console.log(
                "ESA installation choice:",
                choiceResult.outcome
            );


            if (choiceResult.outcome === "accepted") {

                console.log(
                    "✅ ESA CONNECT installation accepted"
                );

            } else {

                console.log(
                    "ℹ️ ESA CONNECT installation cancelled"
                );

            }

        } catch (error) {

            console.error(
                "❌ ESA CONNECT installation failed:",
                error
            );

        }


        deferredPrompt = null;
        window.esaDeferredPrompt = null;

    });

}


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


window.addEventListener("appinstalled", () => {

    console.log(
        "🎉 ESA CONNECT installed successfully"
    );

    deferredPrompt = null;
    window.esaDeferredPrompt = null;

    hideInstallCard();

});


window.addEventListener("load", () => {

    setTimeout(() => {

        if (isESAInstalled()) {

            hideInstallCard();

        } else {

            showInstallCard();

        }

    }, 500);

});


document.addEventListener("visibilitychange", () => {

    if (isESAInstalled()) {

        hideInstallCard();

    } else {

        showInstallCard();

    }

});