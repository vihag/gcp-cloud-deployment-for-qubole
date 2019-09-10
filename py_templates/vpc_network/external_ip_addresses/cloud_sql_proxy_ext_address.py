# Creates a Static External IP address for
# 1. The GCE VM hosting the Cloud SQL Proxy Process
#
# This is for the following reason:
# 1. Right not the proxy process is interacting with the Cloud SQL instance on Public IP, hence the VM needs the IP
# TODO
# Once creating Private IP peering is possible via templates, remove this as we do not want the proxy process to have internet access

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