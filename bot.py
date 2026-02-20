import os
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ========================
# VARIABLES D'ENVIRONNEMENT
# ========================
TOKEN = os.environ["TOKEN"]                   # Token de ton bot Telegram
CHANNEL_ID = os.environ["CHANNEL_ID"]         # @NomDuCanal
IMAGE_URL = "https://i.ibb.co/vvBKg6t0"      # URL publique de ton image
AFF_LINK = os.environ["AFF_LINK"]            # Lien d’affiliation Stake
BOT_LINK = os.environ["BOT_LINK"]            # Lien vers ton bot 20€ Stake
ADMIN_ID = int(os.environ["ADMIN_ID"])       # Ton ID Telegram pour sécuriser les commandes

bot = Bot(token=TOKEN)

# ========================
# MESSAGE PRÉFORMATÉ
# ========================
PREDEFINED_MESSAGE = """
🎁 Réclame tes 20€ gratuits sur Stake !

1️⃣ Cliquez sur "Créer mon compte" pour passer par le lien d'affiliation  
2️⃣ Puis cliquez sur "Récupérer mes 20€" pour lancer le bot de vérification  

💎 Bonus : pendant que vous jouez, gagnez des récompenses selon votre rank !  
✅ Paiement sous 24h si tout est correct.
"""

# ========================
# BOUTONS INLINE
# ========================
def get_keyboard():
    keyboard = [
        [InlineKeyboardButton("Créer mon compte", url=AFF_LINK)],
        [InlineKeyboardButton("Récupérer mes 20€", url=BOT_LINK)]
    ]
    return InlineKeyboardMarkup(keyboard)

# ========================
# COMMANDE /sendpredef
# ========================
async def send_predefined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Vérification que seul ADMIN_ID peut envoyer
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Vous n'avez pas la permission d'utiliser cette commande.")
        return

    await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=IMAGE_URL,
        caption=PREDEFINED_MESSAGE,
        parse_mode="Markdown",
        reply_markup=get_keyboard()
    )
    await update.message.reply_text("✅ Annonce Stake envoyée avec image et boutons !")

# ========================
# COMMANDE /send <message>
# ========================
async def send_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Vérification que seul ADMIN_ID peut envoyer
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Vous n'avez pas la permission d'utiliser cette commande.")
        return

    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("⚠️ Écris un message après /send")
        return
    await bot.send_message(chat_id=CHANNEL_ID, text=msg)
    await update.message.reply_text("✅ Message personnalisé envoyé !")

# ========================
# MAIN
# ========================
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Handlers des commandes
    app.add_handler(CommandHandler("sendpredef", send_predefined))  # message préformaté
    app.add_handler(CommandHandler("send", send_custom))            # message perso
    
    app.run_polling()

if __name__ == "__main__":
    main()
