# The VPC dedicated for Qubole should have an address range dedicated for PrivateIP
#
# See https://cloud.google.com/vpc/docs/configure-private-services-access
# See sudo gcloud compute addresses delete google-managed-services-qubole-dedicated-vpc --global for deleting global addresses

"""Creates the dedicated address range for PrivateIP connections to and from Qubole VPC."""

def GenerateConfig(context):
    """Creates the dedicated address range for PrivateIP connections to and from Qubole VPC."""

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