# Create an External IP to be attached to the cloud sql proxy host

"""Create an External IP to be attached to the cloud sql proxy host."""

def GenerateConfig(context):
    """Create an External IP to be attached to the cloud sql proxy host."""

    resources = [{
        'name': 'cloud-sql-proxy-external-ip',
        'type': 'compute.v1.address',
        'properties': {
            'region': context.properties['region']
        }
    }]
    return {'resources': resources}