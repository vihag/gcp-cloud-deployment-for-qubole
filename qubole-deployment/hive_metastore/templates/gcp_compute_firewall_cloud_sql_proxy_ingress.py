# Creates a Firewall Rule that
# 1. Allows ingress to the Cloud SQL Proxy Host from the Bastion in the Qubole Dedicated VPC
# 2. Allows ingress to the Cloud SQL Proxy Host from the Private Subnet in the Qubole Dedicated VPC
#
# This is for the following reason:
# 1. Qubole Control Plane will talk to the Cloud SQL Proxy via the Bastion Host
# 2. Qubole Clusters prefer having direct access to the Metastore instead of going through the Bastion(Latency) and hence need direct access to the proxy


"""Creates the firewall ingress rules for the Cloud SQL Proxy Host."""


def GenerateConfig(context):
    """Creates the firewall ingress rules for the Cloud SQL Proxy Host."""

    resources = [{
        'name': 'proxy-ingress-from-bastion',
        'type': 'compute.v1.firewall',
        'properties': {
            'network': '$(ref.cloud-sql-proxy-vpc.selfLink)',
            'sourceRanges': [context.properties['qubole_bastion_networkIP']],
            'targetTags': ['cloud-sql-proxy-host'],
            'allowed': [{
                'IPProtocol': 'TCP',
                'ports': [3306, 20557]
            }]
        }
    },
        {
            'name': 'proxy-ingress-from-private-subnet',
            'type': 'compute.v1.firewall',
            'properties': {
                'network': '$(ref.cloud-sql-proxy-vpc.selfLink)',
                'sourceRanges': [context.properties['qubole_vpc_subnet_cidr']],
                'targetTags': ['cloud-sql-proxy-host'],
                'allowed': [{
                    'IPProtocol': 'TCP',
                    'ports': [3306]
                }]
            }
        }
    ]
    return {'resources': resources}
