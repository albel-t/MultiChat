import debug

debug.PrintLogOut("Чтение зависимостей")
subjection = {}
names = {}
active_chats = []
with open('subjection.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()  # Удаляем лишние пробелы и переносы строк
        if not line:  # Пропускаем пустые строки
            continue
        # Разделяем только по первому пробелу
        key, *values = line.split(maxsplit=1)  # maxsplit=1 — разделить только 1 раз
        subjection[key] = values[0] if values else ""  # Если есть значение — берём, иначе пустая строка

debug.PrintLogOut("Установка зависимостей")

bot_token = subjection["_bot_token"]
log_file_name = subjection["_log_file_name"]


active_chats.append(subjection["active_chats"])

names["Александр"] = subjection["Александр"]
names["ksaers"] = subjection["ksaers"]

account_password = subjection["account_password"]
debug_port = subjection["debug_port"]





