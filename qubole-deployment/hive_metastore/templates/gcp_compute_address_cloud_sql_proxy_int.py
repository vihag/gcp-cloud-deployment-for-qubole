# Creates a Static Internal IP address for
# 1. The GCE VM hosting the Cloud SQL Proxy Process
#
# This is for the following reason:
# 1. Once enabling Private IP peering via GCP Deployment Manager is possible, this static IP will be used for communication with CloudSQL


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
