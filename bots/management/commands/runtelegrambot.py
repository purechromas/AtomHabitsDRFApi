import telebot
from django.core.management.base import BaseCommand
from users.models import User
from config import settings

token = settings.TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(token=token)

chat_states = {}


class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        @bot.message_handler(commands=['start'])
        def start(chat):
            bot.send_message(
                chat.chat.id,
                f'Hello {chat.from_user.first_name} activate your own HabitBot with command "/bot"'
            )

        @bot.message_handler(commands=['bot'])
        def bot_registration(chat):
            chat_states[chat.chat.id] = 'waiting_for_email'
            bot.send_message(
                chat.chat.id,
                'Please write your email or type "exit" to finish'
            )

        @bot.message_handler(func=lambda message: message.chat.id in chat_states)
        def process_message(chat):
            chat_id = chat.chat.id
            message_text = chat.text
            state = chat_states.get(chat_id)

            if state == 'waiting_for_email':
                if message_text.lower() == 'exit':
                    bot.send_message(
                        chat_id,
                        'Exiting /bot command'
                    )
                    del chat_states[chat_id]
                else:
                    email = message_text
                    user = User.objects.filter(email=email).first()
                    if user:
                        user.telegram_chat_id = chat.chat.id
                        user.save()
                        bot.send_message(
                            chat_id,
                            'All done! We will notice you when it is time for the habit. Have a nice day!'
                        )
                        del chat_states[chat_id]
                    else:
                        bot.send_message(
                            chat_id,
                            'Try again, there is not that kind of email in our database or type "exit" to finish'
                        )

        bot.infinity_polling()
