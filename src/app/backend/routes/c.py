import json


j = """{
    "date": "2024-12-20",
    "assistant": {
      "0": {
        "timestamp": "2024-12-20T10:00:00Z",
        "msg": "Hello, how can I help you today?"
      },
      "1": {
        "timestamp": "2024-12-20T10:01:00Z",
        "msg": "Do you need assistance with anything specific?"
      },
      "2": {
        "timestamp": "2024-12-20T10:02:00Z",
        "msg": "Feel free to ask any questions."
      }
    },
    "user": {
      "0": {
        "timestamp": "2024-12-20T10:00:30Z",
        "msg": "Hi, I need help with JSON formatting."
      },
      "1": {
        "timestamp": "2024-12-20T10:01:30Z",
        "msg": "Can you provide an example with nested data?"
      }
    }
}"""

def get_assistant_messages(json_str) -> str:
    _json = json.loads(json_str)
    return [v.get('msg') for _, v in _json.get('assistant').items()]

def get_user_messages(json_str) -> str:
    _json = json.loads(json_str)
    return [v.get('msg') for _, v in _json.get('user').items()]

a = get_assistant_messages(j)
u = get_user_messages(j)

for o, t in zip(a, u):
    print(f"Assistant: {o}")
    print(f"User: {t}")
