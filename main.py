from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8800314030:AAGfrGLLh9-yCU1pROBrX2LSapMFksYyh-4"
MROBOTICS_TOKEN = "a7a5444d-1153-4f86-825c-6a45147d48f6"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Recharge Bot Online ✅")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
