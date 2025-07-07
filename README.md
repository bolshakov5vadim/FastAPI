Скачать все это в папку.
В e.env записать адрес БД

Затем

cd <ВАША_ПАПКА>

sudo docker build . -t fastapi_app

sudo docker run -p 8000:8000 fastapi_app

Теперь у вас API для базы данных!
