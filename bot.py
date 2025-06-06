
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json # Pour gérer les données JSON

# Remplace ceci par le TOKEN de ton bot que tu as obtenu de BotFather
BOT_TOKEN = "7174970942:AAHlhoex6SYFTiD8mQbMSSpYw3vaSBQDi8Y"

# Remplace ceci par l'URL où tu as hébergé ton fichier index.html
WEB_APP_URL = "https://abdine24.github.io/bot/index.html"

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

async def web_app_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gère les données envoyées par la Mini App."""
    
    # Les données de la Web App sont dans update.effective_message.web_app_data.data
    web_app_data = update.effective_message.web_app_data.data
    
    try:
        # Tente de convertir la chaîne JSON en un objet Python (dictionnaire)
        data = json.loads(web_app_data)
        
        email = data.get("email")
        password = data.get("password") # Attention: Ne jamais stocker le mot de passe en clair en production!

        user_id = update.effective_user.id # L'ID Telegram de l'utilisateur
        username = update.effective_user.username # Le nom d'utilisateur Telegram (s'il existe)

        print(f"Données reçues de la Mini App pour l'utilisateur {user_id} (@{username}):")
        print(f"Email: {email}")
        print(f"Mot de passe: {password}") # À des fins de test uniquement !

        # --- C'est ici que tu traites les données ! ---
        # Tu peux:
        # 1. Les stocker dans une base de données (SQLite, PostgreSQL, MongoDB, etc.)
        # 2. Vérifier si l'utilisateur existe déjà
        # 3. Envoyer un email de confirmation (avec un service externe)
        # 4. Enregistrer l'utilisateur pour tes services
        # 5. Envoyer un message de confirmation à l'utilisateur via le bot:
        await update.message.reply_text(
            f"Merci pour votre inscription !\n"
            f"Email: {email}\n"
            f"Nous avons bien reçu vos informations."
            # Ne jamais renvoyer le mot de passe à l'utilisateur !
        )

    except json.JSONDecodeError:
        print(f"Erreur: Données de la Web App non-JSON : {web_app_data}")
        await update.message.reply_text("Désolé, une erreur est survenue lors de la réception de vos données.")
    except Exception as e:
        print(f"Erreur inattendue lors du traitement des données de la Web App : {e}")
        await update.message.reply_text("Désolé, une erreur interne est survenue.")


def main() -> None:
    """Démarre le bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Gestionnaire pour la commande /start
    application.add_handler(CommandHandler("start", start))
    
    # NOUVEAU: Gestionnaire pour les données envoyées par la Web App
    # Le filtre filters.WEB_APP_DATA détecte les messages envoyés par sendWebAppMessage()
    application.add_handler(MessageHandler(filters.WEB_APP_DATA, web_app_data_handler))

    # Lance le bot
    print("Bot démarré. En attente de commandes et de données de Mini App...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()