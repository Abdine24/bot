// document.addEventListener('DOMContentLoaded', () => {
//     console.log('DOM Content Loaded - script.js started'); // Message au démarrage du script

//     if (window.Telegram && window.Telegram.WebApp) {
//         const WebApp = window.Telegram.WebApp;
//         console.log('Telegram Web App SDK detected.');
//         WebApp.ready(); 

//         const closeButton = document.getElementById('closeButton');
//         if (closeButton) {
//             console.log('Close button found.');
//             closeButton.addEventListener('click', () => {
//                 console.log('Close button clicked. Closing WebApp...');
//                 WebApp.close(); 
//             });
//         } else {
//             console.warn('Close button not found with ID "closeButton"!');
//         }

//         const myForm = document.getElementById('myForm');
//         if (myForm) {
//             console.log('Form found with ID "myForm".');
//             myForm.addEventListener('submit', (event) => {
//                 event.preventDefault(); // Empêche le rechargement de la page par défaut
//                 console.log('Form submission event triggered.');

//                 const emailInput = document.getElementById('email');
//                 const passwordInput = document.getElementById('password');

//                 if (!emailInput || !passwordInput) {
//                     console.error('Email or password input elements not found in the DOM!');
//                     WebApp.showAlert('Erreur: Champs du formulaire introuvables.');
//                     return; 
//                 }

//                 const email = emailInput.value;
//                 const password = passwordInput.value;

//                 // Validation basique côté client
//                 if (!email || !password) {
//                     WebApp.showAlert('Veuillez remplir tous les champs.');
//                     console.warn('Form submission prevented: fields are empty.');
//                     return;
//                 }
//                 if (!email.includes('@') || !email.includes('.')) {
//                     WebApp.showAlert('Veuillez entrer une adresse email valide.');
//                     console.warn('Form submission prevented: invalid email format.');
//                     return;
//                 }

//                 const formData = {
//                     email: email,
//                     password: password
//                 };
//                 const dataToSend = JSON.stringify(formData);

//                 console.log('Form data prepared:', formData);
//                 console.log('Sending data to bot via WebApp.sendWebAppMessage()...');

//                 WebApp.showAlert(`Formulaire soumis !\nEmail: ${email}\nMot de passe: ${password.replace(/./g, '*')}`);

//                 WebApp.sendWebAppMessage(dataToSend);

//                 myForm.reset(); // RÉINITIALISE LE FORMULAIRE
//                 console.log('Form reset.');
                
//                 // Optionnel : Vous pouvez aussi fermer l'application après un envoi réussi
//                 // WebApp.close(); 
//             });
//         } else {
//             console.error('Form not found with ID "myForm"!');
//         }

//         console.log('Telegram Web App SDK est prêt. Informations supplémentaires :');
//         console.log('Thème:', WebApp.themeParams);
//         console.log('User:', WebApp.initDataUnsafe.user);

//     } else {
//         console.warn('Telegram Web App SDK non disponible. L\'application ne s\'exécute pas dans Telegram.');
//         document.querySelector('.container').innerHTML = '<h1>Bonjour en dehors de Telegram!</h1><p>Cette application est conçue pour être exécutée dans Telegram.</p>';
//     }
// });