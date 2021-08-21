from ansible import playbook
from ansible import inventory
from ansible.playbook import Playbook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils

import jinja2
from tempfile import NamedTemporaryFile
import os

# Boilerplate callbacks for stdout/sterr and log output
utils.VERBOSITY = 0
playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
stats = callbacks.AggregateStats()
runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

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
    playbook='/path/to/main/launch.yml',
    host_list=hosts.name,
    remote_user='ubuntu',
    callbacks=playbook_cb,
    runner_callbacks=runner_cb,
    stats=stats,
    private_key_file='/path/to/key.pem'
)

results = pb.run()

# Ensure on_stats callback is called
# for callback modules
playbook_cb.on_stats(pb.stats)

os.remove(hosts.name)

print(results)