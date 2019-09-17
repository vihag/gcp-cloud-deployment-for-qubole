"""Bring together all the elements required to setup a Network for Qubole"""


def GenerateConfig(context):
    """Bring together all the elements required to setup a Network for Qubole"""

    resources = [{
        'name': 'qubole_bastion_external_address',
        'type': 'gcp_compute_address_qubole_bastion_ext.py',
        'properties': {
            'region': context.properties['region']
        }
    }, {
        'name': 'qubole_bastion_ingress_rules',
        'type': 'gcp_compute_firewall_qubole_bastion_ingress.py'
    }, {
        'name': 'qubole_bastion_host',
        'type': 'gcp_compute_instance_qubole_bastion.py',
        'properties': {
            'zone': context.properties['zone'],
            'bastion-vm-type': context.properties['bastion-vm-type'],
            'deployment-suffix': context.properties['deployment-suffix'],
            'public_ssh_key': context.properties['public_ssh_key'],
            'qubole_public_key': context.properties['qubole_public_key']
        }
    }, {
        'name': 'nat_for_qubole_private_subnet',
        'type': 'gcp_compute_nat_qubole_priv_subnet.py',
        'properties': {
            'region': context.properties['region']
        }
    }, {
        'name': 'qubole_dedicated_vpc',
        'type': 'gcp_compute_network_qubole_dedicated_vpc.py'
    }, {
        'name': 'qubole_private_subnetwork',
        'type': 'gcp_compute_subnetwork_qubole_priv_subnet.py',
        'properties': {
            'region': context.properties['region']
        }
    }, {
        'name': 'qubole_pub_subnetwork',
        'type': 'gcp_compute_subnetwork_qubole_pub_subnet.py',
        'properties': {
            'region': context.properties['region']
        }
    }
    ]
    return {'resources': resources}
