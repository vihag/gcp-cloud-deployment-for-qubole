"""Creates the firewall ingress rules for the Qubole Bastion."""


def GenerateConfig(unused_context):
    """Creates the firewall."""

    resources = [{
        'name': 'bastion-ingress-from-qubole',
        'type': 'compute.v1.firewall',
        'properties': {
            'network': '$(ref.qubole-dedicated-vpc.selfLink)',
            'sourceRanges': ['34.73.1.130/32'],
            'targetTags': ['qubole-bastion-host'],
            'allowed': [{
                'IPProtocol': 'TCP',
                'ports': [22]
            }]
        }
    }, {
        'name': 'bastion-ingress-from-private-subnet',
        'type': 'compute.v1.firewall',
        'properties': {
            'network': '$(ref.qubole-dedicated-vpc.selfLink)',
            'sourceRanges': ['$(ref.qu-vpc-private-subnetwork.ipCidrRange)'],
            'targetTags': ['qubole-bastion-host'],
            'allowed': [{
                'IPProtocol': 'TCP',
                'ports': [7000]
            }]
        }
    }]
    return {'resources': resources}