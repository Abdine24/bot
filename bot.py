import os
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json # Pour gérer les données JSON
import os   # Pour vérifier l'existence de fichiers

# Remplace ceci par le TOKEN de ton bot que tu as obtenu de BotFather
BOT_TOKEN = "7174970942:AAHlhoex6SYFTiD8mQbMSSpYw3vaSBQDi8Y"

# Remplace ceci par l'URL où tu as hébergé ton fichier index.html
WEB_APP_URL = "https://abdine24.github.io/bot/index.html"

# Nom du fichier où les données des utilisateurs seront stockées
USERS_DB_FILE = os.path.join(os.path.dirname(__file__), 'users.json')


# --- Fonctions de gestion de la base de données JSON ---

def load_users():
    """Charge les utilisateurs depuis le fichier JSON."""
    if os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Si le fichier est vide ou corrompu, retourne un dictionnaire vide
                return {}
    return {} # Retourne un dictionnaire vide si le fichier n'existe pas

def save_users(users_data):
    """Sauvegarde les utilisateurs dans le fichier JSON."""
    with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=4, ensure_ascii=False)

# --- FIN Fonctions de gestion de la base de données JSON ---


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envoie un message avec un bouton pour ouvrir la Mini App."""
    keyboard = [
        [InlineKeyboardButton("Ouvrir mon application", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Salut ! Clique sur le bouton ci-dessous pour lancer ma super Mini App :",
        reply_markup=reply_markup
    )

async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gère tous les messages et filtre ceux de la Mini App."""
    
    # Vérifie si le message provient d'une Web App
    if update.effective_message and update.effective_message.web_app_data:
        web_app_data = update.effective_message.web_app_data.data
        
        try:
            data = json.loads(web_app_data)
            
            email = data.get("email")
            password = data.get("password") 

            user_id = update.effective_user.id
            username = update.effective_user.username

            print(f"Données reçues de la Mini App pour l'utilisateur {user_id} (@{username if username else 'N/A'}):")
            print(f"Email: {email}")
            print(f"Mot de passe: {password}")

            # --- NOUVEAU : Traitement et stockage des données ---
            users = load_users() # Charge les utilisateurs existants

            if email in users:
                # Si l'email existe déjà
                await update.message.reply_text(
                    f"Bonjour de nouveau, {email} ! Vos informations semblent déjà enregistrées.\n"
                    f"Si vous souhaitez modifier votre mot de passe, utilisez une autre option."
                )
            else:
                # Nouvel utilisateur
                users[email] = {
                    "telegram_user_id": user_id,
                    "telegram_username": username,
                    "password": password, # ATTENTION: Ceci stocke le MDP en clair. HACHEZ-LE EN PRODUCTION !
                    "registration_date": update.message.date.isoformat() # Date d'inscription
                }
                save_users(users) # Sauvegarde les utilisateurs mis à jour

                await update.message.reply_text(
                    f"Merci pour votre inscription, {email} !\n"
                    f"Nous avons bien reçu vos informations et les avons enregistrées."
                )
            # --- FIN NOUVEAU ---

        except json.JSONDecodeError:
            print(f"Erreur: Données de la Web App non-JSON : {web_app_data}")
            await update.message.reply_text("Désolé, une erreur est survenue lors de la réception de vos données.")
        except Exception as e:
            print(f"Erreur inattendue lors du traitement des données de la Web App : {e}")
            await update.message.reply_text("Désolé, une erreur interne est survenue.")
    else:
        # Si ce n'est pas un message de Web App, tu peux gérer d'autres types de messages ici
        if update.effective_message.text:
            await update.message.reply_text(f"J'ai reçu votre message : {update.effective_message.text}. Pour lancer l'application, tapez /start.")


def main() -> None:
    """Démarre le bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Gestionnaire pour la commande /start
    application.add_handler(CommandHandler("start", start))
    
    # Gère tous les messages et les filtre manuellement à l'intérieur de la fonction
    application.add_handler(MessageHandler(filters.ALL, handle_all_messages))

    # Lance le bot
    print("Bot démarré. En attente de commandes et de données de Mini App...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()