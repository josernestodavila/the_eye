# The Eye
"The Eye" is a service that collects events from registered applications.

The events can have the following shape:

```json
[
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
]
```

## Setup Development Environment
"The Eye" uses Docker for development, to automate the process we use `invoke`. To setup the local development environment first create
a virtualenvironment with:

```zsh
> pyenv install 3.10
> pyenv 3.10 theeye
> pyenv activate theeye
> pip install invoke pyyaml requests
```
You can see list of available tasks by running `invoke -l`.

### Building Docker container
To build the Docker container for "The Eye" run: `invoke build`.


