import csv
import logging
import os

from django.core.management.base import BaseCommand
from django.db import DatabaseError, IntegrityError

from api_yamdb.settings import BASE_DIR
from reviews.models import (Title,
                            Review,
                            Comment,
                            Category,
                            User,
                            Genre)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
logger.addHandler(sh)

PATH = os.path.join(BASE_DIR, 'static/data/')

FILE_FUNC = {
    'users': [User, 'users.csv'],
    'genre': [Genre, 'genre.csv'],
    'category': [Category, 'category.csv'],
    'titles': [Title, 'titles.csv'],
    'genre_title': [Title.genre.through, 'genre_title.csv'],
    'review': [Review, 'review.csv'],
    'comments': [Comment, 'comments.csv']
}

REPLACE_VALUE = {
    'author': 'author_id',
    'category': 'category_id',
}


def open_csv(file, model):
    try:
        with open(f'{PATH + file}', 'r', encoding='utf-8') as r_file:
            reader = csv.DictReader(r_file, delimiter=',')
            create_obj(reader, model)
    except FileNotFoundError:
        logger.error(f'- Ошибка | {file} | Файл не найден.')


def create_obj(reader, model):
    try:
        if model == Title.genre.through:
            objects = [model(title_id=i['title_id'], genre_id=i['genre_id'])
                       for i in reader]
            model.objects.bulk_create(objects)
        else:
            model.objects.bulk_create(
                [model(**{REPLACE_VALUE.get(k, k): v for k, v
                          in row.items()}) for row
                 in reader]
            )
    except IntegrityError:
        logger.error(f'- Ошибка | {model.__name__} | '
                     f'Проверьте уникальность полей '
                     f'модели.')
    except DatabaseError as er:
        logger.error(f'- Ошибка | {model.__name__} | {er}.')
    else:
        logger.info(f'+ Успех | {model.__name__} | '
                    f'Записей добавлено: {reader.line_num - 1}')


class Command(BaseCommand):
    help = (f'Загружает данные из csv таблицы по адресу "{PATH}" '
            'в sqlite базу проекта Django, перед использованием,'
            'необходимо описать модели и сделать миграции.')

    def add_arguments(self, parser):
        parser.add_argument('-p', '--prefix', type=str,
                            help='Имя файла (без расширения).', )

    def handle(self, *args, **options):
        prefix = options.get('prefix')
        if prefix:
            try:
                model, file = FILE_FUNC.get(prefix)
                open_csv(file, model)
            except TypeError:
                logger.error(
                    f'- Ошибка | Файл "{prefix}.csv" не найден в {PATH}.'
                )
        else:
            for model, file in FILE_FUNC.values():
                open_csv(file, model)
