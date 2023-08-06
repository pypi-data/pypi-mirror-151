from datetime import datetime
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def make_start_event(sender_id):
    return {
        "sender_id" : sender_id,
        "event" : "session_started",
        "timestamp" : datetime.timestamp(datetime.now())
    }

def make_user_message(text, sender_id):
    return {
        "sender_id" : sender_id,
        "event" : "user",
        "timestamp" : datetime.timestamp(datetime.now()),
        "text" : text,
        "parse_data" : {
            "intent" : {
                "id" : -3.55026567409232e+18,
                "name" : "greet",
                "confidence" : 0.999085903167725
            },
            "entities" : [],
            "text" : text,
            "message_id" : get_random_string(32),
            "metadata" : {},
            "intent_ranking" : [
                {
                    "id" : -3.55026567409232e+18,
                    "name" : "greet",
                    "confidence" : 0.999085903167725
                },
                {
                    "id" : 6.5339638489912e+18,
                    "name" : "affirm",
                    "confidence" : 0.000509693869389594
                },
                {
                    "id" : 8.90562756180644e+18,
                    "name" : "deny",
                    "confidence" : 0.000218229135498405
                },
                {
                    "id" : -1.27223814573968e+18,
                    "name" : "bot_challenge",
                    "confidence" : 8.98175785550848e-05
                },
                {
                    "id" : -6.06990355981528e+18,
                    "name" : "mood_great",
                    "confidence" : 7.75596563471481e-05
                },
                {
                    "id" : -1.74631550931555e+18,
                    "name" : "goodbye",
                    "confidence" : 1.47294904309092e-05
                },
                {
                    "id" : -6.17061844832234e+18,
                    "name" : "mood_unhappy",
                    "confidence" : 4.06487788495724e-06
                }
            ],
            "response_selector" : {
                "all_retrieval_intents" : [],
                "default" : {
                    "response" : {
                        "id" : None,
                        "responses" : None,
                        "response_templates" : None,
                        "confidence" : 0,
                        "intent_response_key" : None,
                        "utter_action" : "utter_None",
                        "template_name" : "utter_None"
                    },
                    "ranking" : []
                }
            }
        },
        "input_channel" : "cmdline",
        "message_id" : "a1a3ce0263a8482abf3649b16f756604",
        "metadata" : {},
        "handled" : True
    }


def make_bot_message(text, sender_id):
    return {
        "sender_id" : sender_id,
        "event" : "bot",
        "timestamp" : datetime.timestamp(datetime.now()),
        "metadata" : {
            "utter_action" : "utter_greet"
        },
        "text" : text,
        "data" : {
            "elements" : None,
            "quick_replies" : None,
            "buttons" : None,
            "attachment" : None,
            "image" : None,
            "custom" : None
        }
    }
