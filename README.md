# Foodgram
### Описание
Продуктовый помощник - на этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Технологии
* Python 3.9
* Django 4.2
* Django REST framework
* Postgres
* Docker
* Nginx
* Yandex.Cloud
* CI на GitHub Action

### Для локальной сборки

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:AlexBatanov/api_yamdb.git
```

Перейти в каталог
```
cd infra
```

создать .env
```
touch .env
```

Заполнить
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=namebd
POSTGRES_USER=user
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=secretkey django
```

Создание и запуск контейнера
```
sudo docker compose up -d
```

Создать миграции
```
sudo docker compose exec backend python manage.py migrate
```

Создание суперюзера
```
sudo docker compose exec backend python manage.py createsuperuser
```

Собрать статику
```
sudo docker compose exec backend python manage.py collectstatic --noinput
```

Заполнить бд ингредиентами
```
sudo docker compose exec backend python manage.py loadingredients ingredients.csv
```

Проект будет доступен по адресу 
```
http://localhost/
```

В админ панели создать теги для успешного создания рецептов

### Доступ к проекту

http://158.160.67.200

админка
```
login -> admin
password -> admin
```

### Автор
[Alexandr](https://github.com/AlexBatanov)