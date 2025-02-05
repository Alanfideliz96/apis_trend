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
configuration.host = 'https://cloudone.trendmicro.com/api/'


# Authentication
configuration.api_key['api-secret-key'] = os.getenv("configuration_list.api_key['api-secret-key']")
configuration.api_key['Authorization'] = os.getenv("configuration_list.api_key['Authorization']")

# Initialization
# Set Any Required Values
api_instance = deepsecurity.ComputersApi(deepsecurity.ApiClient(configuration))
api_version = 'v1'
expand_options = deepsecurity.Expand()
expand_options.add(expand_options.none)
expand = expand_options.list()
overrides = False

try:
	api_response = api_instance.list_computers(api_version, expand=expand, overrides=overrides)
	pprint(api_response)
	print("Opaaaa")
except ApiException as e:
	print("An exception occurred when calling ComputersApi.list_computers: %s\n" % e)

