from django.core.exceptions import ValidationError
import re


def phone_validator(value):
    pattern = re.compile(r'^(\+7|8)\d{10}$')
    if not pattern.match(value):
        raise ValidationError(
            f'Номер телефона должен быть в одном из следующих форматов: +79999999999 or 89999999999'
        )
    return value
