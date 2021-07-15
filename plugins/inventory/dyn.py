from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable, to_safe_group_name

import requests

ANSIBLE_METADATA = {
    'metadata_version': '1.0.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: dyn
plugin_type: inventory
short_description: An example Ansible Inventory Plugin
version_added: "2.9.13"
description:
    - "A very simple Inventory Plugin created for demonstration purposes only."
options:
  id:
    description:
      - Just an option
    type: int
author:
    - Gaëtan Trellu
'''

class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = 'dyn'

    def verify_file(self, path):
        return True

    def _get_raw_host_data(self, id):

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        session = requests.Session()
        req = ("http://150.239.165.187/inventories/{}".format(id))
        response = session.get(req, headers=headers)

        return response.json()

    def _populate(self):
        return True

    def parse(self, inventory, loader, path,
              cache=True):  # Plugin interface (2)
        super(InventoryModule, self).parse(inventory, loader, path)

        self._read_config_data(path)

        id = self.get_option('id')

        raw_data = self._get_raw_host_data(id)
        raw_data.pop('id', None)

        self.inventory.add_group('ibx22')
        self.inventory.add_host(host='ibx22lrdapp01', group='ibx22')
        self.inventory.set_variable('ibx22lrdapp01', 'ansible_host', '10.10.1.4')

        return(raw_data)
        