from celery import shared_task
from datetime import datetime, timedelta

from django.core.management import call_command

from habits.models import Habit


@shared_task
def schedule_reminder(habit_id):
    """Отложенная задача"""

    habit = Habit.objects.get(id=habit_id)

    if not habit.sign_pleasant_habit and habit.time <= datetime.now() - timedelta(days=7):
        if (datetime.now() - habit.time).days > 7:
            habit.sign_pleasant_habit = True
            habit.save()
            call_command('command')
