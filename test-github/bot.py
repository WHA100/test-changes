import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
import random

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Состояния для ConversationHandler
ASK_NAME = 1

# Словарь для хранения зарегистрированных пользователей (user_id: name)
registered_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Для регистрации введите, пожалуйста, ваше имя:')
    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    name = update.message.text.strip()
    registered_users[user_id] = name
    await update.message.reply_text(f'Спасибо, {name}! Вы успешно зарегистрированы.')
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Регистрация отменена.')
    return ConversationHandler.END

# --- Мини-игра ---
async def game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 100)
    context.user_data['number'] = number
    context.user_data['attempts'] = 0
    await update.message.reply_text('Я загадал число от 1 до 100. Попробуй угадать! Напиши число или /cancel для выхода.')
    return ASK_NAME

async def game_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        guess = int(update.message.text)
    except ValueError:
        await update.message.reply_text('Пожалуйста, введи целое число!')
        return ASK_NAME
    number = context.user_data['number']
    context.user_data['attempts'] += 1
    if guess < number:
        await update.message.reply_text('Мое число больше!')
        return ASK_NAME
    elif guess > number:
        await update.message.reply_text('Мое число меньше!')
        return ASK_NAME
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

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)

    print('Бот запущен...')
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main()) 