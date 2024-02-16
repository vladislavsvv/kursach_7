from django.core.management import BaseCommand

from users.services import MyBot


class Command(BaseCommand):

    def handle(self, *args, **options):
        my_bot = MyBot()
        my_bot.send_message('Прошло больше 7 дней. Вы давно не выполняли привычку. '
                            'Нельзя выполнять привычку реже, чем 1 раз в 7 дней!')
