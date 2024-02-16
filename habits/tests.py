# from django_filters.compat import TestCase
from django.test import TestCase
from users.models import User
from rest_framework import status, serializers
from rest_framework.test import APITestCase, APIClient

from .models import Habit
from .validators import TimeToExecuteValidator, RelatedHabitAwardValidator, RelatedHabitSignPleasantHabitValidator, \
    SignPleasantHabitHabitValidator, PeriodicityValidator


class HabitsHabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='sdk@mail.ru', password='zxc123zxc123', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            place="test",
            time="2023-12-12T20:14:07.295779+03:00",
            action="бег",
            sign_pleasant_habit=True,
            periodicity=7,
            award="здоровье",
            time_to_execute=120,
            public=True
        )

    def test_create_habit(self):
        """Тестирование создание привычки"""

        response = self.client.post(
            path='/habit/create/',
            data={
                "place": "test",
                "time": "2023-12-13T19:34:20.134737+03:00",
                "action": "бег",
                "sign_pleasant_habit": True,
                "periodicity": 7,
                "award": "здоровье",
                "time_to_execute": 120,
                "public": True,
            }
        )

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # print(response.json())

        self.assertEqual(
            response.json(),
            {
                "id": 3,
                "place": "test",
                "time": "2023-12-13T19:34:20.134737+03:00",
                "action": "бег",
                "sign_pleasant_habit": True,
                "periodicity": 7,
                "award": "здоровье",
                "time_to_execute": 120,
                "public": True,
                "related_habit": None,
                "client": 2
            }
        )

    def test_list_habit(self):
        """Тестирование публичных привычек"""

        response = self.client.get(path='/habit/')

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # print(response.json())

        self.assertEqual(
            response.json(),
            [
                {

                    "id": 5,
                    "place": "test",
                    "time": "2023-12-12T20:14:07.295779+03:00",
                    "action": "бег",
                    "sign_pleasant_habit": True,
                    "periodicity": 7,
                    "award": "здоровье",
                    "time_to_execute": 120,
                    "public": True,
                    "related_habit": None,
                    "client": None
                }
            ]
        )

    def test_update_habit(self):
        """Тестирование редактирование привычки"""

        data = {
            "place": "test2",
        }

        response = self.client.patch(
            f'/habit/update/{self.habit.id}/',
            data=data
        )

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # print(response)

        self.assertEqual(
            response.json(),
            {
                "id": self.habit.id,
                "place": "test2",
                "time": "2023-12-12T20:14:07.295779+03:00",
                "action": "бег",
                "sign_pleasant_habit": True,
                "periodicity": 7,
                "award": "здоровье",
                "time_to_execute": 120,
                "public": True,
                "related_habit": None,
                "client": None
            }
        )

    def test_destroy_habit(self):
        """Тестирование удаление привычки"""

        response = self.client.delete(
            f'/habit/delete/{self.habit.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_client_list_habit(self):
        """Тестирование списка привычек текущего пользователя"""

        response = self.client.get(path='/user-habit/')

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # print(response.json())

        expected_data = []

        self.assertEqual(response.json(), expected_data)


class ValidatorsTestCase(TestCase):

    def test_time_to_execute_validator(self):
        """Тестирование время выполнения привычки"""

        validator = TimeToExecuteValidator()
        self.assertTrue(validator.__call__(120))
        self.assertTrue(validator.__call__(100))
        self.assertFalse(validator.__call__(121))

    def test_related_habit_award_validator(self):
        """Тестирование исключение одновременного выбора связанной привычки и указания вознаграждения"""

        validator = RelatedHabitAwardValidator()
        attrs = {'related_habit': 1, 'award': 'здоровье'}
        with self.assertRaises(serializers.ValidationError):
            validator.__call__(attrs)

        attrs = {'related_habit': None, 'award': 'здоровье'}
        self.assertEqual(validator.__call__(attrs), attrs)

    def test_related_habit_with_pleasant_habit(self):
        """
        Тестирование на связанные привычки.
        Валидатор должен пройти если связанная привычка имеет приятный характер.
        """

        validator = RelatedHabitSignPleasantHabitValidator()
        attrs = {'related_habit': {'sign_pleasant_habit': True}}
        result = validator.__call__(attrs)
        self.assertEqual(result, attrs)

    def test_related_habit_without_pleasant_habit(self):
        """
        Тестирование на связанные привычки.
        Валидатор должен вызвать ошибку, если связанная привычка не является приятной.
        """

        validator = RelatedHabitSignPleasantHabitValidator()
        attrs = {'related_habit': {'sign_pleasant_habit': False}}
        with self.assertRaises(serializers.ValidationError):
            validator.__call__(attrs)

    def test_sign_pleasant_habit_without_award_and_related_habit(self):
        """
        Тестирование валидатора приятной привычки.
        Валидатор должен пройти, если у приятной привычки нет награды и связанные привычки.
        """

        validator = SignPleasantHabitHabitValidator()
        attrs = {'sign_pleasant_habit': True, 'award': None, 'related_habit': None}
        result = validator.__call__(attrs)
        self.assertEqual(result, attrs)

    def test_sign_pleasant_habit_with_award(self):
        """
        Тестирование валидатора приятной привычки
        Валидатор должен вызвать ошибку, если у приятной привычки есть награда.
        """

        validator = SignPleasantHabitHabitValidator()
        attrs = {'sign_pleasant_habit': True, 'award': 'some award', 'related_habit': None}
        with self.assertRaises(serializers.ValidationError):
            validator.__call__(attrs)

    def test_sign_pleasant_habit_with_related_habit(self):
        """
        Тестирование валидатора приятной привычки
        Валидатор должен вызвать ошибку, если у приятной привычки есть связанная приятная привычка.
        """

        validator = SignPleasantHabitHabitValidator()
        attrs = {'sign_pleasant_habit': True, 'award': None, 'related_habit': {'sign_pleasant_habit': True}}
        with self.assertRaises(serializers.ValidationError):
            validator.__call__(attrs)

    def test_periodicity_greater_than_7(self):
        """
        Тестирование валидатора периодичности привычки.
        Валидатор должен вызвать ошибку, если периодичность больше 7 дней.
        """

        validator = PeriodicityValidator()
        attrs = {'periodicity': 10}
        with self.assertRaises(serializers.ValidationError):
            validator.__call__(attrs)

    def test_periodicity_equal_to_7(self):
        """
        Тестирование валидатора периодичности привычки.
        Валидатор должен пройти, если периодичность равна 7 дням.
        """

        validator = PeriodicityValidator()
        attrs = {'periodicity': 7}
        result = validator.__call__(attrs)
        self.assertEqual(result, attrs)

    def test_periodicity_less_than_7(self):
        """
        Тестирование валидатора периодичности привычки.
        Валидатор должен пройти, если периодичность менее 7 дней.
        """

        validator = PeriodicityValidator()
        attrs = {'periodicity': 5}
        result = validator.__call__(attrs)
        self.assertEqual(result, attrs)
