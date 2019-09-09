# Cloud SQL cannot whitelist Internal Networks(Subnets of VPC Networks)
# Hence to be able to connect to different VPCs, the Cloud SQL must sit behing a Cloud SQL Proxy
# This VPC will host the Cloud SQL Proxy
#
# References
# Connecting from External Applications: https://cloud.google.com/sql/docs/mysql/external-connection-methods

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