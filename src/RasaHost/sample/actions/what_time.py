from rasa_core_sdk import Action

class WhatTimeAction(Action):
   def name(self):
      return "action_general.what_time"

   def run(self, dispatcher, tracker, domain):
    
      dispatcher.utter_message("The current time is " + datetime.datetime.now().strftime("%I:%M%p"))

      return []