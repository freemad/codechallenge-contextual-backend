# Full Stack Coding Exercise Starter

## Scenario
You have been tasked with building a new event-based application that tracks the movement of a user's mouse cursor in a 
web browser, calculating the velocity of the mouse cursor and the distance it has travelled, and display the results to 
the user in near real-time on a chart.

### Requirements

1. The application must be built using Python and Django
2. Mouse move events must be captured in the browser and sent to the server using a REST API
3. Events must be stored in the database for later analysis
4. Processing of events must be done asynchronously using Celery tasks
5. The results must be displayed to the user in near real-time on a chart (this can be on the same page that captures 
   the mouse movements)

>**Note**
> 
> - You are free to use any additional libraries or frameworks you wish 
> - You may chart the results using any style of chart you see fit

## Getting started

A starter repository has been provided for you to get up and running quickly. It includes a basic Django app and is 
configured to use Celery for running asynchronous tasks. A Docker compose.yml file is provided to run the supporting
application services such as a PostgreSQL database and Redis message broker.

### Prerequisites

Before jumping in you'll need the following installed:

- [Python 3.11](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/install/)

### First run

With the prerequisites installed you'll now want to do the following:

Start the database and message broker services
```bash
docker compose -p fs_starter up
```

Install the Python dependencies and shell into the virtual environment
```bash
poetry install
poetry shell
```

Rename the `.env.example` file to `.env` and update the values as needed 
```bash
mv .env.example .env
`````

Run the Django migrations
```bash
python manage.py migrate
```

### Running the application

Start the server
```bash
python manage.py runserver
```

Start the Celery worker 
```bash
celery -A core worker -l debug
```

> **Note** 
> 
> Unlike the Django server, the Celery worker does not auto-reload when changes are made. You will need to
> restart the worker manually to pick up any changes.


## The Solution

The solution consists of 3 main parts:
- The Analytics app containing the models, serializers and views of the analytics data, which is PointerPositionEvent here.
- The Dashboard app consists of the models, serializers and views of the data which are related to the dashboard and the browser the data is shown in.
- The Worker and Periodic task manager which analyse and persists the results in async manner, using Celery Worker and Celery Beat

Some data like analytics and statuses (calculated event) has the time-series manner which the Timescale library is used to demonstrate and store them.

For providing API the used package is Django Rest Framework (DRF) and for the simplicity the views are just function views. 

All the analytics and statuses data related to a browser instance (a page which loads the front-end application) with cascade on_delete because they have a composition relation. 

### Running the Solution

All the running section in the "Scenario" description is valid except for the celery worker part which is modified below to run the celery beat as well:

Start the Celery Worker and Beat
```bash
celery -A core worker -l info -B
```
And for the Test cases just run
```bash
python manage.py test analytics dashboard 
```

### Suggestions
1. Using Class-Based Views and implement a Full RESTful API set.
2. Adding API Documentation and Design Tools like Swagger.
3. Adding throttling mechanism
4. Using Django Session for User and Session Management.
5. Design and Implementing an N-tier Design instead of Model-View.
6. Design and Implement an Exception Management mechanism.
7. Fully design based on Domain Driven Design.
8. Implementing Full Event-Driven Micro-service Architecture (like Event Sourcing or Transactional Outbox).

