#!/usr/bin/python
# The import path of hashivault changes depending on where you have kept it
from ansible.modules.hvault import hashivault
from ansible.module_utils.basic import *

'''
cretes hashicorp vault entry.
hashi(corp)v(ault)c(create)
'''


def main():

    fields = {
        "approlename": {"required": True, "type": "str"},
        "location": {"required": True, "type": "str"},
        "json_data": {"required": True, "type": "str"},
    }
    module = AnsibleModule(argument_spec=fields)
    response = hashivault().set_secret(module.params['approlename'],
                                       module.params['location'],
                                       module.params['json_data'])
    module.exit_json(changed=True, meta=response)


if __name__ == '__main__':
    main()
