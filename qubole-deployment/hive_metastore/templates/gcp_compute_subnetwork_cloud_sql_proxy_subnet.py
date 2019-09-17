# Creates a SubNetwork in the VPC designated to host the Cloud SQL Proxy Process
#
# This is for the following reason:
# 1. This VPC will be Private IP peered with the Cloud SQL instance for security reasons

""" Create a sub-network that will act as the private sub-network hosting the Cloud SQL Proxy. """


def GenerateConfig(context):
    """ Create a sub-network that will act as the private sub-network hosting the Cloud SQL Proxy. """

    resources = [{
        'name': 'cloud-sql-proxy-subnetwork',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'network': '$(ref.cloud-sql-proxy-vpc.selfLink)',
            'ipCidrRange': '10.174.0.0/20',
            'region': context.properties['region'],
            # TODO check if Cloud SQL Private IP access can be achieved with DM
            'privateIpGoogleAccess': True,
            'enableFlowLogs': False
        }
    }]
    return {'resources': resources}
