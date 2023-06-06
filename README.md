# praktikum_new_diplom
### Для локальной сборки

cd infra
создать .env 
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=namebd
POSTGRES_USER=user
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=secretkey django
```
создание и запуск контейнера

```
sudo docker compose up -d
```

создать миграции

```
sudo docker compose exec backend python manage.py migrate
```

создание суперюзера

```
sudo docker compose exec backend python manage.py createsuperuser
```

собрать статику

```
sudo docker compose exec backend python manage.py collectstatic --noinput
```

заполнить бд ингредиентами

```
sudo docker compose exec backend python manage.py loadingredients ingredients.csv
```

проект будет доступен по адресу 

```
 http://localhost/
```

в админ панели создать теги для успешной регистрации рецептов

P.S.: редок после деплоя на боевой сервер переделается