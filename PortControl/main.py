import socket
import struct

def send_rcon_command(host, port, password, command):
    try:
        # Создаем подключение
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Формируем пакет аутентификации
        auth_packet = (
            struct.pack("<ii", 0, 3) +  # ID запроса (0) и тип (3 = auth)
            password.encode("utf-8") + b"\x00\x00"
        )
        sock.send(auth_packet)
        
        # Проверяем ответ на аутентификацию
        auth_response = sock.recv(4096)
        if auth_response[4:8] != b"\x00\x00\x00\x00":
            print("Ошибка: Неверный RCON-пароль")
            return False
        
        # Формируем пакет команды
        cmd_packet = (
            struct.pack("<ii", 1, 2) +  # ID запроса (1) и тип (2 = command)
            command.encode("utf-8") + b"\x00\x00"
        )
        sock.send(cmd_packet)
        
        # Получаем ответ
        response = sock.recv(4096)
        print(f"Ответ сервера: {response[12:-2].decode('utf-8')}")
        
        sock.close()
        return True
        
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return False

# Настройки (замените на свои)
SERVER_IP = "78.132.204.46"
# SERVER_IP = "192.168.0.10"
RCON_PORT = 25575  # Стандартный порт RCON
RCON_PASSWORD = "$BS#4xMgaFqH@7y"

# Пример использования
if __name__ == "__main__":
    print("Отправка сообщений в Minecraft-чат")
    print("(Введите 'exit' для выхода)")
    
    while True:
        message = input("Ваше сообщение: ")
        if message.lower() == "exit":
            break
            
        # Отправляем команду say в чат
        command = f"say {message}"
        send_rcon_command(SERVER_IP, RCON_PORT, RCON_PASSWORD, command)