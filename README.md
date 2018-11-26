# RasaHost

ui and host for Rasa Nlu and Rasa Core

### Installation
pip install rasa-host

### Running
```python
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent
interpreter = RasaNLUInterpreter('models/current/nlu')
agent = Agent.load("models/current/dialogue", interpreter=interpreter)

from RasaHost import host
host.set_data_path("path_to_directory_with_data")
host.agent = agent
if __name__ == '__main__':    
    host.run()
    # werkzeug  -  * Running on http://0.0.0.0:5005/ (Press CTRL+C to quit)
    
    # GET http://localhost:5005/conversations/daniel/respond?q={{message}}
```

### Screens

![Rasa Chat](doc/chat.PNG "Rasa Chat")

### NLU - Editing md files
![Rasa Nlu Editor](doc/data-nlu.PNG "Rasa Nlu Editor")

### Core - Stories - Editing md files
![Rasa Core Stories Editor](doc/data-stories.PNG "Rasa Core Stories Editor")

### Core - Domain - Editing the file
![Rasa Domain Editor](doc/data-domain.PNG "Rasa Domain Editor")

### Core - Conversations logs
![Rasa Conversations](doc/logs-conversations.PNG "Rasa Conversations")

### Core - Conversations details logs
![Rasa Logs](doc/logs-rasa.PNG "Rasa Logs")


### Actions
You can also host actions, with or without agent.
```python
from rasa_core_sdk.executor import ActionExecutor
actionExecutor = ActionExecutor()
actionExecutor.register_package('actions')

from RasaHost import host
host.actionExecutor = actionExecutor
if __name__ == '__main__':    
    host.run()
    # werkzeug  -  * Running on http://0.0.0.0:5005/ (Press CTRL+C to quit)
    # POST http://localhost:5005/actions
```

### Agent with actions
```python
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent
from rasa_core import utils, server
from rasa_core_sdk.executor import ActionExecutor
#  #rasa-host.endpoints.yml
#  action_endpoint:
#  url: "http://localhost:5005/actions"
action_endpoint_conf = utils.read_endpoint_config("rasa-host.endpoints.yml", endpoint_type="action_endpoint")
interpreter = RasaNLUInterpreter('models/current/nlu')
agent = Agent.load("models/current/dialogue", interpreter=interpreter, action_endpoint=action_endpoint_conf)

actionExecutor = ActionExecutor()
actionExecutor.register_package('actions')

from RasaHost import host
host.set_data_path("path_to_directory_with_data")
host.agent = agent
host.actionExecutor = actionExecutor
if __name__ == '__main__':    
    host.run()
    # werkzeug  -  * Running on http://0.0.0.0:5005/ (Press CTRL+C to quit)
    
    # GET http://localhost:5005/conversations/daniel/respond?q={{message}}
    # POST http://localhost:5005/actions
```

### Channels
Supports channels. All the conversations will be logged.
```python
from rasa_core.channels.botframework import BotFrameworkInput
input_channel = BotFrameworkInput(
        app_id="",
        app_password=""
)

from RasaHost import host
host.agent = agent
host.channels = [input_channel]
if __name__ == '__main__':    
    host.run()
```


