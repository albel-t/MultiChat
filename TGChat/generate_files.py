import subjection
import debug

path = [
    ['server.properties', 
        ["enable-rcon=true",
        "rcon.password="+subjection.account_password,
        "rcon.port="+subjection.debug_port]]
    
    
    ]



print(f"введите цифру соответствующую требуемому файлу")
for i in range(0, len(path)):
    print(f"{i}: {path[i][0]}")
path_id = int(input())
with open(path[path_id][0], 'w', encoding='utf-8') as file:
    file.writelines(line + '\n' for line in path[path_id][1]) 
debug.PrintLogOut(f"Файл {path[path_id][0]} создан!")