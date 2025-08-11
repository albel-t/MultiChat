import logging
import subjection
from debug import InitLogFile, PrintLogOut
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import threading
import sys
import asyncio

# Инициализация лог-файла
InitLogFile()

# Токен бота
TOKEN = subjection.bot_token
CountMessages = 0
# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TranslateMode:
    def __init__(self):
        self.active_chats = set()  # Хранит ID чатов с активным режимом
    
    def add_chat(self, chat_id):
        self.active_chats.add(chat_id)
    
    def remove_chat(self, chat_id):
        self.active_chats.discard(chat_id)
    
    def is_active(self, chat_id):
        return chat_id in self.active_chats

translate_mode = TranslateMode()

async def get_chat_info(update: Update):
    """Получает информацию о чате и пользователе"""
    chat = update.effective_chat
    user = update.effective_user
    
    chat_info = {
        'chat_id': chat.id,
        'chat_title': chat.title if hasattr(chat, 'title') else "Личная переписка",
        'user_name': user.full_name if user else "Неизвестный пользователь",
        'user_id': user.id if user else None
    }
    return chat_info

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    await update.message.reply_text(f"Привет, {chat_info['user_name']}! Я бот для отладки.")
    PrintLogOut(f"User {chat_info['user_id']} started bot in chat {chat_info['chat_id']}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = '''
Доступные команды:
/start - начать работу
/help - справка
/translate - начать вывод сообщений
/stoptranslate - остановить вывод

---------------
''' + str(CountMessages) + ''' cообщений отправленно с момента включения бота!

'''
    await update.message.reply_text(help_text)

async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    
    if translate_mode.is_active(chat_info['chat_id']):
        await update.message.reply_text("Режим перевода уже включен!")
    else:
        translate_mode.add_chat(chat_info['chat_id'])
        await update.message.reply_text("✅ Режим перевода включен")
        PrintLogOut(f"Translate ON in chat '{chat_info['chat_title']}' ({chat_info['chat_id']})")

async def stop_translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    
    if translate_mode.is_active(chat_info['chat_id']):
        translate_mode.remove_chat(chat_info['chat_id'])
        await update.message.reply_text("❌ Режим перевода выключен")
        PrintLogOut(f"Translate OFF in chat '{chat_info['chat_title']}' ({chat_info['chat_id']})")
    else:
        await update.message.reply_text("Режим перевода не был активен")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    PrintLogOut(f"New message!")
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
        log_entry = f"[{subjection.names[user.first_name]}]: {content}\n" 
        if (content[0] != ".") and ((chat.title or 'private') in subjection.active_chats):
            PrintLogOut(f"{log_entry[:100]}")


    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")

def console_sender(application):
    while True:
        try:
            console_input = input("Введите chat_id:сообщение: ")
            if ":" in console_input:
                chat_id, message = console_input.split(":", 1)
                try:
                    chat_id = int(chat_id.strip())
                    asyncio.run_coroutine_threadsafe(
                        application.bot.send_message(chat_id, message.strip()),
                        application.create_task
                    )
                    PrintLogOut(f"Sent to {chat_id}: {message.strip()}")
                except ValueError:
                    PrintLogOut("Ошибка: chat_id должен быть числом")
                except Exception as e:
                    PrintLogOut(f"Ошибка отправки: {str(e)}")
            else:
                PrintLogOut("Используйте формат chat_id:message")
        except (KeyboardInterrupt, SystemExit):
            PrintLogOut("Консольный ввод остановлен")
            break
        except Exception as e:
            PrintLogOut(f"Ошибка ввода: {str(e)}")

def main():
    application = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков
    handlers = [
        CommandHandler("start", start),
        CommandHandler("help", help_command),
        CommandHandler("translate", translate_command),
        CommandHandler("stoptranslate", stop_translate_command),
        MessageHandler(filters.ALL, handle_message)
    ]
    
    for handler in handlers:
        application.add_handler(handler)
    

    PrintLogOut("Бот запускается...")
    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES,
        close_loop=False
    )
    PrintLogOut("Бот запущен и готов к работе")

if __name__ == "__main__":
    main()