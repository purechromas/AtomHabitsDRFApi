from rest_framework.serializers import ValidationError

from habits.models import Habit


class RewardOrPleasantHabit:
    def __call__(self, data):
        is_pleasant = data.get("is_pleasant")
        related_habit = data.get("related_habit")
        reward = data.get("reward")

        if not is_pleasant:
            if related_habit is None and reward is None:
                raise ValidationError("Provide either 'related_habit' or 'reward'")
            if related_habit is not None and reward is not None:
                raise ValidationError("Provide either 'related_habit' or 'reward' not both")


class TimeMaximum:
    def __init__(self, time_complete):
        self.time_complete = time_complete

    def __call__(self, data):
        time_complete = data.get(self.time_complete)

        if time_complete is None:
            raise ValidationError("Provide a 'time_complete'")

        if int(time_complete) > 120:
            raise ValidationError("Time for complete must be less then 120 seconds")


class RelatedHabitOnlyPleasantHabit:
    def __init__(self, related_habit):
        self.related_habit = related_habit

    def __call__(self, data):
        related_habit = data.get(self.related_habit)

        if related_habit is not None:
            try:
                habit = Habit.objects.get(id=related_habit.id)
            except Habit.DoesNotExist:
                raise ValidationError("There is no habit with this ID")
            else:
                if not habit.is_pleasant:
                    raise ValidationError("The selected habit is not pleasant")



class PleasantHabitNoRelatedHabitOrReward:
    def __call__(self, data):
        is_pleasant = data.get("is_pleasant")

        if is_pleasant:
            reward = data.get("reward")
            related_habit = data.get("related_habit")

            if reward is not None or related_habit is not None:
                raise ValidationError("You can't add reward or related habit on pleasant habit")
