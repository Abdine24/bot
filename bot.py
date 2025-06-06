from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json
import os

# === Configuration ===
BOT_TOKEN = "7174970942:AAHlhoex6SYFTiD8mQbMSSpYw3vaSBQDi8Y"
WEB_APP_URL = "https://abdine24.github.io/bot/index.html"

# === Fichier JSON pour stocker les utilisateurs ===
USERS_DB_FILE = "users.json"  # Simple, à la racine du projet

# === Fonctions de gestion de la base de données ===
def load_users():
    if os.path.exists(USERS_DB_FILE):
        try:
            with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Fichier JSON corrompu. Base vide recréée.")
            return {}
        except Exception as e:
            print(f"❌ Erreur lors du chargement : {e}")
            return {}
    return {}

def save_users(data):
    try:
        with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("✅ Données sauvegardées.")
    except Exception as e:
        print(f"❌ Erreur de sauvegarde : {e}")

# === Commande /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("Ouvrir mon application", web_app=WebAppInfo(url=WEB_APP_URL))
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Bienvenue ! Cliquez sur le bouton ci-dessous pour ouvrir l'application.",
        reply_markup=reply_markup
    )

# === Réception des données de la WebApp ===
async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message and update.effective_message.web_app_data:
        try:
            data = json.loads(update.effective_message.web_app_data.data)
            email = data.get("email")
            password = data.get("password")
            user_id = update.effective_user.id
            username = update.effective_user.username
            print(f"✅ Données reçues : {data}")

            users = load_users()

            if email in users:
                await update.message.reply_text(
                    f"👋 Bonjour encore, {email} ! Vous êtes déjà inscrit."
                )
            else:
                users[email] = {
                    "telegram_user_id": user_id,
                    "telegram_username": username,
                    "password": password,
                    "registration_date": update.message.date.isoformat()
                }
                save_users(users)
                await update.message.reply_text(
                    f"🎉 Merci pour votre inscription, {email} !"
                )
        except json.JSONDecodeError:
            print("⚠️ Données reçues non valides (pas en JSON)")
            await update.message.reply_text("Erreur : données invalides.")
        except Exception as e:
            print(f"❌ Erreur interne : {e}")
            await update.message.reply_text("Erreur interne du serveur.")
    else:
        await update.message.reply_text("Tapez /start pour lancer la Mini App.")

# === Lancement du bot ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_all_messages))
    print("🚀 Bot démarré et en attente...")
    app.run_polling()

if __name__ == "__main__":
    main()
