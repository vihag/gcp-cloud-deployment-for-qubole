# Create a VM that will act as a Bastion Host for communication with the Qubole Control Plane
#
# The bastion host will sit in the Public Subnetwork
# The bastion host will have to be configured with the Qubole Account Level Key
# This will be achieved by the startup script

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
            'machineType': '/zones/'+context.properties['zone']+'/machineTypes/'+context.properties['machineType'],
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