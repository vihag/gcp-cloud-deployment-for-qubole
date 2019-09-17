# Creates a Static Global IP address range for
# 1. The Cloud SQL Instance to use when peering with the Cloud SQL Proxy VPC
#
# This is for the following reason:
# 1. When Service Peering, the service creates a new project, VPC and subnetwork. The IP range for the subnetwork is this Global IP address range
# 2. Allocating an address range ensures that there are no IP range conflicts between the service providers network and service consumers network

"""Creates the dedicated address range for PrivateIP connections to and from Cloud SQL Proxy VPC."""

def GenerateConfig(context):
    """Creates the dedicated address range for PrivateIP connections to and from Cloud SQL Proxy VPC."""

    resources = [{
        'name': 'cloudsql-int-address-range',
        'type': 'compute.v1.globalAddresses',
        'properties': {
            'region': context.properties['region'],
            'purpose': 'VPC_PEERING',
            'prefixLength': 24,
            'addressType': 'INTERNAL',
            'description': 'Dedicated address range for PrivateIP connections to and from Qubole VPC',
            'network': '$(ref.cloud-sql-proxy-vpc.selfLink)',
        }
    }]
    return {'resources': resources}
