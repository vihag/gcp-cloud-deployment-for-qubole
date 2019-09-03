# Create a notional private subnetwork which will host Qubole Spark/Hive/Airflow
#
# The bastion host in the public subnetwork will be Qubole's gateway into the private subnetwork
# The private subnetwork is protected by firewall rules which default to deny everything
#
# References https://github.com/GoogleCloudPlatform/deploymentmanager-samples/blob/master/community/cloud-foundation/templates/network/subnetwork.py.schema

""" Create a sub-network that will act as the private sub-network hosting the clusters in the Qubole dedicated VPC. """


def GenerateConfig(context):
    """Creates the network."""

    resources = [{
        'name': 'qu-vpc-private-subnetwork',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'network': '$(ref.qubole-dedicated-vpc.selfLink)',
            'ipCidrRange': '10.3.0.0/24',
            'region': context.properties['region'],
            'privateIpGoogleAccess': True,
            'enableFlowLogs': False
        }
    }]
    return {'resources': resources}