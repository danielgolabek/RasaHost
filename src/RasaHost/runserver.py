"""
This script runs the RasaHost application using a development server.
"""

import os
current_dir = os.path.dirname(os.path.realpath(__file__))

def train_core():
    from rasa_core.policies.fallback import FallbackPolicy
    from rasa_core.policies.keras_policy import KerasPolicy
    from rasa_core.interpreter import RasaNLUInterpreter
    from rasa_core.agent import Agent
    from rasa_core import utils, server
    from rasa_core.channels.channel import UserMessage
    from rasa_core_sdk.executor import ActionExecutor

    utils.configure_colored_logging("DEBUG")
    utils.configure_file_logging("DEBUG", "rasa_core_logs.txt")

    agent = Agent(os.path.join(current_dir, "sample/domain.yml"), 
                  policies=[
                      KerasPolicy(), 
                      FallbackPolicy(fallback_action_name="action_default_fallback",
                              core_threshold=0.3,
                              nlu_threshold=0.3)])
    data = agent.load_data(os.path.join(current_dir, "sample/stories"))
    agent.train(data)
    agent.persist(os.path.join(current_dir, "sample/domain.yml"))


def train_nlu():
    from rasa_nlu import utils, config
    from rasa_nlu.training_data.loading import load_data
    from rasa_nlu.model import Trainer
    from rasa_nlu.config import RasaNLUModelConfig
    nlu_config = config.load(os.path.join(current_dir, "sample/nlu_config.yml"))
    nlu_trainer = Trainer(nlu_config)
    nlu_training_data = load_data(os.path.join(current_dir, "sample/intents"))
    nlu_trainer.train(nlu_training_data)
    nlu_trainer.persist(os.path.join(current_dir, "sample/models/current/nlu"))

from RasaHost import host
host.set_data_path(os.path.join(current_dir, "sample"))

if __name__ == '__main__':    
    host.run()

