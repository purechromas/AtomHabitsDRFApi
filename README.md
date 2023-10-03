# AtomHabit RESTful API

Welcome to the AtomHabit Django RESTful API!

## Technologies Used

This project utilizes the following technologies and frameworks:

- Django
- Django Rest Framework (DRF)
- PostgreSQL
- Celery
- Celery Beat
- Redis
- Telegram Bot API
- Unit Testing
- Swagger
- CORS
- JWT AUTH

Enjoy tracking your habits and achieving your goals!

## Getting Started

Follow these steps to run the API on your local machine:

1. **Clone the Repository**: Begin by cloning this repository to your local environment.

    ```bash
    git clone https://github.com/yourusername/atomic-habit-api.git
    cd atomic-habit-api
    ```

2. **Configure Your Environment**: Create a `.env` file by copying the provided `.env-example`. This file should contain sensitive information such as database settings, email configurations, and any required API keys.

    ```bash
    .env-example -> .env
    ```

    Edit the `.env` file and fill in the necessary values.

3. **Database Migration**: Migrate the database to create the required tables.

    ```bash
    ./manage.py migrate
    ```

4. **Start the Telegram Bot**: Run the Telegram bot to receive habit reminders. You can access the Telegram bot [here](https://t.me/AtomHabitsBot).

    ```bash
    ./manage.py runtelegrambot
    ```

5. **Start Celery and Celery Beat**: Start Celery and Celery Beat for background task processing.

    ```bash
    celery -A yourprojectname worker --loglevel=info
    celery -A yourprojectname beat --loglevel=info
    ```

    Replace `yourprojectname` with the name of your Django project.

6. **Start the Server**: Finally, start the development server.

    ```bash
    ./manage.py runserver
    ```

    You can now access the API at `http://localhost:8000` in your web browser or use a tool like Postman to interact with it.


