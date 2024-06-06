import os
import json
import logging
import ibm_vpc
from ibm_vpc import VpcV1
from ibm_platform_services import IamIdentityV1, ResourceControllerV2, ResourceManagerV2
from ibm_platform_services.resource_controller_v2 import ResourceInstancesPager, ResourceBindingsPager, ResourceKeysPager
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

def setup_logging(default_path='logging.json', default_level=logging.info, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


# Iam authenticator
def iam_authenticator():
    authenticator = IAMAuthenticator(apikey=ibmcloud_api_key)
    return authenticator

def iam_client():
    authenticator = iam_authenticator()  
    iamIdentityService = IamIdentityV1(authenticator=authenticator)
    return iamIdentityService

def resource_controller_client():
    authenticator = iam_authenticator()  
    resourceControllerService = ResourceControllerV2(authenticator=authenticator)
    return resourceControllerService

def resource_manager_client():
    authenticator = iam_authenticator()  
    resourceManagerService = ResourceManagerV2(authenticator=authenticator)
    return resourceManagerService

def get_account_id():
    try:
        client = iam_client()
        api_key = client.get_api_keys_details(
          iam_api_key=ibmcloud_api_key
        ).get_result()
    except ApiException as e:
        logging.error("API exception {}.".format(str(e)))
        quit(1)
    account_id = api_key["account_id"]
    return account_id

def get_all_resource_instances():
    try:
        client = resource_controller_client()
        all_results = []
        pager = ResourceInstancesPager(client=client)
        while pager.has_next():
            next_page = pager.get_next()
            assert next_page is not None
            all_results.extend(next_page)
        print(json.dumps(all_results, indent=2))

    except ApiException as e:
        logging.error("API exception {}.".format(str(e)))
        quit(1)
    return all_results

def vpc_client(region):
    authenticator = iam_authenticator()
    try:
        vpc_service = VpcV1(authenticator=authenticator)
        vpc_service.set_service_url(f'https://{region}.iaas.cloud.ibm.com/v1')
    except ApiException as e:
        logging.error("API exception {}.".format(str(e)))
        quit(1)
    return vpc_service
