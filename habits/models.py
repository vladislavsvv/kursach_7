from datetime import datetime
from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}

class Habit(models.Model):
    """Привычка"""

    place = models.CharField(max_length=300, verbose_name='Место, выполнения привычки')
    time = models.DateTimeField(default=datetime.now, verbose_name='Время, выполнения привычки')
    action = models.CharField(max_length=300, verbose_name='Действие')

    sign_pleasant_habit = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Связанная привычка')
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name='Периодичность, выполнения привычки')
    award = models.CharField(max_length=500, verbose_name='Вознаграждение')
    time_to_execute = models.PositiveSmallIntegerField(verbose_name='Время на выполнение привычки')
    public = models.BooleanField(default=False, verbose_name='Признак публичности')

    client = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'Я буду{self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
