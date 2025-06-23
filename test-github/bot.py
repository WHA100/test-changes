import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
import random

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

GAME = range(1)

# Обработчик команды /start
def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return update.message.reply_text('Привет! Я тестовый бот.')

# Обработчик команды /help
def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return update.message.reply_text(
        '/start — начать
/help — список команд
/about — о боте
/game — мини-игра "Угадай число"
/cancel — выйти из игры'
    )

# Обработчик команды /about
def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return update.message.reply_text('Я бот для тестирования. Теперь у меня есть мини-игра!')

# Обработчик текстовых сообщений
def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return update.message.reply_text(f'Вы написали: {update.message.text}')

# --- Мини-игра ---
async def game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 100)
    context.user_data['number'] = number
    context.user_data['attempts'] = 0
    await update.message.reply_text('Я загадал число от 1 до 100. Попробуй угадать! Напиши число или /cancel для выхода.')
    return GAME

async def game_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        guess = int(update.message.text)
    except ValueError:
        await update.message.reply_text('Пожалуйста, введи целое число!')
        return GAME
    number = context.user_data['number']
    context.user_data['attempts'] += 1
    if guess < number:
        await update.message.reply_text('Мое число больше!')
        return GAME
    elif guess > number:
        await update.message.reply_text('Мое число меньше!')
        return GAME
    else:
        attempts = context.user_data['attempts']
        await update.message.reply_text(f'Поздравляю! Ты угадал число {number} за {attempts} попыток!')
        return ConversationHandler.END

async def game_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Игра окончена. Если захочешь сыграть снова — напиши /game!')
    return ConversationHandler.END

async def main():
    # Замените 'YOUR_TOKEN' на токен вашего бота
    app = ApplicationBuilder().token('YOUR_TOKEN').build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('about', about))

    game_handler = ConversationHandler(
        entry_points=[CommandHandler('game', game_start)],
        states={
            GAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, game_guess)]
        },
        fallbacks=[CommandHandler('cancel', game_cancel)]
    )
    app.add_handler(game_handler)
    app.add_handler(CommandHandler('cancel', game_cancel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print('Бот запущен...')
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main()) 