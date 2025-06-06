from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Remplace ceci par le TOKEN de ton bot que tu as obtenu de BotFather
BOT_TOKEN = "7174970942:AAHlhoex6SYFTiD8mQbMSSpYw3vaSBQDi8Y"

# Remplace ceci par l'URL où tu as hébergé ton fichier index.html
# Assure-toi que c'est une URL HTTPS !
WEB_APP_URL = "https://abdine24.github.io/bot" 
# Exemple: si tu utilises un simple serveur HTTP local pour tester, ça pourrait être "http://localhost:8000/index.html"
# Mais pour le déploiement réel, il FAUT du HTTPS.

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envoie un message avec un bouton pour ouvrir la Mini App."""
    
    # Crée un bouton qui ouvre la Web App
    keyboard = [
        [InlineKeyboardButton("Ouvrir mon application", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envoie le message avec le bouton
    await update.message.reply_text(
        "Salut ! Clique sur le bouton ci-dessous pour lancer ma super Mini App :",
        reply_markup=reply_markup
    )

def main() -> None:
    """Démarre le bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Commande pour démarrer le bot
    application.add_handler(CommandHandler("start", start))

    # Lance le bot
    print("Bot démarré. En attente de commandes...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()