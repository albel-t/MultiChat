import logging
from debug import InitLogFile, PrintLogOut, TOKEN
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import threading
import sys

# Инициализация лог-файла
InitLogFile()

# Токен бота
#TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Включим логирование, чтобы видеть ошибки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

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
"""
    await update.message.reply_text(help_text)
    PrintLogOut(f"User {update.effective_user.id} requested help")

# Обработчик команды /debug
async def debug_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Это тестовая команда для отладки.")
    PrintLogOut(f"Debug command executed by {update.effective_user.id}")

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

def main() -> None:
    # Создаем приложение и передаем токен бота
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("debug", debug_command))

    # Запускаем поток для консольного ввода
    console_thread = threading.Thread(target=console_sender, args=(application,), daemon=True)
    console_thread.start()

    PrintLogOut("Бот запущен и готов к работе...")

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()