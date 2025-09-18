# Pollster: A Django Polling Application

Pollster is a functional web application built with the Django framework that allows users to create, manage, and vote on polls. The project is fully containerized using Docker and Docker Compose, ensuring a consistent and easy-to-manage development environment.

## Features

* **User Authentication**: Full user registration, login, and logout capabilities.
* **Poll Management (CRUD)**: Users can create, view, update, and delete polls and their corresponding choices.
* **Ownership**: Polls are associated with the user who created them, and only the owner can modify or delete their own polls.
* **Permission System**: Creating polls is restricted to users with the appropriate permissions, managed through the Django admin panel.
* **Voting**: Authenticated users can cast votes on active polls.
* **Search and Sort**: The main list of polls can be searched by title and sorted by name, date, or total vote count.
* **Pagination**: Poll lists are paginated to handle larger sets of data efficiently.

## Technology Stack

* **Backend**: Python, Django
* **Frontend**: HTML, CSS, Bootstrap
* **Database**: SQLite3
* **Web Server**: Gunicorn
* **Containerization**: Docker, Docker Compose

## Local Setup Instructions

Follow these steps to get a local copy of the project up and running.

### Prerequisites

* Git
* Docker and Docker Compose

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/dibyanshu-8/pollster.git](https://github.com/dibyanshu-8/pollster.git)
    ```

2.  **Navigate to the project directory:**
    ```sh
    cd pollster
    ```

3.  **Build and run the Docker containers:**
    This command builds the Django image from the `Dockerfile` and starts the application.
    ```sh
    docker-compose up --build
    ```

4.  **Apply database migrations:**
    In a **new terminal window**, run the following command to create the necessary database tables inside the running container.
    ```sh
    docker-compose exec web python manage.py migrate
    ```

5.  **Create a superuser:**
    To use the Django admin panel, create an administrator account.
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```
    Follow the prompts to set your username, email, and password.

6.  **Access the application:**
    The application is now running. You can access it in your browser at the following URLs:
    * **Homepage**: [http://localhost:8000/](http://localhost:8000/)
    * **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/)