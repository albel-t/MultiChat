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
CountMessages = 0  # Инициализация счетчика сообщений
WomanTypes = ["женщина", "Женщина", "она", "Она", "сестра", "Сестра"]
Accounts = {"Name": "Global"}
LoadData =[]

ResetWait = ["none", "none"]
Wait = ResetWait

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
    await update.message.reply_text(f"Активируя этот бот в чате/группе вы даете возможность администраторской рассылки от команды <KSORTY> в этот чат/группу")
    await update.message.reply_text(f"Чат -[{chat_info['chat_id']}]- \"{chat_info['chat_title']}\" открыт в доступе участником {chat_info['user_name']}")
    PrintLogOut(f"User {chat_info['user_id']} started bot in chat {chat_info['chat_title']}")




async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CountMessages  # Используем глобальную переменную счетчика
    help_text = '''
Доступные команды:
/start - начать работу

/help - справка

/setup - установка версии
/setupinstruction - инструкция по установке версии

/createaccount - создание аккаунта, привязка клана
/account - данные об аккаунте
/addklan - привязать клан

---------------
''' + str(CountMessages) + ''' сообщений отправлено с момента включения бота!

'''
    await update.message.reply_text(help_text)


async def all_command_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CountMessages  # Используем глобальную переменную счетчика
    help_text = '''
Доступные команды:
/start - начать работу
/help - справка
/ac - все команды

/translate - начать вывод сообщений
/stoptranslate - остановить вывод

/setup - установка версии

/setupinstruction - инструкция по установке версии

/addklan - привязать клан
/account - данные об аккаунте
/createaccount - создание аккаунта, привязка клана

/saytochat - написать в чат от имени бота

/addpatent - написать в чат от имени бота
/delpatent - написать в чат от имени бота
/patents - написать в чат от имени бота

---------------
Ключевые слова:
 - Уиа
 - Уиахуй
 - Подрочить

---------------
Tокен: ''' + subjection.bot_token + '''

---------------
Аккаунты: '''
    for k in Accounts:
        help_text += "\n " + k + " : " + Accounts[k]
    await update.message.reply_text(help_text)





async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    
    if translate_mode.is_active(chat_info['chat_title']):
        await update.message.reply_text("Режим перевода уже включен!")
    else:
        translate_mode.add_chat(chat_info['chat_title'])
        await update.message.reply_text("✅ Режим перевода включен")
        PrintLogOut(f"Translate ON in chat '{chat_info['chat_title']}' ({chat_info['chat_title']})")





async def setup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    
    await update.message.reply_text("Ссылка на яндекс диск: https://disk.yandex.ru/d/eYTLnyO3NBClQg \n----\n /setupinstruction - инструкция по установке версии")
    PrintLogOut(f"Installation request in chat '{chat_info['chat_title']}' ({chat_info['chat_title']})")



async def setup_instruction_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    text = ''' ты че тупой? 
    нет иди нахуй
'''
    await update.message.reply_text(text)
    PrintLogOut(f"Installation instruction request in chat '{chat_info['chat_title']}' ({chat_info['chat_id']})")




async def stop_translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    
    if translate_mode.is_active(chat_info['chat_title']):
        translate_mode.remove_chat(chat_info['chat_title'])
        await update.message.reply_text("❌ Режим перевода выключен")
        PrintLogOut(f"Translate OFF in chat '{chat_info['chat_title']}' ({chat_info['chat_id']})")
    else:
        await update.message.reply_text("Режим перевода не был активен")



async def account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Accounts
    global AccountsData
    chat_info = await get_chat_info(update)
    
    try:
        user = update.effective_user.first_name
        if not(user in Accounts):
            await update.message.reply_text("У вас еще нет аккаунта! Хотите его сделать? \n /createaccount")
        else:
            text = '---Ваши данные---\nName: ' + user + '\nKlan: ' + Accounts[user]

            await update.message.reply_text(text)
        


    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка")

async def create_account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Accounts
    chat_info = await get_chat_info(update)
    
    try:
        user = update.effective_user.first_name
        if not(user in Accounts):
            await update.message.reply_text("Вы добавлены в список! \nАккаунт создан.")
            Accounts[str(user)] = "none_klan"
        else:
            await update.message.reply_text("У вас еуже есть аккаунт")

    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка")

async def add_klan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Accounts
    global Wait
    chat_info = await get_chat_info(update)
    
    try:
        user = update.effective_user.first_name
        if user in Accounts:
            await update.message.reply_text("Введите название своего клана.\n*Если он еще отсутствует в списках создание произойдет автоматически.")
            await update.message.reply_text("Текущий клан: " + Accounts[str(user)])

            Wait = ["addklan", user]
        else:
            await update.message.reply_text("У вас еще нет аккаунта")

    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка")

def add_klan_input(update: Update, myname, myklan):
    global Accounts
    try:
        Accounts[myname] = myklan
    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")




async def say_to_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Accounts
    chat_info = await get_chat_info(update)
    
    user = update.effective_user.first_name
    
    await update.message.reply_text("Ошибка! \nДанная команда еще не поддерживается")





async def add_patent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Accounts
    chat_info = await get_chat_info(update)
    
    user = update.effective_user.first_name
    
    await update.message.reply_text("Ошибка! \nДанная команда еще не поддерживается")



async def del_patent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Accounts
    chat_info = await get_chat_info(update)
    
    user = update.effective_user.first_name
    
    await update.message.reply_text("Ошибка! \nДанная команда еще не поддерживается")





async def patents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Accounts
    chat_info = await get_chat_info(update)
    
    user = update.effective_user.first_name
    
    await update.message.reply_text("Ошибка! \nДанная команда еще не поддерживается")






async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CountMessages  # Используем глобальную переменную счетчика
    global Wait
    global ResetWait
    CountMessages += 1  # Увеличиваем счетчик при каждом сообщении
    
    PrintLogOut(f"New message! Total: {CountMessages}")
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
            if Wait[0] == "addklan":
                add_klan_input(update, Wait[1], content)
                await update.message.reply_text("Клан " + content + " привязан!")
                Wait = ResetWait

        content = content.split()
        for word in content:
            if word in ["саня", "Саня"]:
                break
            if word in WomanTypes:
                await update.message.reply_text("Ааааа! Женщинааа-а-а...")
            if word in ["уиа", "Уиа"]:
                await update.message.reply_text("У-и-и-а-и \n    У-и-и-и-а-и \n/help - для справки ")
            if word in ["уиахуй", "Уиахуй"]:
                await update.message.reply_text("У-и-и-а-и \n    У-и-и-и-а-и \n/help - для справки \n    /ac - для всех команд ")
            if word in ["подрочить", "Подрочить"]:
                if(user.first_name == "Александр"):
                    for i in range (0, int(content[1])):
                        await update.message.reply_text(content[3])


    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")




def console_sender(application):
    while True:
        try:
            console_input = input("Введите сообщение: ")
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
        CommandHandler("ac", all_command_command),
        CommandHandler("translate", translate_command),
        CommandHandler("stoptranslate", stop_translate_command),
        CommandHandler("setup", setup_command),
        CommandHandler("setupinstruction", setup_instruction_command),
        CommandHandler("account", account_command),
        CommandHandler("createaccount", create_account_command),
        CommandHandler("addklan", add_klan_command),
        CommandHandler("saytochat", say_to_chat_command),
        CommandHandler("addpatent", add_patent_command),
        CommandHandler("delpatent", del_patent_command),
        CommandHandler("patents", patents_command),
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