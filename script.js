document.addEventListener('DOMContentLoaded', () => {
    // Vérifie si l'SDK Telegram Web App est disponible
    if (window.Telegram && window.Telegram.WebApp) {
        const WebApp = window.Telegram.WebApp;

        // Active le bouton de fermeture par défaut si nécessaire
        // WebApp.ready(); 

        // Gérer le clic sur le bouton "Fermer l'application"
        const closeButton = document.getElementById('closeButton');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                // Ferme la Mini App
                WebApp.close();
            });
        }

        // ---------- Nouvelle logique pour le formulaire ----------
        const myForm = document.getElementById('myForm');
        if (myForm) {
            myForm.addEventListener('submit', (event) => {
                event.preventDefault(); // Empêche le rechargement de la page par défaut

                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;

                console.log('Données du formulaire soumises :');
                console.log('Email:', email);
                console.log('Mot de passe:', password);

                // Optionnel : Afficher un message de confirmation à l'utilisateur
                WebApp.showAlert(`Formulaire soumis !\nEmail: ${email}\nMot de passe: ${password.replace(/./g, '*')}`); // Masque le mdp dans l'alerte

                // ----------- Important pour envoyer des données au bot Telegram -----------
                // Si vous voulez envoyer ces données au bot Python, vous utiliserez WebApp.sendData()
                // ou WebApp.sendWebAppMessage().
                // Par exemple:
                // WebApp.sendData(JSON.stringify({ email: email, password: password }));
                // ou (plus polyvalent pour des messages structurés):
                // WebApp.sendWebAppMessage(JSON.stringify({ type: 'form_submission', email: email, password: password }));

                // Après l'envoi des données, vous pourriez vouloir fermer l'appli ou vider le formulaire
                // WebApp.close(); // Pour fermer l'appli après envoi
                // myForm.reset(); // Pour vider le formulaire
            });
        }
        // ---------- Fin de la nouvelle logique pour le formulaire ----------


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