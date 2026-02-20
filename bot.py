import os
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Variables d'environnement
TOKEN = os.environ["TOKEN"]                   # Token de ton bot
CHANNEL_ID = os.environ["CHANNEL_ID"]         # @NomDuCanal
IMAGE_URL = "https://i.ibb.co/vvBKg6t0"      # Ton image Stake
AFF_LINK = os.environ["AFF_LINK"]            # Ton lien d’affiliation Stake
BOT_LINK = os.environ["BOT_LINK"]            # Lien vers ton bot 20€ Stake

bot = Bot(token=TOKEN)

# Message texte avec instructions et conditions
PREDEFINED_MESSAGE = """
🎁 Réclame tes 20€ gratuits sur Stake !

1️⃣ Cliquez sur "Créer mon compte" pour passer par le lien d'affiliation  
2️⃣ Puis cliquez sur "Récupérer mes 20€" pour lancer le bot de vérification  

💎 Bonus : pendant que vous jouez, gagnez des récompenses selon votre rank !  
✅ Paiement sous 24h si tout est correct.
"""

# Boutons inline
def get_keyboard():
    keyboard = [
        [InlineKeyboardButton("Créer mon compte", url=AFF_LINK)],
        [InlineKeyboardButton("Récupérer mes 20€", url=BOT_LINK)]
    ]
    return InlineKeyboardMarkup(keyboard)

# Commande pour envoyer le message préformaté avec image + boutons
async def send_predefined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=IMAGE_URL,
        caption=PREDEFINED_MESSAGE,
        parse_mode="Markdown",
        reply_markup=get_keyboard()
    )
    await update.message.reply_text("✅ Annonce Stake envoyée avec image et boutons !")

# Commande pour envoyer un message personnalisé texte
async def send_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("⚠️ Écris un message après /send")
        return
    await bot.send_message(chat_id=CHANNEL_ID, text=msg)
    await update.message.reply_text("✅ Message personnalisé envoyé !")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("sendpredef", send_predefined))  # annonce préformatée
    app.add_handler(CommandHandler("send", send_custom))            # message perso
    
    app.run_polling()

if __name__ == "__main__":
    main()
