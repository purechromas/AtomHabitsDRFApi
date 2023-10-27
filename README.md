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

## Easy RUN by docker:

# Docker Image for Your Python Application

This Docker image is designed to run your Python application using Python 3.11 on a slim Debian-based image.

## Building the Docker Image

1. Make sure you have Docker installed on your system. If not, you can download and install it from the [Docker website](https://www.docker.com/get-started).

2. Clone the repository containing the Dockerfile and your application code if you haven't already.

3. Open a terminal and navigate to the directory where your Dockerfile is located.

4. **Configure Your Environment**: Create a `.env` file by copying the provided `.env-example`. This file should contain sensitive information such as database settings, email configurations, and any required API keys.

    ```bash
    .env-example -> .env
    ```

5. Build the Docker image using the following command:
   ```shell
   docker-compose build 
   docker-compose up


## Hard RUN

Follow these steps to run the API on your local machine:

1. **Clone the Repository**: Begin by cloning this repository to your local environment.

    ```bash
    git clone https://github.com/yourusername/atomic-habit-api.git
    cd atomic-habit-api
    ```

2. **Create a Virtual Environment**: Before configuring the environment, it's a good practice to create a virtual environment using tools like Poetry or venv to isolate your project dependencies.

3. **Configure Your Environment**: Create a `.env` file by copying the provided `.env-example`. This file should contain sensitive information such as database settings, email configurations, and any required API keys.

    ```bash
    .env-example -> .env
    ```

    Edit the `.env` file and fill in the necessary values.

4. **Database Migration**: Migrate the database to create the required tables.

    ```bash
    ./manage.py migrate
    ```

5. **Start the Telegram Bot**: Run the Telegram bot to receive habit reminders. You can access the Telegram bot [here](https://t.me/AtomHabitsBot).

    ```bash
    ./manage.py runtelegrambot
    ```

6. **Start Celery and Celery Beat**: Start Celery and Celery Beat for background task processing.

    ```bash
    celery -A config worker --loglevel=info
    celery -A config beat --loglevel=info
    ```

    Replace `yourprojectname` with the name of your Django project.

7. **Start the Server**: Finally, start the development server.

    ```bash
    ./manage.py runserver
    ```

    You can now access the API at `http://localhost:8000` in your web browser or use a tool like Postman to interact with it.
