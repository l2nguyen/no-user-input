from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    ActionExecuted,
    UserUtteranceReverted,
    SlotSet
)

class ActionSetOfficeOpen(Action):

    def name(self) -> Text:
        return "action_get_last_intent"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        current_tracker = tracker.events_after_latest_restart()

        print(current_tracker)

        utterances = [e for e in tracker.events_after_latest_restart() if "parse_data" in e]
        
        # get info about user's original message
        entry_user_event = utterances[-1]
        # get users first intent
        entry_intent = entry_user_event.get('parse_data').get('intent').get('name')
        
        print("====BREAK======")
        print(entry_user_event)
        print("====BREAK======")
        print(entry_intent)    
        
        return [
            SlotSet("last_intent", entry_intent)
        ]

class ActionResumeConvo(Action):

    def name(self) -> Text:
        return "action_resume_after_no_user_input"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        no_user_input_count = tracker.get_slot("voz_continuar")
        print(no_user_input_count)
        print(type(no_user_input_count))

        # get all the user utterances - reversed order
        user_utterances = [e for e in 
                           reversed(tracker.events_after_latest_restart()) 
                           if "parse_data" in e]
        
        
        print("====BREAK======")
        print(user_utterances)
        print("====BREAK======")
        # get info about user's original message before noUserInput
        entry_user_event = user_utterances[no_user_input_count + 1]
        
        # get users first intent
        entry_intent = entry_user_event.get('parse_data').get('intent').get('name')
        

        print(entry_user_event)
        print("====BREAK======")
        print(entry_intent)
        
        if no_user_input_count == 1:
            
            revert_events = [
                            # revert affirmation and request
                            UserUtteranceReverted(), 
                            # revert vaig_noUserInput=1
                            UserUtteranceReverted()
                            ]

        elif no_user_input_count == 2:
            revert_events = [
                            # revert affirmation and request
                            UserUtteranceReverted(),
                            # revert vaig_noUserInput=2
                            UserUtteranceReverted(),
                            # revert vaig_noUserInput=1
                            UserUtteranceReverted()
                            ]
        else:
            revert_events = []
        
        if len(user_utterances) > 1:
            events = revert_events + [
                        # replace action with action listen
                      ActionExecuted("action_listen"), 
                      # set up the response to the user's first intent
                      entry_user_event]
        else:
            events = []

        return events
