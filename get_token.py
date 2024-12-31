import requests

url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = 'your api key'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'your authorize code'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# json 저장
import json
#1.
with open(r"kakao_code.json","w") as fp:
    json.dump(tokens, fp)