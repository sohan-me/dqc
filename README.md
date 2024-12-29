# Daily Quote Companion
Daily Quote Companion is a Django-based web application that delivers personalized motivational quotes to users based on their preferences with scrolling feed. 
Leveraging AI, the app generates unique quotes in categories such as inspiration, humor, and success, and sends them to users daily via email. Users can provide
feedback on the quotes to improve future suggestions, fostering a tailored motivational journey.

## Features

- **Django** - A powerful Python web framework for rapid web development.
- **Celery** - A distributed task queue for handling background tasks asynchronously.
- **Redis** - An in-memory data structure store used as a message broker for Celery.
- **Celery Beat** - A scheduler for Celery to run tasks at regular intervals.
- **Docker** - Simplifies environment setup by using containers.
- **Openai** - To generate quotes based on user preferences and goals.
- **Docker Compose** - Orchestrates multiple services like Django, Celery, Redis, and Celery Beat.

## Prerequisites

Make sure you have Docker and Docker Compose installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to get the project up and running.

### 1. Clone the Repository

```bash
git clone https://github.com/sohan-me/dqc
cd dqc
```
## Run the Project

Once you've set up and built the project, follow these steps to run it and ensure everything is working as expected.

### 2. Start the Docker Containers

Use the following command to start all services in the background:

```bash
docker-compose up -d --build
```

### 3. API endpoints Docs
After running the containers visit the following url to read and view api endpoints documentations
- [SwaggerUI](http://127.0.0.1:8000/api/schema/swagger-ui/#/)

