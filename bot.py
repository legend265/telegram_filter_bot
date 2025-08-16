import os
from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

# === CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")  # read from Render environment variable
BANNED_WORDS = ["badword1", "badword2", "slur1", "slur2"]
WARN_USERS = True  # set to False if you don't want warning messages

# === FILTER HANDLER ===
async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        message_text = update.message.text.lower()
        for word in BANNED_WORDS:
            if word in message_text:
                try:
                    await update.message.delete()
                    if WARN_USERS:
                        await update.message.chat.send_message(
                            f"⚠️ Message from {update.message.from_user.mention_html()} "
                            f"was removed for containing a banned word.",
                            parse_mode="HTML"
                        )
                except Exception as e:
                    print(f"Error deleting message: {e}")
                break

# === MAIN ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()