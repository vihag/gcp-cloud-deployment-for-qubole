# Creates a Google Compute Engine VM that will act as a Bastion Host in the Qubole Dedicated VPC
# Features
# 1. A network interface allowing for a Public IP address
# 2. A custom start up script to create a user configured with accessibility from Qubole
#       - the script should also setup the system to accept Qubole's Public Key and Customer's Account Level SSH key
#
# This is for the following reason:
# 1. Create a secure channel (ssh tunnel forwarding) between the Qubole Control Plane and the Customer's Big Data Clusters
#    - This secure channel will be used to submit commands, perform admin tasks and retrieving results
# 3. Create a secure channel (ssh tunnel forwarding) between the Qubole Control Plane and the Customer's Hive Metastore
#    - This secure channel will be used by the Qubole Control Plane to list the schemas and tables available in the Customer's Hive Metastore
#    - This is ONLY for metadata. No customer data will flow via this channel
#
# Caveats:
# 1. The Bastion needs to be configured to accept
#    - Qubole's Public SSH Key
#    - Customer's Account Level Public SSH Key, retrievable via REST or Qubole UI
#    - The SSH service should allow Gateway ports

"""Creates the bastion host for Qubole."""

def getBootstrapAsArray(public_ssh_key, qubole_public_key):

    return ''.join([
        '#!/bin/bash\n',
        'sudo useradd bastion-user -p \'\'\n',
        'mkdir -p /home/bastion-user/.ssh\n',
        'chown -R bastion-user:bastion-user /home/bastion-user/.ssh\n',
        'bash -c \'echo "'+public_ssh_key+'" >> /home/bastion-user/.ssh/authorized_keys\'\n'
        'bash -c \'echo "'+qubole_public_key+'" >> /home/bastion-user/.ssh/authorized_keys\'\n'
        'bash -c \'echo "GatewayPorts yes" >> /etc/ssh/sshd_config\'\n',
        'sudo service ssh restart\n'
    ])


def GenerateConfig(context):
    """Creates the bastion host for Qubole."""

    resources = [{
        'name': 'qubole-bastion-host',
        'type': 'compute.v1.instance',
        'properties': {
            'zone': context.properties['zone'],
            'machineType': '/zones/'+context.properties['zone']+'/machineTypes/'+context.properties['bastion-vm-type'],
            'canIpForward': True,
            'tags': {
                'items': [
                    'qubole-bastion-host'
                ]
            },
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': 'projects/'+'debian-cloud/global/'+'images/family/debian-9'
                }
            }],
            'networkInterfaces': [{
                'network': '$(ref.qubole-dedicated-vpc.selfLink)',
                'subnetwork': '$(ref.qu-vpc-public-subnetwork.selfLink)',
                'accessConfigs': [{
                    'name': 'External NAT',
                    'type': 'ONE_TO_ONE_NAT',
                    'natIP': '$(ref.qubole-bastion-external-ip.address)'
                }]
            }],
            'metadata': {
                'items': [{
                    'key': 'startup-script',
                    'value': ''+getBootstrapAsArray(context.properties['public_ssh_key'], context.properties['qubole_public_key'])
                }]
            }
        }
    }]
    return {'resources': resources}
