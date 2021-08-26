from ansible import inventory
from ansible.playbook import Playbook
from ansible.plugins.callback import CallbackBase
from ansible import utils

import jinja2
from tempfile import NamedTemporaryFile
import os

# Callback plugin to capture output


class ResultsCollectorJSONCallback(CallbackBase):
    pass


# Dynamic Inventory
inventory = """
[tenant]
{{public_ip_address}}

[tenant:vars]
domain={{domain_name}}
tenant_id={{tenant_id}}
tenant_name={{tenant_name}}
tenant_email={{tenant_email}}
"""

inventory_template = jinja2.Template(inventory)
rendered_inventory = inventory_template.render({
    'public_ip_address': '',
    'domain_name': ''
})

# create a temporary file and write the template string to it
hosts = NamedTemporaryFile(delete=False)
hosts.write(rendered_inventory)
hosts.close()

pb = Playbook(
    playbook='/ansible/launch.yml',
    host_list=hosts.name,
    remote_user='ubuntu',
)

results = pb.run()

# Ensure on_stats callback is called
# for callback modules

os.remove(hosts.name)

print(results)
