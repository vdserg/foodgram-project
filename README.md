![Foodgram Workflow](https://github.com/vdserg/foodgram-project/workflows/Foodgram%20Workflow/badge.svg)
# foodgram-project

"Продуктовый помошник"

## Описание

Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Запуск (docker)

### Установка Docker
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop) 
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

### Запуск docker-compose
- Добавьте в файл `.env`'` переменные окружения для работы с базой данных:
```
POSTGRES_DB=foodgram # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```
- Запустите docker-compose командой `sudo docker-compose up -d` 
- Накатите миграции `sudo docker-compose exec web python manage.py migrate`
- Соберите статику командой `sudo docker-compose exec web python manage.py collectstatic --no-input`
- Создайте суперпользователя Django `sudo docker-compose exec web python manage.py createsuperuser --username admin --email 'admin@yamdb.com'`
- Чтобы загрузить список ингредиентов в БД используйте `docker-compose exec web python manage.py loaddata ingredients.json`