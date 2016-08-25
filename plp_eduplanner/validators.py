from django.core.validators import MaxValueValidator, MinValueValidator

RATE_VALIDATORS = [
    MaxValueValidator(3),
    MinValueValidator(1)
]
