let deferredPrompt = null;

const installCard = document.getElementById("installCard");
const installBtn = document.getElementById("installBtn");

window.addEventListener("beforeinstallprompt", (e) => {

    console.log("✅ beforeinstallprompt fired");

    e.preventDefault();

    deferredPrompt = e;

    if (installCard) {
        installCard.style.display = "block";
    }

});

if (installBtn) {

    installBtn.addEventListener("click", async () => {

        if (!deferredPrompt) return;

        deferredPrompt.prompt();

        const { outcome } = await deferredPrompt.userChoice;

        if (outcome === "accepted") {
            console.log("✅ ESA installed");
        }

        deferredPrompt = null;

        if (installCard) {
            installCard.style.display = "none";
        }

    });

}

window.addEventListener("appinstalled", () => {

    console.log("🎉 ESA App Installed");

    if (installCard) {
        installCard.remove();
    }

});