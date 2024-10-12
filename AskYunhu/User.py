import requests
import json
from AskYunhu import RandomUA

def Login(email:str, password:str, platform:str) -> dict:
    url = 'https://chat-go.jwzhd.com/v1/user/email-login'
    data = {
        "email": email,
        "password": password,
        "deviceId": RandomUA.Get(),
        "platform": platform
    }
    response = requests.post(url, data=json.dumps(data))
    return json.loads(response.text)