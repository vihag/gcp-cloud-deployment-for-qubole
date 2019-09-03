# Create an External IP to be attached to the bastion host

"""Creates the bastion host external IP for Qubole."""

def GenerateConfig(context):
    """Creates the bastion host external IP for Qubole."""

    resources = [{
        'name': 'qubole-bastion-external-ip',
        'type': 'compute.v1.address',
        'properties': {
            'region': context.properties['region']
        }
    }]
    return {'resources': resources}