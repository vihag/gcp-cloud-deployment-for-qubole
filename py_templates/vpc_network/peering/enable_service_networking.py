# Qubole recommends having a dedicated VPC network in which Qubole can orchestrate your VMS
#
# By doing this, you can isolate Qubole from the rest of your GCP resources
#
# The recommended sub-network configuration is having a public subnetwork, which will host a Bastion Host
# and a private subnetwork, in which Qubole orchestrated Spark/Hive/Airflow clusters will be setup

"""Creates the network."""


def GenerateConfig(unused_context):
    """Creates the network."""

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