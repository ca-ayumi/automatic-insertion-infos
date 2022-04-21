import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
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
token_dev = json.loads(response.content)["access_token"]

endpoint = "https://oauth.prd.franq.com.br/oauth2/token/"
response_prd = requests.post(endpoint, files=payload, data=payload)
token_prod = json.loads(response_prd.content)["access_token"]

# Get All Orders

times = []

for _ in range(3):
    for page in range(10):
        endpoint_dev = f"http://checkout.devfranq.vpn/franq-api/v1/getallorders/?page={page}"
        header_dev = {}
        header_dev["Authorization"] = "Bearer " + token_dev
        response_dev = requests.get(endpoint_dev, headers=header_dev)
        endpoint_prod = f"https://checkout.franq.com.br/franq-api/v1/getallorders/?page={page}"
 
        header_prod = {}
        header_prod["Authorization"] = "Bearer " + token_prod
        response_prod = requests.get(endpoint_prod, headers=header_prod)
        times.append([response_dev.elapsed.total_seconds(),
                      response_prod.elapsed.total_seconds()])

df = pd.DataFrame(times, columns=list('DP'))
plt.figure()

ax1 = df.D.plot(color='blue', grid=True, label='Dev')
ax1 = df.P.plot(color='red', grid=True, label='Prod')

h1, l1 = ax1.get_legend_handles_labels()
plt.legend(h1, l1, loc=2)
plt.show()
