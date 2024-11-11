# FastAPI-gRPC downloader
В данном репозитории представлен проект с реализацией протокола gRPC для обмена данными между клиентским приложением
(FastAPI) и серверным приложением.
Серверное приложение хранит и раздаёт файлы, на стороне клиента - роутинг и взаимодействие с сервером
(при помощи встроенного интерфейса - OpenAPI)

Для запуска проекта необходимо:
- склонировать репозиторий:
```commandline
git clone git@github.com:LeoNefesch/fastapi_grpc_downloader.git
```
- установить docker и docker-compose:
Инструкция для Linux (Если у Вас Windows, то потребуется установить wsl):
```commandline
sudo apt update
```
```commandline
sudo apt install docker.io
```
```commandline
sudo systemctl start docker
```
```commandline
sudo systemctl enable docker --now
```
```commandline
sudo curl -SL https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
```
```commandline
sudo chmod +x /usr/local/bin/docker-compose
```
Проверьте установку:
```commandline
sudo docker-compose --version
```

Перейти в корневую директорию:
```commandline
cd fastapi_grpc_downloader
```

Далее - инструкции по запуску проекта в docker compose и дальнейшей работе.
Сборка / персборка контейнеров:
```commandline
sudo docker-compose up -d
```
После запуска проекта в docker compose проверьте, запущены ли контейнеры:
```commandline
sudo docker-compose ps -a
```
Затем введите в адресной строке браузера `http://127.0.0.1:8000/docs` - 
должен отобразиться интерфейс OpenAPI.
При помощи метода POST загрузите на сервер файл со своего компьютера:
- нажмите `Try it out`;
- выберите файл со своего компьюьтера, а также введите название файла вместе с расширением (.txt, .png и т.д.)
в поле filename;
- нажмите `Execute` - файл загружен на сервер.
При помощи метода GET скачайте файл с сервера на свой компьютер:
- нажмите `Try it out`;
- введите название файла вместе с расширением (.txt, .png и т.д.) в поле filename;
- нажмите `Execute`;
- пролистайте страницу немного вниз и нажмите на ссылку для скачивания `Download file` -
файл скачан в папку `Загрузки` на вашем компьютере.


Остановка и удаление контейнера (если в docker-compose внесены изменения):
```commandline
sudo docker-compose down
```

Для очистки внутреннего хранилища файлов получите название тома (где хранятся скачанные данные) через команду ниже:
```commandline
sudo docker volume ls
```
Удалить том (только после того, как остановите контейнеры):
```commandline
sudo docker volume rm <имя тома>
```
