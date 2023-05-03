# Домашнее задание: 15 спринт.

### Описание:
Приложение для оценки и комментирования творческих произведений.

### Стек:
 - Django RF
 - Postgres
 - nginx

### Запуск:

 1. Файл `.env` необходимо создать в директории `~/infra/` 
 2. Укажите следующие параметры:
     - `POSTGRES_USER=<username>`
     - `POSTGRES_PASSWORD=<password>`
  
 3. Перейдите в директорию `~/infra/` и выполните команду `docker-compose up -d`
 4. Сделайте миграции:
	- `docker-compose exec web python manage.py makemigrations`
	- `docker-compose exec web python manage.py migrate`
Затем адаптируйте static командой:
	- `docker-compose exec web python manage.py collectstatic --no-input`

#### Проект доступен.
