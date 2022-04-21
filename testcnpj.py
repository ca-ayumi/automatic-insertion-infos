import requests
import json
from httpx import Client


# Autenticação
payload = dict(
    client_id='yCR27fACri6wmCBIQ85fewgzmlk2h631ZVDOjC0eYMJ7ibgA',
    client_secret='4NLGghvicLLgeuMaSjj2ukUW15xFowpIrMujw6QwBciWigouo70By200OCyVYMRB9gRfagMrQPQBZ9WnLfd3kIE8Gk6QewuDjE8gBh8ZT8ja5pQ4Dq3uT5J0XewuDWL3',
    scope='franqapp',
    grant_type='password',
    username='franqapp@franq.com.br',
    password='oGohmooBahw6',
)

endpoint = "http://oauth.devfranq.vpn/oauth2/token/"
response = requests.post(endpoint, files=payload, data=payload)
token = json.loads(response.content)["access_token"]

# Get All Orders
for page in range(10):
    endpoint2 = f"http://checkout.devfranq.vpn/franq-api/v1/getallorders/?page={page}"
    header = {}
    header["Authorization"] = "Bearer "+ token
    response = requests.get(endpoint2, headers=header)
    contents = json.loads(response.content)["data"]

    for content in contents:
        print(content["cnpj"])
