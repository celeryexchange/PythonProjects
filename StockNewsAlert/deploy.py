import subprocess
from jinja2 import Environment, FileSystemLoader
import yaml


# Load variables from config.yaml
with open("config.yaml", "r") as f:
    config_d = yaml.safe_load(f)

resource_group = config_d["resource_group"]
aci_name = config_d["aci_name"]
subscription_id = config_d["subscription_id"]

# Load the Jinja2 template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('logic_app_definition_template.json')

# Render the template with the variables
logic_app_definition = template.render(
    subscription_id=subscription_id,
    resource_group=resource_group,
    aci_name=aci_name
)

# Save the rendered template to a file
# This file will be used by deploy-to-azure.ps1
with open('logicAppDefinition.json', 'w') as f:
    f.write(logic_app_definition)

# Run the PowerShell script to create resources in Azure
# subprocess.run(["powershell", "-File", "deploy-to-azure.ps1"], check=True)