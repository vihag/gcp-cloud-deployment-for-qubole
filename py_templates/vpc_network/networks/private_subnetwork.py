# Creates a SubNetwork in the Qubole Dedicated VPC.
# 1. This will be the notional private subnetwork in which Qubole will launch clusters without External IP
#
# This is for the following reason:
# 1. Not having internet access can be an important security requirment

""" Create a sub-network that will act as the private sub-network hosting the clusters in the Qubole dedicated VPC. """


def GenerateConfig(context):
    """ Create a sub-network that will act as the private sub-network hosting the clusters in the Qubole dedicated VPC. """

    resources = [{
        'name': 'qu-vpc-private-subnetwork',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'network': '$(ref.qubole-dedicated-vpc.selfLink)',
            'ipCidrRange': '10.3.0.0/24',
            'region': context.properties['region'],
            # TODO enable this once Serivce Networking API is supported by GCP DM
            #'privateIpGoogleAccess': True,
            'enableFlowLogs': False
        }
    }]
    return {'resources': resources}