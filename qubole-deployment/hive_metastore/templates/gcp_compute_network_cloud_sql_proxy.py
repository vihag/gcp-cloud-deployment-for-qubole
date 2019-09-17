# Creates a VPC designated to host the Cloud SQL Proxy Process
#
# This is for the following reason:
# 1. This VPC will be Private IP peered with the Cloud SQL instance for security reasons
# 2. This VPC will be able to use Private IP peering
#
# Cloud SQL Proxy is required in a scalable architecture. Please see Connecting from External Applications: https://cloud.google.com/sql/docs/mysql/external-connection-methods

"""Creates the network."""


def GenerateConfig(unused_context):
    """Creates the network."""

    resources = [{
        'name': 'cloud-sql-proxy-vpc',
        'type': 'compute.v1.network',
        'properties': {
            'routingConfig': {
                'routingMode': 'REGIONAL'
            },
            'autoCreateSubnetworks': False,
            'privateIpGoogleAccess': True
        }
    }]
    return {'resources': resources}
