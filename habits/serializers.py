from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    RewardOrPleasantHabit, TimeMaximum, RelatedHabitOnlyPleasantHabit, PleasantHabitNoRelatedHabitOrReward)


class HabitSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault(), required=False)

    class Meta:
        model = Habit
        fields = ('id', 'action', 'time', 'place', 'is_pleasant', 'frequency', 'time_complete',
                  'is_public', 'reward', 'related_habit', 'creator')
        read_only_fields = ('id', 'creator')
        optional_fields = ('is_public', 'reward', 'related_habit')
        validators = (
            RewardOrPleasantHabit(),
            TimeMaximum(time_complete='time_complete'),
            RelatedHabitOnlyPleasantHabit(related_habit='related_habit'),
            PleasantHabitNoRelatedHabitOrReward(),
        )
