from rest_framework import serializers

from habits.models import Habit
from habits.validators import TimeToExecuteValidator, RelatedHabitAwardValidator, \
    RelatedHabitSignPleasantHabitValidator, SignPleasantHabitHabitValidator


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
        default_validators = [TimeToExecuteValidator(), RelatedHabitAwardValidator(),
                              RelatedHabitSignPleasantHabitValidator(), SignPleasantHabitHabitValidator()]
