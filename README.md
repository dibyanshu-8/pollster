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

* **Backend**: Django
* **Frontend**: HTML, CSS, Javascript
* **Database**: SQLite3
* **Web Server**: Gunicorn
* **Containerization**: Docker, Docker Compose

