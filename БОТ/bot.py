from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import nest_asyncio
import asyncio

nest_asyncio.apply()

TOKEN = '8021389548:AAGoOGGt6XVW8LLRSPxloOoE8I1Nr7Erwvg'
GAME_URL = 'https://bejewelled-mandazi-0c9aec.netlify.app/'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Калькулятор", callback_data='calculator')],
        [InlineKeyboardButton("Играть в Память 🎮", url=GAME_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Выбери:', reply_markup=reply_markup)

async def button(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'calculator':
        await query.edit_message_text(text="Вы выбрали Калькулятор. Отправьте математическое выражение.")

async def calculator(update, context):
    await update.message.reply_text("Отправьте математическое выражение, например: 2+2 или 3*5")

async def handle_calculator(update, context):
    try:
        expression = update.message.text
        result = eval(expression)
        keyboard = [[InlineKeyboardButton("Вернуться в меню", callback_data='start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Результат: {result}", reply_markup=reply_markup)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при вычислении: {str(e)}")

async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Играть в Память 🎮", url=GAME_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Запускаем игру!", reply_markup=reply_markup)

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("game", game))
    application.add_handler(CommandHandler("calculator", calculator))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_calculator))
    application.add_handler(CallbackQueryHandler(button))
    
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
