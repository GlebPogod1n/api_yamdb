from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    """Валидатор для определения года."""

    if not (0 < value <= timezone.now().year):
        raise ValidationError(
            '%(value)s год указан не корректно',
            params={'value': value},
        )
