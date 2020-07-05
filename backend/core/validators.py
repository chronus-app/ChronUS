from django.core.exceptions import ValidationError


def validate_minutes(value):
    minutes = ['25', '50', '75']

    if not float(value).is_integer():
        decimal_digits = str(value).split('.')[1]

        if len(decimal_digits) == 1:
            decimal_digits += '0'

        if decimal_digits not in minutes:
            raise ValidationError(
            (f'{value} is not an allowed value'),
            params={'value': value},
            )

