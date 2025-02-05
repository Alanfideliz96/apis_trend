import requests
import json
from dotenv import load_dotenv
import os

url_base = 'https://api.xdr.trendmicro.com'
url_path = '/v3.0/oat/detections'

# Pegando as informações
dotenv_file = f".\Config\.env.v1"

# Carregando as váriaveis do arquivo .env
load_dotenv(dotenv_file)

token = os.getenv("token")

query_params = {
    'detectedStartDateTime': '2024-10-08T00:00:00Z',
    'detectedEndDateTime': '2024-10-09T00:00:00Z',
    #'ingestedStartDateTime': '2024-10-08T00:00:00Z',
    #'ingestedEndDateTime': '2024-04-09T00:00:00Z',
    'top': '10'
}
headers = {
    'Authorization': 'Bearer ' + token,
    #'TMV1-Filter': 'YOUR_FILTER (string)'
}

r = requests.get(url_base + url_path, params=query_params, headers=headers)

print(r.status_code)
for k, v in r.headers.items():
    print(f'{k}: {v}')
print('')
if 'application/json' in r.headers.get('Content-Type', '') and len(r.content):
    print(json.dumps(r.json(), indent=4))
else:
    print(r.text)