# Create an Internal IP to be attached to the cloud sql proxy host

"""Create an External IP to be attached to the cloud sql proxy host."""

def GenerateConfig(context):
    """Create an Internal IP to be attached to the cloud sql proxy host."""

    resources = [{
        'name': 'cloud-sql-proxy-internal-ip',
        'type': 'compute.v1.address',
        'properties': {
            'region': context.properties['region'],
            'addressType': 'INTERNAL',
            'purpose': 'GCE_ENDPOINT',
            'subnetwork': '$(ref.cloud-sql-proxy-subnetwork.selfLink)'
        }
    }]
    return {'resources': resources}