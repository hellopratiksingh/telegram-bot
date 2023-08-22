import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "6448817659:AAGCGYYfTr_BKZQrAcbX9HY8UMQ3P4_5vdM"  # Replace with your actual bot token

NUMBER_EMOJIS = [
    "0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", 
    "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"
]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send /count <minutes> <message>")

def count(update: Update, context: CallbackContext) -> None:
    args = context.args
    if len(args) < 2:
        update.message.reply_text("Usage: /count <minutes> <message>")
        return

    try:
        minutes = int(args[0])
    except ValueError:
        update.message.reply_text("Invalid input. Minutes must be an integer.")
        return

    countdown_message = " ".join(args[1:])
    chat_id = update.message.chat_id

    countdown_msg = update.message.reply_text(f"Countdown: {minutes} minutes")
    update.message.delete()

    for remaining_time in range(minutes * 60, -1, -1):
        minutes_display = remaining_time // 60
        seconds_display = remaining_time % 60
        countdown_text = f"Countdown: {NUMBER_EMOJIS[minutes_display // 10]}{NUMBER_EMOJIS[minutes_display % 10]} minutes {NUMBER_EMOJIS[seconds_display // 10]}{NUMBER_EMOJIS[seconds_display % 10]} seconds"
        countdown_msg.edit_text(countdown_text)
        time.sleep(1)

    update.message.bot.send_message(chat_id, f"Countdown finished! Message: {countdown_message}")
    countdown_msg.delete()

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("count", count))
    dp.add_handler(MessageHandler(Filters.command, lambda update, context: update.message.delete()))  # Delete all other command messages

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
