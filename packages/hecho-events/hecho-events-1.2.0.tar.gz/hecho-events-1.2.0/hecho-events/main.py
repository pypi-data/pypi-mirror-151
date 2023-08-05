import requests
import decouple
import json
import asyncio

# send interval is in seconds
SEND_INTERVAL = 5
# max size before sending
MAX_QUEUE_SIZE = 512


class RasaEventBroker():
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url
        self.queue = list()
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self.start_loop())

    def insert_entities_text(self, text, entities):
        for entity in entities:
            entity["text"] = text[entity["start"]:entity["end"]]
        return entities

    def check_duplicate_entities(self, entities):
        entities_start = list()
        new_entities = list()
        entities = sorted(entities, key=lambda entity: entity['start'])
        for entity in entities:
            if entity["start"] not in entities_start:
                entities_start.append(entity["start"])
                new_entities.append(entity)
        return new_entities

    def publish(self, event):
        try:
            if event['event'] == 'user':
                text = event['text']
                new_text = text
                event['parse_data']['entities'] = self.insert_entities_text(text, event["parse_data"]["entities"])
                entities = self.check_duplicate_entities(event['parse_data']['entities'])
                event['handled'] = event['parse_data']['intent']['name'] != 'nlu_fallback'
                for entity in entities:
                    dict_entity = {'entity': entity['entity'], 'value': entity['value']}
                    new_text = new_text.replace(entity["text"], f"[{entity['text']}]{json.dumps(dict_entity)}", 1)
                event['text'] = new_text
            if event['event'] in ['session_started', 'user', 'bot']:
                self.add_to_queue(event)
        except:
            print('Failed to add event to queue')

    def add_to_queue(self, event):
        self.queue.append(event)
        if len(self.queue) > MAX_QUEUE_SIZE:
            loop = asyncio.get_event_loop()
            loop.create_task(self.post_events())

    async def post_events(self):
        try:
            if len(self.queue) <= 0:
                return
            queue_to_send = self.queue
            self.queue = list()
            url = f"{self.api_url}/track"
            params = {
                "apiKey": self.api_key,
                "platform": "rasa"
            }
            response = requests.post(url, params=params, json=queue_to_send)
            if response.status_code != 201:
                print('Failed to send events to Hecho', response.status_code)
        except:
            print('Failed to send events to Hecho')

    async def start_loop(self):
        while True:
            await asyncio.sleep(SEND_INTERVAL)
            await self.post_events()

    async def close(self):
        self.task.cancel()
        await self.post_events()

    @classmethod
    async def from_endpoint_config(cls, broker_config):
        if broker_config is None:
            return None
        return cls(**broker_config.kwargs)
