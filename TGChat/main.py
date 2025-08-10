import logging
import subjection
from debug import InitLogFile, PrintLogOut
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import threading
import sys

# Инициализация лог-файла
InitLogFile()

# Токен бота
TOKEN = subjection.bot_token

# Включим логирование, чтобы видеть ошибки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальная переменная для хранения chat_id с активным режимом перевода
ACTIVE_TRANSLATE_CHATS = set()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f"Привет, {user.mention_html()}! Я бот для отладки.", parse_mode="HTML")
    PrintLogOut(f"User {user.id} started the bot")

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
Доступные команды:
/start - начать работу с ботом
/help - показать это сообщение
/debug - тестовая команда для отладки
/translate - начать вывод сообщений в консоль
/stoptranslate - остановить вывод сообщений в консоль
"""
    await update.message.reply_text(help_text)
    PrintLogOut(f"User {update.effective_user.id} requested help")

# Обработчик команды /debug
async def debug_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Это тестовая команда для отладки.")
    PrintLogOut(f"Debug command executed by {update.effective_user.id}")

# Обработчик команды /translate
async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_user
    
    if chat_id in ACTIVE_TRANSLATE_CHATS:
        await update.message.reply_text("Режим перевода уже включен для этого чата.")
    else:
        ACTIVE_TRANSLATE_CHATS.add(chat_id)
        await update.message.reply_text("Режим перевода включен. Все сообщения будут выводиться в консоль.")
        PrintLogOut(f"Translate mode activated for chat {chat_id} by user {user.full_name} ({user.id})")

# Обработчик команды /stoptranslate
async def stop_translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_user
    
    if chat_id in ACTIVE_TRANSLATE_CHATS:
        ACTIVE_TRANSLATE_CHATS.remove(chat_id)
        await update.message.reply_text("Режим перевода выключен. Сообщения больше не выводятся в консоль.")
        PrintLogOut(f"Translate mode deactivated for chat {chat_id} by user {user.full_name} ({user.id})")
    else:
        await update.message.reply_text("Режим перевода не был активен для этого чата.")

# Обработчик всех текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    
    if chat_id in ACTIVE_TRANSLATE_CHATS:
        user = update.effective_user
        message_text = update.message.text
        
        # Формируем строку для вывода
        output = f"Сообщение от {user.full_name} (ID: {user.id}): {message_text}"
        print(output)  # Вывод в консоль
        PrintLogOut(output)  # Запись в лог
    else:
        print(message_text)  # Вывод в консоль
        PrintLogOut(message_text)  # Запись в лог
# Функция для отправки сообщений из консоли
def console_sender(application):
    while True:
        try:
            console_input = input("Введите chat_id и сообщение (формат: chat_id:message): ")
            if ":" in console_input:
                chat_id, message = console_input.split(":", 1)
                try:
                    chat_id = int(chat_id.strip())
                    message = message.strip()
                    
                    # Используем run_async для асинхронной отправки
                    application.create_task(
                        application.bot.send_message(chat_id=chat_id, text=message)
                    )
                    PrintLogOut(f"Message sent to chat {chat_id}: {message}")
                except ValueError:
                    PrintLogOut("Ошибка: chat_id должен быть числом")
                except Exception as e:
                    PrintLogOut(f"Ошибка при отправке сообщения: {str(e)}")
            else:
                PrintLogOut("Ошибка: используйте формат chat_id:message")
        except KeyboardInterrupt:
            PrintLogOut("Консольный ввод завершен")
            break
        except Exception as e:
            PrintLogOut(f"Ошибка в консольном вводе: {str(e)}")

async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        chat = update.effective_chat
        message = update.message
        
        if message.text:
            content = message.text
        elif message.caption:
            content = f"[MEDIA] {message.caption}"
        else:
            content = "[NON-TEXT CONTENT]"
        if (content[0] != ".") and ((chat.title or 'private') in subjection.active_chats):
            log_entry = f"[] {subjection.names[user.first_name]}: {content}\n"
            PrintLogOut(f"New Message  -  {log_entry[:100]}")

    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")
def main() -> None:
    # Создаем приложение и передаем токен бота
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("debug", debug_command))
    application.add_handler(CommandHandler("translate", translate_command))
    application.add_handler(CommandHandler("stoptranslate", stop_translate_command))
    
    # Добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.ALL, log_message))

    # Запускаем поток для консольного ввода
    console_thread = threading.Thread(target=console_sender, args=(application,), daemon=True)
    console_thread.start()

    PrintLogOut("Бот запущен и готов к работе...")

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()