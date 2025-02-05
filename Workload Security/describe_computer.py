from __future__ import print_function
import sys, warnings
import deepsecurity
from deepsecurity.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
import os

# Pegando as informações
dotenv_file = f".\Config\.env.ws"

# Carregando as váriaveis do arquivo .env
load_dotenv(dotenv_file)


# Setup
if not sys.warnoptions:
	warnings.simplefilter("ignore")
configuration = deepsecurity.Configuration()
#configuration.host = 'https://cloudone.trendmicro.com/api/computers/'
configuration.host = 'https://cloudone.trendmicro.com/workload/api/computers/'
# Authentication
configuration.api_key['api-secret-key'] = os.getenv("configuration.api_key['api-secret-key']")
configuration.api_key['Authorization'] = os.getenv("configuration.api_key['Authorization']")

# Initialization
# Set Any Required Values
api_instance = deepsecurity.ComputersApi(deepsecurity.ApiClient(configuration))
computer_id = 1
api_version = 'v1'
expand_options = deepsecurity.Expand()
expand_options.add(expand_options.none)
expand = expand_options.list()
overrides = False

try:
	api_response = api_instance.describe_computer(computer_id, api_version, expand=expand, overrides=overrides)
	pprint(api_response)
except ApiException as e:
	print("An exception occurred when calling ComputersApi.describe_computer: %s\n" % e)

