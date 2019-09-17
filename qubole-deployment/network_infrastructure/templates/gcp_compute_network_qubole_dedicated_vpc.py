# Creates a VPC that will be dedicated to use by Qubole.

"""Creates the Qubole Dedicated Virtual Private Network."""


def GenerateConfig(unused_context):
    """Creates the Qubole Dedicated Virtual Private Network."""

    resources = [{
        'name': 'qubole-dedicated-vpc',
        'type': 'compute.v1.network',
        'properties': {
            'routingConfig': {
                'routingMode': 'REGIONAL'
            },
            'autoCreateSubnetworks': False
        }
    }]
    return {'resources': resources}
