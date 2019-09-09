# Qubole recommends having a dedicated VPC network in which Qubole can orchestrate your VMS
#
# By doing this, you can isolate Qubole from the rest of your GCP resources
#
# The recommended sub-network configuration is having a public subnetwork, which will host a Bastion Host
# and a private subnetwork, in which Qubole orchestrated Spark/Hive/Airflow clusters will be setup
#
# Reference in Terraform: https://github.com/terraform-providers/terraform-provider-google/issues/2902
#
# NOT SUPPORTED BY CLOUD DM AS SERVICE NETWORKING IS NOT A SUPPORTED GCP TYPE. SEE https://cloud.google.com/deployment-manager/docs/configuration/supported-gcp-types

"""Creates the network."""


def GenerateConfig(unused_context):
    """Creates the network."""

    resources = [{
        'name': 'enable-service-networking',
        'type': 'gcp-types/servicenetworking.googleapis.com:services.connections',
        'properties': {
            #'parent': 'services/servicenetworking.googleapis.com',
            'network': '$(ref.cloud-sql-proxy-vpc.selfLink)',
            'reservedPeeringRanges': [
                "$(ref.cloudsql-int-address-range.name)"
            ]
        }
    }]
    return {'resources': resources}