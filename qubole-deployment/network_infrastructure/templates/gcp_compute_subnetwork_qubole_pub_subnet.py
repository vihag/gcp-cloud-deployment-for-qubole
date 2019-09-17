# Creates a SubNetwork in the Qubole Dedicated VPC.
# 1. This will be the notional public subnetwork in which a Bastion Host will reside
#
# This is for the following reason:
# 1. The Bastion host is the secure gateway through which Qubole will talk to the clusters running in the customer's project/network

""" Create a sub-network that will act as the public sub-network hosting the bastion host in the Qubole dedicated VPC. """


def GenerateConfig(context):
    """ Create a sub-network that will act as the public sub-network hosting the bastion host in the Qubole dedicated VPC. """

    resources = [{
        'name': 'qu-vpc-public-subnetwork',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'network': '$(ref.qubole-dedicated-vpc.selfLink)',
            'ipCidrRange': '10.2.0.0/24',
            'region': context.properties['region'],
            'privateIpGoogleAccess': True,
            'enableFlowLogs': False
        }
    }]
    return {'resources': resources}