# Generated by Django 4.2.8 on 2023-12-13 16:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_alter_habit_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Время, выполнения привычки'),
        ),
    ]
