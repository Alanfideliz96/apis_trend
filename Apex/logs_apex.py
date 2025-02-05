import base64
import jwt
import hashlib
import requests
import time
import json
import urllib.parse
from dotenv import load_dotenv
import os

def create_checksum(http_method, raw_url, headers, request_body):
    string_to_hash = http_method.upper() + '|' + raw_url.lower() + '|' + headers + '|' + request_body
    base64_string = base64.b64encode(hashlib.sha256(str.encode(string_to_hash)).digest()).decode('utf-8')
    return base64_string


def create_jwt_token(application_id, api_key, http_method, raw_url, headers, request_body,
                     iat=time.time(), algorithm='HS256', version='V1'):
    payload = {'appid': application_id,
               'iat': iat,
               'version': version,
               'checksum': create_checksum(http_method, raw_url, headers, request_body)}
    token = jwt.encode(payload, api_key, algorithm=algorithm)
    return token 
	
# Define the Apex Central server variables (server url, application id, api key)
# Definindo de onde vou buscar as chaves

dotenv_file = f".\Config\.env.apex"

# Pegando as chaves
load_dotenv(dotenv_file)

use_url_base = os.getenv("use_url_base") 
use_application_id = os.getenv("use_application_id")
use_api_key = os.getenv("use_api_key")

# Get the required logs 
# Aqui no caso é onde podemos alterar o módulo do antivirus para trazer as informações que queremos
productAgentAPIPath = '/WebApp/api/v1/Logs/officescan_virus'
canonicalRequestHeaders = ''

useRequestBody = ''

useQueryString="?output_format=CEF&page_token=0&since_time=0"

while True:
    jwt_token = create_jwt_token(use_application_id, use_api_key, 'GET',
                              productAgentAPIPath + useQueryString,
                              canonicalRequestHeaders, useRequestBody, iat=time.time())
    
    headers = {'Authorization': 'Bearer ' + jwt_token , 'Content-Type': 'application/json;charset=utf-8'}
    
    r = requests.get(use_url_base + productAgentAPIPath + useQueryString, headers=headers, verify=False)
    
    if r.status_code!=200:
        print("Error return code: "+ str(r.status_code))
        break
    
    print(json.dumps(r.json(), indent=4))
    
    # Process the log data according to your company's requirements 
    # For example, send the log data to your SIEM server
    
    # Retrieve the QueryString for the next set of log data (if available) 
    nextlink = r.json()["Data"]["Next"]
    if nextlink is None:
        print("No more log data found.")
        pageToken = r.json()["Data"]["NextPage"]["PageToken"]
        time = r.json()["Data"]["NextPage"]["SinceTime"]
        useQueryString = '?output_format=CEF&page_token={pageToken}&since_time={time}'.format(pageToken=pageToken, time=time)
        print("\nAppend the following query string to the next get request for more data\n"+useQueryString)
        break
        
    useQueryString = nextlink[nextlink.index('?'):]
