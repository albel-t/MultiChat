
import subjection
import os

def PrintLogOut(massage):
    print(massage)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(massage)
    

TOKEN = subjection.bot_token
LOG_FILE = subjection.log_file_name

def InitLogFile():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("=== Telegram Chat Bot ===\n\n")
        
                