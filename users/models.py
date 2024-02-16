from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Пользователь"""

    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='город', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активный')
    date_of_birth = models.DateField(verbose_name='дата_рождения', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
