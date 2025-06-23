import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Обработчик команды /start
def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return update.message.reply_text('Привет! Я тестовый бот.')

# Обработчик текстовых сообщений
def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return update.message.reply_text(f'Вы написали: {update.message.text}')

async def main():
    # Замените 'YOUR_TOKEN' на токен вашего бота
    app = ApplicationBuilder().token('YOUR_TOKEN').build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print('Бот запущен...')
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main()) 