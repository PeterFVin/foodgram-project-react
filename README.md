# Проект «Foodgram» V1.0

![Workflow Foodgram](https://github.com/PeterFVin/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## О проекте

Проект Foodgram - продуктовый помощник, сайт, на котором пользователи публикуют свои рецепты, подписываются друг на друга. Также можно создать свой избранный список любимых рецептов.
При помощи сервиса "Список покупок" пользователи могут выбрать определенные рецепты и скачать список продуктов для  приготовления этих рецептов.

### Использованные технологии: 

 - Docker
 - Python 3.11 
 - Django==3.2.16 
 - djangorestframework==3.12.4 
 - Nginx 
 - gunicorn
 - React

 ### Автор проекта:

Петр Виноградов, python plus, когорта 29+

### Как запустить проект: 

- В корневой папке проекта запустить Docker Compose

sudo docker compose -f docker-compose.production.yml up -d

- Выполнить миграции

sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate

- Наполнить базу данных ингредиентами

sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_db

- Наполнить базу данных тегами

sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_tags

- Собрать статику бэкенда

sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic

- Скопировать статику бэкенда в папку /backend_static/static/

sudo docker compose -f docker-compose.production.yml exec backend cp -r /collected_static/. /backend_static/static/

### В проекте нужен .env файл 
