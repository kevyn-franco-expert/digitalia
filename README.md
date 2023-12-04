# Project Name

Digitalia Project.

## Requirements

- Python 3.9
- Docker

## Local Setup

These instructions will help you get a copy of the project up and running on your local machine for development and
testing purposes.

1. **Environment Setup**: Ensure you have Python and Django installed. It's recommended to use a virtual environment.

2. **Clone the Repository**: Clone this repository to your local machine.

    ```bash
    git clone ''
    ```

3. **Install Dependencies**: Install all the required dependencies.

    ```bash
    pip install -r requirements.txt
    ```

4. **Database Migrations**: Run the migrations to set up your database.

    ```bash
    python manage.py migrate
    ```

5. **Create a Superuser**: Create a superuser to access the admin panel.

    ```bash
    python manage.py createsuperuser
    ```

6. **Collect Static Files**: Collect all the necessary static files.

    ```bash
    python manage.py collectstatic
    ```

7. **Set Environment Variables**: Set the necessary environment variables.

    ```bash
    export DJANGO_SETTINGS_MODULE=ChallengeDigitalia.settings
    ```

8. **Run the Development Server**: Start the development server.

    ```bash
    uvicorn ChallengeDigitalia.asgi:application --port 8000 --reload
    ```

   You can now access the application at `http://localhost:8000`.

## Deployment with Docker

To deploy this project using Docker, follow these steps:

1. **Build and Run with Docker Compose**:

    ```bash
    docker-compose up --build
    ```

   This will build the image and run the container.

2. Access the application at `http://localhost:8000`.

## License

Information about the license.

This addition informs users where to find the tests and how to run them, integrating seamlessly with the rest of your
project's setup instructions.
