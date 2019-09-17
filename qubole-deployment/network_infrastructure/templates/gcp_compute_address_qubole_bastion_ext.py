# Creates a Static External IP address for
# 1. The GCE VM being used as the Bastion Host in the Qubole dedicated VPC
#
# This is for the following reason:
# 1. If we use ephemeral IP, everytime the bastion restarts, Qubole configuration - metastore/clusters will have to be updated

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
