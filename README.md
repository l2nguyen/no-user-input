# Handle default vaig_noUserInput interruptions in conversations

Bot to handle no audiocode's no user input interruption in a conversation outside the context of a form.

This takes inspiration from the [reverting of events by the TwoStageFallbackPolicy](https://github.com/RasaHQ/rasa/blob/main/rasa/core/actions/action.py#L814)

## How it works

If the `vaig_event_noUserInput` intent occurs because the user has been silent and they affirm that they want to continue, then the custom action `action_resume_after_no_user_input` will:

- revert previous event using `UserUtteranceReverted`
- queue the user's original intent so they can continue their previous journey.

This will remove the `vaig_event_noUserInput` and the `affirm` intents from the tracker so that the ML Policies will not see those events when trying to make a prediction.

### Important notes

- the slot `last_intent` was to see the last intent: purely for debug purposes
- This was not tested in a context of a form so this may not work.

### UserUtteranceReverted

`UserUtteranceReverted`  reverts the user utterance and all events since the last user message, which will include all slot set events after the message.

For example, consider a tracker like so:

```
*intent_1
  - action_1
*intent_2
  - action_2
  - action_3
  - action_4
```

After a `UserUtteranceReverted()`, it will look like:

```
*intent_1
  - action_1
```

### Conditional Response Variation (CRV)

`vaig_event_noUserInput` uses CRV to return different bot utterances based how often it has checked with the user. The bot utterance depends on the value of slot `voz_continuar` - a `from_entity` slot linked to the `value` entity.

Blog post about [CRV](https://rasa.com/blog/conditional-response-variations/)

## How to use this example?

Train a Rasa model containing the Rasa NLU and Rasa Core models by running:

```bash
rasa train
```

The model will be stored in the /models directory as a zipped file.

Test the assistant by running:

```bash
rasa run actions
rasa shell
```

Have the following conversation with the bot:

```
Your input ->  /update_member_info                                               
Certainly. I can help you update your address. Let's look at the address on file.
Your address on file is 123 Somewhere Place.
do you want to update your address?
Your input ->  /vaig_event_noUserInput{"value": 1}                               
Posso ser útil em mais alguma questão?
Your input ->  yes                                                               
Certainly. I can help you update your address. Let's look at the address on file.
Your address on file is 123 Somewhere Place.
do you want to update your address?
Your input ->  yes                                                               
what is your new address?
```
