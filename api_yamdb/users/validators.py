import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError('Этот ник зарезеривирован')
    pattern = re.compile(r'^[\w.@+-]+')
    if not pattern.match(value):
        raise ValidationError(
            'Можно использовать только цифры, буквы и символы @/./+/-/_'
        )
