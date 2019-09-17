# Creates a Firewall Rule that
# 1. Allows ingress to the Bastion Host from Qubole's Tunneling NAT
# 2. Allows ingress to the Bastion Host from the Private Subnet in the Qubole Dedicated VPC
#
# This is for the following reason:
# 1. Qubole Control Plane will talk(e.g. command submissions) to the Qubole Clusters via the Bastion Host


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
