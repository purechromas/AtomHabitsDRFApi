from datetime import datetime

import telebot
from celery import shared_task

from config import settings
from habits.models import Habit
from users.models import User

telegram_message = """
Hey there! 🕒 It's time for your habit reminder:
You have a {habit.action} to do.
Location: {habit.place}
                
Time to get it done! 💪😄
"""


@shared_task
def send_habit_telegram_notification():
    bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

    current_time = datetime.now().time()

    users = User.objects.filter(telegram_chat_id__isnull=False)

    for user in users:
        habits = Habit.objects.filter(creator=user)

        for habit in habits:
            if habit.time.hour == current_time.hour and habit.time.minute == current_time.minute:
                message = telegram_message.format(habit.action, habit.place)

                bot.send_message(user.telegram_chat_id, message)
