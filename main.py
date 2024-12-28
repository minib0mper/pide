import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Включение логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7463462122:AAEJFKA-ICGqGtTaW366-vcIyv6e094wYAk"  # Замените на ваш токен
Money = 0
money = 0
lang = 0
num = 0
new_text = None
sent_message = None
text = None
delete_text = None
new_text = None
keyboard = None

types = [
    "lox", "loxx", "balic", "earn", "menu"
]

async def langu(update, user_id, query, chat_id, message_id, sent_message, text, context):
    """Функция для отправки сообщения в зависимости от данных в файле."""
    with open('data.txt', 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
        id_found = False
        for line in lines:
            if line.startswith(str(user_id)):
                parts = line.split()
                if len(parts) >= 2:
                    number = parts[1]
                    id_found = True
                    await menuu(query, chat_id, message_id, sent_message, text, context)
                    break
        if not id_found:
            await update.message.reply_text("Ваш ID не найден в базе данных.")

async def data(user_id, money):
    """Обновляет или добавляет данные в файл data.txt."""
    try:
        file_path = 'data.txt'
        lines = []
        try:
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                lines = file.readlines()
        except FileNotFoundError:
            pass

        id_found = False
        for i in range(len(lines)):
            if lines[i].startswith(str(user_id)):
                lines[i] = f"{user_id} {money}\n"
                id_found = True
                break

        if not id_found:
            lines.append(f"{user_id} {money}\n")

        with open(file_path, 'w', encoding='ISO-8859-1') as file:
            file.writelines(lines)

    except Exception as e:
        print(f"Ошибка при работе с файлом: {e}")

def log_visit(user_id, username):
    """ Логирование визитов пользователей. """
    visit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{visit_time} - User ID: {user_id}, Username: {username}"

    try:
        with open("loxi.txt", "r", encoding='ISO-8859-1') as f:
            for line in f:
                if f"User ID: {user_id}" in line:
                    return
    except FileNotFoundError:
        pass

    with open("loxi.txt", "a", encoding='ISO-8859-1') as f:
        f.write(log_entry + "\n")

async def menuu(query, chat_id, message_id, sent_message, text, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id,
        text="👋 Привет, друг!\n\nХочешь легко зарабатывать деньги? Этот бот поможет тебе заработать, выполняя простые задания. 💰\n\n"
             "Как начать зарабатывать прямо в Telegram:\n🔹 **Выполняй задания** и получай деньги сразу.\n🔹 **Приглашай друзей** по своей реферальной ссылке и зарабатывай **$1** за каждого друга, который нажмёт 'start'. 💵\n"
             "🔹 **Выводи заработанные деньги** каждый день. 🔥\n\n🤔 *Почему мы это делаем?*\nПопулярные Telegram-каналы платят нам за привлечение подписчиков, а мы делимся прибылью с тобой. Это выгодно всем!📈📈\n\nНачни прямо сейчас и смотри, как растёт твой доход! 🚀"
    )
    await menu(query, chat_id, message_id, sent_message, text, context)

async def menu(query, chat_id, message_id, sent_message, update, context: ContextTypes.DEFAULT_TYPE):
    global num, new_text
    keyboard = [
        [InlineKeyboardButton("Зарабатывать!🔥", callback_data="earn")],
        [InlineKeyboardButton("Баланс💰", callback_data="balic")],
        [InlineKeyboardButton("Пригласить друга👥", callback_data="lox")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if num == 1:
        await change_message(query, chat_id, message_id, sent_message, "Выбери вариант!📋", context)
        num = 0
    else:
        if update and update.message:
            await update.message.reply_text("Выбери вариант!📋", reply_markup=reply_markup)
        elif query and hasattr(query, "message"):
            await query.message.reply_text("Выбери вариант!📋", reply_markup=reply_markup)
        elif chat_id:
            await context.bot.send_message(
                chat_id=chat_id, text="Выбери вариант!📋", reply_markup=reply_markup
            )
        num = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global num
    global Money, money
    user_id = update.effective_user.id
    chat_id = update.message.chat_id if update.message else None
    message_id = update.message.message_id if update.message else None

    money = 0
    username = update.effective_user.username or "не указано"

    # Логируем пользователя
    log_visit(user_id, username)
    await data(user_id, money)

    num = 0

    # Передаем данные в langu
    await langu(update, user_id, None, chat_id, message_id, None, None, context)

async def change_message(query, chat_id, message_id, sent_message, text, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Зарабатывать!🔥", callback_data="earn")],
        [InlineKeyboardButton("Баланс💰", callback_data="balic")],
        [InlineKeyboardButton("Пригласить друга👥", callback_data="lox")]
    ]

    # Создаем reply_markup только если callback_data соответствует одному из допустимых типов
    types = ["earn", "balic", "lox", "menu"]
    reply_markup = InlineKeyboardMarkup(keyboard) if query and query.data in types else None

    if query and query.message:
        if reply_markup:
            await query.message.edit_text(text, reply_markup=reply_markup)
        else:
            await query.message.edit_text(text)
    elif chat_id:
        # Если объект `query` отсутствует или не имеет message, отправляем новое сообщение
        await context.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=reply_markup
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    global Money, money, new_text, keyboard
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == "menu":
        global num
        num = 1
        keyboard = [
            [InlineKeyboardButton("Зарабатывать!🔥", callback_data="earn")],
            [InlineKeyboardButton("Баланс💰", callback_data="balic")],
            [InlineKeyboardButton("Пригласить друга👥", callback_data="lox")]
        ]   
        new_text = "Выбери вариант!📋"
    elif query.data == "earn":
        await data(user_id, money)
        if money == 0:
            link = 'https://t.me/+_PslAnpWv5owY2Uy'
            money += 1
            Money = '1$'
            keyboard = [
                [InlineKeyboardButton(f"Подписаться✅", callback_data=f"{link}")],
                [InlineKeyboardButton(f"Назад в меню💼", callback_data="menu")]
            ]
            await data(user_id, money)
        elif money == 1:
            link = 'https://t.me/+PT9OOK_m7FI1YWQy'
            money += 1
            Money = '2$'
            keyboard = [
                [InlineKeyboardButton(f"Подписаться✅", callback_data=f"{link}")],
                [InlineKeyboardButton(f"Назад в меню💼", callback_data="menu")]
            ]
            await data(user_id, money)
        elif money == 2:
            link = 'https://t.me/+hOfy2MT0X8JjNzE6'
            money += 1
            Money = '3$'
            keyboard = [
                [InlineKeyboardButton(f"Подписаться✅", callback_data=f"{link}")],
                [InlineKeyboardButton(f"Назад в меню💼", callback_data="menu")]
            ]
            await data(user_id, money)
        elif money == 3:
            link = 'Ссылки кончились, простите'
            money = 0
        keyboard = [
            [InlineKeyboardButton(f"Подписаться✅", callback_data=f"{link}")],
            [InlineKeyboardButton(f"Назад в меню💼", callback_data="menu")]
        ]
        new_text = "Подпишись для вознаграждения!📈📈"
    elif query.data == "balic":
        await data(user_id, money)
        keyboard = [
            [InlineKeyboardButton(f"Назад в меню💼", callback_data="menu")],
            [InlineKeyboardButton(f"Вывести деньги💳", callback_data="loxx")]
        ]
        new_text = f"Ваш баланс: {Money}"
    elif query.data == "loxx":
        keyboard = [
            [InlineKeyboardButton(f"Назад в меню💼", callback_data="menu")],
            [InlineKeyboardButton(f"Пригласить друга👬", callback_data="lox")]
        ]
        new_text = "Для вывода требуется пригласить 10 друзей по ссылке:"
    elif query.data == "lox":
        keyboard = [
            [InlineKeyboardButton(f"Назад в меню💼", callback_data="menu")],
            [InlineKeyboardButton("Скопировать ссылку", callback_data=f"@EZPAY9_bot")]
        ]
        new_text = "Скопируйте ссылку и отправьте другу\n @EZPAY9_bot"

    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=new_text,
        reply_markup=InlineKeyboardMarkup(keyboard) if query.data in types else None
    )

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open('loxi.txt', 'r', encoding='ISO-8859-1') as file:
            lines = file.readlines()
            line_count = len(lines)

        await update.message.reply_text(f"Количество пользователей: {line_count}")
    except FileNotFoundError:
        await update.message.reply_text("Логи отсутствуют.")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("users", users))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()

if __name__ == "__main__":
    main()
