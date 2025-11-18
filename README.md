# Приложение для поиска интересных мест в Москве

Карта с маркерами интересных мест с описанием и фото

<img width="1291" height="641" alt="изображение" src="https://github.com/user-attachments/assets/9e94a684-3141-463e-ab2c-8f15afc2a3bb" />


## Запуск

Для запуска сайта вам понадобится Python 3.12.

Скачайте код с GitHub. Установите зависимости:

```sh
pip install -r requirements.txt
```

Создайте базу данных SQLite

```sh
python3 manage.py migrate
```

Запустите разработческий сервер(127.0.0.1:8000)

```
python3 manage.py runserver
```

Для доступа к админке(127.0.0.1:8000/admin)

```
python3 manage.py createsuperuser
```

Для наполнения базы данных через консоль используются json файлы вида:

<img width="1273" height="261" alt="изображение" src="https://github.com/user-attachments/assets/7b3582d0-971f-45cf-a005-b915b77a0dcd" />

и команда

```
python3 manage.py load_place path/to/filename.json
```
с необязательными атрибутами *--update* для обновления существующей записи и *--update  --clear-images* для удаления ранее загруженных изображений.


## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны переменные:
- `DEBUG` — дебаг-режим. Поставьте `True`, чтобы увидеть отладочную информацию в случае ошибки.
- `SECRET_KEY` — секретный ключ проекта.
- `DATABASE_FILEPATH` — полный путь к файлу базы данных SQLite, например: `/home/user/base.sqlite3`
- `ALLOWED_HOSTS` — см [документацию Django](https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts)
- `STATIC_URL`, `STATIC_ROOT`, `MEDIA_URL`, `MEDIA_ROOT` — статические файлы и медиа.


## Цели проекта

Код написан в учебных целях — для курса по Python и веб-разработке на сайте [Devman](https://dvmn.org).

