from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import NULLABLE, User


class Habit(models.Model):
    class Frequency(models.TextChoices):
        DAILY = ('daily', _('Daily'))
        WEEKLY = ('weekly', _('Weekly'))
        MONTHLY = ('monthly', _('Monthly'))

    action = models.CharField(_('Action'), max_length=255)
    time = models.TimeField(_('Time'), db_index=True)  # In what time we will make the habit
    place = models.CharField(_('Place'), max_length=255)
    is_pleasant = models.BooleanField(_('Is pleasant'))
    frequency = models.CharField(
        _('Frequency'), choices=Frequency.choices, default=Frequency.DAILY, max_length=10
    )
    time_complete = models.PositiveIntegerField(_('Time complete'))  # How much time we need for the habit
    is_public = models.BooleanField(_('Is public'), default=True)

    reward = models.CharField(_('Reward'), max_length=255, **NULLABLE)  # reward or pleasant_habit
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE,  related_name='related_habits', **NULLABLE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')


    def __str__(self):
        return f'HABIT: {self.action} - TIME: {self.time} - PLACE: {self.place}'

    class Meta:
        verbose_name = _('Habit')
        verbose_name_plural = _('Habits')
