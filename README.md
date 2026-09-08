# Animal Shelter & Adoption Management System

A team project for managing animal shelter operations, adoptions, appointments, medical records, and user roles.

## Tech Stack

- Python 3.12
- Django 6.1
- MongoDB 8.0
- Docker
- Docker Compose

## Prerequisites

Install:

- Git
- Docker
- Docker Compose

## Setup

Clone the repository:

```bash
git clone git@github.com:Tmonstah/animal-shelter-management-system.git

Enter the project directory:
cd animal-shelter-management-system

Build and start the containers:
docker compose up --build

Open the application on your Web Browser at:
http://localhost:8000

Stop the Project
docker compose down


Run Django Commands:
docker compose exec web python manage.py migrate

WorkFlow to add personal or assigned feature
---------------------------------------------

Create a new branch before working on a feature:
git checkout -b feature/your-feature-name

Commit your work:

git add .
git commit -m "Describe your change"

Push your branch:
git push -u origin feature/your-feature-name

Then create a Pull Request on GitHub.
