# Hecho-events

Event Broker for Rasa Chatbot to send metrics to [Hecho Dashboard](https://hecho.ml).

Start **monitoring** your **Rasa Chatbot** right now, access [https://hecho.ml](https://hecho.ml)!!

## Getting Started

```
pip install hecho-events aiohttp
```

Register at [https://hecho.ml](https://hecho.ml) to get an api key.

After install add this entries to `endpoints.yml`:
```yaml
# endpoints.yml
event_broker:
  type: hecho-events.main.RasaEventBroker
  api_key: "<your-api-key>"
  api_url : "https://hecho.ml/api"
```

## Dependencies

```
pip install aiohttp
```


## About Hecho

**Hecho Dashboard** is a platform to store and show messaging, users, intents and much more from your **chatbot**.
