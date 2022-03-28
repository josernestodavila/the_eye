# The Eye
"The Eye" is a service that collects events from registered applications.

The events can have the following shape:

```json
  {
    "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
    "category": "page interaction",
    "name": "pageview",
    "data": {
      "host": "www.consumeraffairs.com",
      "path": "/",
    },
    "timestamp": "2021-01-01 09:15:27.243860"
  }
  
  {
    "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
    "category": "page interaction",
    "name": "cta click",
    "data": {
      "host": "www.consumeraffairs.com",
      "path": "/",
      "element": "chat bubble"
    },
    "timestamp": "2021-01-01 09:15:27.243860"
  }
  
  {
    "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
    "category": "form interaction",
    "name": "submit",
    "data": {
      "host": "www.consumeraffairs.com",
      "path": "/",
      "form": {
        "first_name": "John",
        "last_name": "Doe"
      }
    },
    "timestamp": "2021-01-01 09:15:27.243860"
  }
```

## Setup Development Environment
"The Eye" uses Docker for development, to automate the process we use `invoke`. To set up the local
development environment first create a Python virtual environment with:

### TL;DR
```zsh
# Setup a Python virtualenv
> pyenv install 3.10.2
> pyenv 3.10.2 theeye
> pyenv activate theeye
> pip install invoke pyyaml requests

# Clone this repository
> git clone https://github.com/josernestodavila/the_eye.git
> cd the_eye

# Create a local_settings.py
> cp the_eye/local_settings.py.template the_eye/local_settings.py

# Build the docker containers 
> invoke build
```
You can see list of available tasks by running `invoke -l`.

### Building Docker container
First create a `.env` file in the root directory of the project, a sample `.env` file looks like this:

```dotenv
CELERY_BROKER_URL=amqp://rabbituser:rabbitpass@rabbitmq:5672//
DEBUG=true
ENVIRONMENT=local
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
RABBITMQ_DEFAULT_USER=rabbituser
RABBITMQ_DEFAULT_PASS=rabbitpass
```

To build the Docker containers used by "The Eye" run: `invoke build`, building the docker containers
might take a couple of minutes depending on your internet connection. At the end of the command you
should see something like this: 

```zsh
INFO:     Will watch for changes in these directories: ['/var/task']
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [19] using watchgod
INFO:     Started server process [28]

```

An API web client is available at http://localhost:8001/.

### Running the tests suite 
To run the test suite you only have to run `invoke test`.

## Solution Description

### The `Application` model
To register the Applications that will be authorized to send events to "The Eye" a custom Django
User model was created derived from the `AbstractBaseUser` since we don't need all the other fields
coming from Django's `AbstractUser`. With this implementation we can leverage on Django REST Framework's
token authentication to generate the access `token` for each client application. To register an application
we only need to create an instance of the `Application` model and save it to the database like this:

```zsh
> invoke connect
> python manage.py shell_plus
```
```python
In [1]: from events.models import Application
In [2]: app = Application.objects.create(name='iOS Application')
In [3]: print(app.auth_token)
Out [3]:
9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### The `Session` model
The `Session` entity associates a session to an `Application`, to avoid a session being associated
to two different applications a unique constraint was added to the `Session.id` field in the `Session`
model.

### The `Event` model
This entity is in charge to record all the events into "The Eye" database. This model is associated 
to a `Session` through a foreign key. The records on this model are by default on
descending order by `session_id` and `timestamp`. A `CheckConstraint` was added at database level to
ensure that avoid events to created with future dated timestamps.

### The `EventView` class
To create and retrieve events a Django REST Framework API is exposed to the authenticated applications
(using Token authentication). This endpoint leverage on the `EventSerializer` class to validate the
incoming payload and returning errors back to the clients in case such are found. As well as with the
`Event` model, a validation was introduced on the `EventSerializer.validate_timestamp()` method so that
the serializer can raise a validation error without waiting to hit the database.

### Pending Improvements
- Add more tests for the `EventView` class, specifically for the `get()` method.
- Add a serializer for the `EventSerializer.data` field.
