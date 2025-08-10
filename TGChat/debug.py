
import subjection
import os

LOG_FILE = subjection.log_file_name

def PrintLogOut(massage):
    print(massage)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(massage)
    
def InitLogFile():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("=== Telegram Chat Bot ===\n\n")
        
                