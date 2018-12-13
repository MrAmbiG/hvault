# hvault
Read from and Write to Hashicorp's Vault
## Hashicorp Vault setup it supports
Please look at hvault (python) and ansible-modules-hashivault for a broader
coverage.
This reads and writes to hashicorp's vault. This is written for a specific
setup. This is designed for the following setup/design of hashicorp's vault.
1. An approle is created on hashicorp's vault  
2. You have to provide the approle's token to a specific hashicorp vault's
    address and get the SECRET_ID
3. Use this SECRET_ID along with VAULT_ROLE_ID to generate a shortlived
    CLIENT_TOKEN.
4. Use the CLIENT_TOKEN to perform a read or write activity.
    _In short:- you generate a SECRET_ID to generate a CLIENT_TOKEN to do a or
    few read/write action against hashicorp vault. Since The CLIENT_TOKEN is
    shortlived (depending on what you have set the timeout to be) you do this
    for every read/write_

## Prerequisite
* python 2.7+ [Since it is the defacto version shipped with all containers &
    most linux distros, I have kept it compatible with 2.7+. Anyone's help
    to make it compatible with both python2 & 3 are welcome]
* python packages : json, requests
* The following OS environment variables
- VAULT_ADDR - http or https address to the hashicorp vault along with the port
- VAULT_TOKEN - vault token for the approle
- VAULT_ROLE_ID - vault role id for the approle

## How to Use
* for ansible
1. Copy hvault.py to the /usr/lib/python2.7/site-packages/ansible/modules/hvault
 or simply clone this repo inside /usr/lib/python2.7/site-packages/ansible/modules/
 and make sure you also have a __init__.py file at the same location.
2. Move or copy .py files from "library" to your ansible modules directory.
 Check https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html
 on how and where you can copy these ansible module files.
3. Example playbooks are in the playbooks directory along with their jinja2
 templates.

* for python
1. put the hvault.py along with a __init__.py file anywhere. Import that into
   your scripts and have fun
2. examples  
approlename = 'ansible'
location = 'v1/secret/app-credentials/data/test'
JSON_DATA_CONTENT = '{ "batman": "wayne", "superman": "kent" }'
    - Read  
    obj = hashivault().get_secret(approlename, location)  
    print obj
    - write  
    obj = hashivault().set_secret(approlename, location, JSON_DATA_CONTENT)  
    print obj
