from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly

from habits.models import Habit
from habits.serliazers import HabitSerializer
from users.permissions import UserIsStaff
from .tasks import send_notification


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        related_habit = None
        new_habit = serializer.save(related_habit=related_habit, client=self.request.user)
        send_notification.delay(new_habit.id)  # вызов отложенной задачи с передачей параметра


class HabitListAPIView(generics.ListAPIView):
    """Список публичных привычек"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = PageNumberPagination


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Редактирование привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [UserIsStaff]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки"""

    queryset = Habit.objects.all()
    permission_classes = [UserIsStaff]


class ClientHabitListAPIView(generics.ListAPIView):
    """Список привычек текущего пользователя с пагинацией"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        client = self.request.user
        return Habit.objects.filter(client=client)
