document.addEventListener('DOMContentLoaded', () => {
    // Vérifie si l'SDK Telegram Web App est disponible
    if (window.Telegram && window.Telegram.WebApp) {
        const WebApp = window.Telegram.WebApp;

        // Active le bouton de fermeture par défaut si nécessaire
        // WebApp.ready(); 

        // Rends le bouton principal visible (si tu l'utilises)
        // WebApp.MainButton.setText("Salut depuis ma Mini App !").show();
        // WebApp.MainButton.onClick(() => {
        //     alert("Bouton principal cliqué !");
        // });

        // Gérer le clic sur le bouton "Fermer l'application"
        const closeButton = document.getElementById('closeButton');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                // Ferme la Mini App
                WebApp.close();
            });
        }

        // Optionnel : Afficher des informations de débogage
        console.log('Telegram Web App SDK est prêt.');
        console.log('Thème:', WebApp.themeParams);
        console.log('User:', WebApp.initDataUnsafe.user);

    } else {
        console.warn('Telegram Web App SDK non disponible. L\'application ne s\'exécute pas dans Telegram.');
        // Tu peux ajouter une logique pour afficher un message d'erreur ou de test ici
        document.querySelector('.container').innerHTML = '<h1>Bonjour en dehors de Telegram!</h1><p>Cette application est conçue pour être exécutée dans Telegram.</p>';
    }
});