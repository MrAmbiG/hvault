import requests
import json
import os

# disable InsecureRequestWarning
requests.packages.urllib3.disable_warnings()

# os environment variables
VAULT_ADDR = os.environ['VAULT_ADDR']
VAULT_TOKEN = os.environ['VAULT_TOKEN']
VAULT_ROLE_ID = os.environ['VAULT_ROLE_ID']


class hashivault(object):
    '''
    SYNOPSIS
        Performs basic CRUD operations against hashicorp vault (hvault).
    DESCRIPTION
        This is designed to work against a hashicorp vault setup where
        a 'secret_id' needs to be generated using the 'VAULT_TOKEN',
        'VAULT_ADDR', 'approlename'. The generated 'secret_id' is then used
        to generate a 'client_token' with the help of 'VAULT_ROLE_ID',
        'VAULT_ADDR', 'approlename'. This 'client_token' is shortlived and thus
        every time you want to perform a any CRUD (Create, Read, Update, Delete)
        you have to perform these tasks all over again to avail a very high
        degree of security.
    NOTES
        for ansible
        -----------
        clone this repo to /usr/lib/python2.7/site-packages/ansible/modules/
        move or copy library/*.py files to your ansible library folder
        File Name      : hashivault.py
        Prerequisite   : Python 2.x,
            Python packages : json, requests,
            OS Environment variables :
                VAULT_ADDR : the http or https url to the hashicorp's vault with
                             port number. ex:- http://vault.managed-from.net:443
                VAULT_TOKEN : a token to access hashicorp vault.
                VAULT_ROLE_ID : a role id needed to generate secret_id
    LINK
        https://learn.hashicorp.com/vault/getting-started/apis
        https://curl.trillworks.com/
    '''

    def secret_id(self, approlename):
        '''
        SYNOPSIS : Generates 'secret id' needed to generate 'client token'
        DESCRIPTION : It takes approlename (string) as an input. Returns
            secret_id (string) after parsing the json. VAULT_ADDR, VAULT_TOKEN
            should be present as OS environment variables.
        EXAMPLE: secret_id('ansible')
        '''
        url = "{}/v1/auth/approle/role/{}/secret-id".format(
            VAULT_ADDR, approlename)
        headers = {'X-Vault-Token': "{}".format(VAULT_TOKEN)}
        response = requests.post(url, headers=headers, verify=False)
        json_data = json.loads(response.text)
        return json_data["data"]["secret_id"]

    def client_token(self, approlename):
        '''
        SYNOPSIS : Generates 'client token' using secret_id
        DESCRIPTION : Generate 'client token' needed to perform CRUD operations
            against hvault. approlename(str). VAULT_ADDR, VAULT_TOKEN should be
            present as OS environment variables. Returns a client token (string).
        EXAMPLE: client_token('ansible')
        '''
        SECRET_ID = self.secret_id(approlename)
        data = '{ "role_id": "%s", "secret_id": "%s" }' % (
            VAULT_ROLE_ID, SECRET_ID)
        url = "{}/v1/auth/approle/login".format(VAULT_ADDR)
        response = requests.post(url, data=data, verify=False)
        json_data = json.loads(response.text)
        return json_data["auth"]["client_token"]

    def get_secret(self, approlename, location):
        '''
        SYNOPSIS : Reads from hvault.
        DESCRIPTION : Takes approlename(string) and location(string) as inputs.
            location is the path to the secret excluding the VAULT_ADDR. If
            'VAULT_ADDR/v1/secret/batman/data/DATA_NAME' is
            the location of the data and that you want to get then you should
            only provide 'v1/secret/batman/data/DATA_NAME'.
            VAULT_ADDR should be present as an OS environment variable.
        EXAMPLE: get_secret('ansible', 'v1/secret/batman/data/jenkins_secets')
                Here jenkins_secets is the name of the json data.
        '''
        CLIENT_TOKEN = self.client_token(approlename)
        headers = {'X-Vault-Token': "{}".format(CLIENT_TOKEN)}
        url = '{}/{}'.format(
            VAULT_ADDR, location)
        response = requests.get(url, headers=headers, verify=False)
        json_data = json.loads(response.text)
        return json_data['data']['data']

    def set_secret(self, approlename, location, JSON_DATA_CONTENT):
        '''
        SYNOPSIS : Writes to hvault.
        DESCRIPTION : Takes approlename(string) and location(string) as inputs.
            location is the path to the secret excluding the VAULT_ADDR. If
            'VAULT_ADDR/v1/secret/batman/data/DATA_NAME' is
            the location of the data that you want to set then
            location='v1/secret/batman/data/some_unique_name'. Here
            some_unique_name decides the final path to the data that you are
            storing and thus becomes the name of the data.
            VAULT_ADDR should be present as an OS environment variable.
        EXAMPLE: set_secret('ansible', 'v1/secret/batman/data/some_unique_name',
                            JSON_DATA_CONTENT)
                JSON_DATA_CONTENT='{ "foo": "bar1", "food": "pizza" }'
        '''
        CLIENT_TOKEN = self.client_token(approlename)
        headers = {'X-Vault-Token': "{}".format(CLIENT_TOKEN)}
        JSON_DATA = "{ "+'"data"'+": " + JSON_DATA_CONTENT+"}"
        url = '{}/{}'.format(
            VAULT_ADDR, location)
        response = requests.post(url, headers=headers, data=JSON_DATA)
        return json.loads(response.text)
