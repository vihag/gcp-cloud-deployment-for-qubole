# Create a notional public subnetwork which will host a bastion host
#
# The bastion host will be Qubole's gateway into the private subnetwork
# This way we can have an additional layer of firewall security through which even Qubole has limited access
# The rest of the world will have now way of accessing the private subnetwork
#
# References https://github.com/GoogleCloudPlatform/deploymentmanager-samples/blob/master/community/cloud-foundation/templates/network/subnetwork.py.schema

""" Create a sub-network that will act as the public sub-network hosting the bastion host in the Qubole dedicated VPC. """


def GenerateConfig(context):
    """Creates the network."""

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