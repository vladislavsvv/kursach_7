from rest_framework import serializers


class TimeToExecuteValidator:
    """Время выполнения должно быть не больше 120 секунд."""

    def __call__(self, value: int) -> bool:
        if value <= 120:
            return True
        else:
            return False


class RelatedHabitAwardValidator:
    """Исключение одновременного выбора связанной привычки и указания вознаграждения."""

    def __call__(self, attrs):
        related_habit = attrs.get('related_habit')
        award = attrs.get('award')

        if related_habit and award:
            raise serializers.ValidationError("Выберите только связанную привычку или указание вознаграждения, "
                                              "но не оба")

        return attrs


class RelatedHabitSignPleasantHabitValidator:
    """В связанные привычки могут попадать только привычки с признаком приятной привычки."""

    def __call__(self, attrs):
        related_habit = attrs.get('related_habit', {})

        if related_habit and not related_habit.get('sign_pleasant_habit', False):
            raise serializers.ValidationError("Связанная привычка должна быть действительной приятной привычкой")

        return attrs


class SignPleasantHabitHabitValidator:
    """У приятной привычки не может быть вознаграждения или связанной привычки."""

    def __call__(self, attrs):
        sign_pleasant_habit = attrs.get('sign_pleasant_habit')
        award = attrs.get('award')
        related_habit = attrs.get('related_habit')

        if sign_pleasant_habit:
            if award:
                raise serializers.ValidationError("Приятной привычке нельзя указывать вознаграждение")

            if related_habit:
                raise serializers.ValidationError("Приятная привычка не может иметь связанную привычку")

        return attrs


class PeriodicityValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней."""

    def __call__(self, attrs):
        periodicity = attrs.get('periodicity')

        if periodicity > 7:
            raise serializers.ValidationError("Привычка не может выполняться реже, чем 1 раз в 7 дней")

        return attrs
