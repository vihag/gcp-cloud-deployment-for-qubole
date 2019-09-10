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