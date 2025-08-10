# Клонирование репозитория
В папке с проектами открыть командную строку (GitBash), ввести команду:
```bash
git clone https://github.com/albel-t/TGBotPrint.git
```
# Зависимости
Для логирования чата:
```bash
pip install python-telegram-bot
```
Для вывода в чате сервера:
```bash
pip install mcrcon
```
Скопировать "server.properties" в папку сервера
```json
enable-rcon=true
rcon.password=$BS#4xMgaFqH@7y - пароль без ковычек
rcon.port=25575 - порт должен совпадать с портом в коде
```
### Вспомогательные файлы
в зависимостях "subjection.txt" указать нужные правки;
в программе "generate_files.py" можно создать требуемый файл зсново по новым зависимостям
# Запуск
### Отладка
Открыть vs code в папке с решением, установить расширения для питона, запустить "main.py"
