# Create a notional private subnetwork which will host the Cloud SQL Proxy


""" Create a sub-network that will act as the private sub-network hosting the Cloud SQL Proxy. """


def GenerateConfig(context):
    """Creates the network."""

    resources = [{
        'name': 'cloud-sql-proxy-subnetwork',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'network': '$(ref.cloud-sql-proxy-vpc.selfLink)',
            'ipCidrRange': '10.174.0.0/20',
            'region': context.properties['region'],
            # TODO check if Cloud SQL Private IP access can be achieved with DM
            'privateIpGoogleAccess': True,
            'enableFlowLogs': False
        }
    }]
    return {'resources': resources}