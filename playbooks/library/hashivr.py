#!/usr/bin/python
# The import path of hashivault changes depending on where you have kept it
from ansible.modules.hvault import hashivault
from ansible.module_utils.basic import *

'''
Reades an hashicorp vault entry.
'''


def main():

    fields = {
        "approlename": {"required": True, "type": "str"},
        "location": {"required": True, "type": "str"},
    }
    module = AnsibleModule(argument_spec=fields)
    response = hashivault().get_secret(module.params['approlename'], module.params['location'])
    module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()
