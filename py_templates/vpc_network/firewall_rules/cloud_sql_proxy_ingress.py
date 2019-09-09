"""Creates the firewall ingress rules for the Cloud SQL Proxy Host."""


def GenerateConfig(unused_context):
    """Creates the firewall."""

    resources = [{
        'name': 'proxy-ingress-from-bastion',
        'type': 'compute.v1.firewall',
        'properties': {
            'network': '$(ref.cloud-sql-proxy-vpc.selfLink)',
            'sourceRanges': ['$(ref.qubole-bastion-host.networkInterfaces[0].networkIP)'],
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
                'sourceRanges': ['$(ref.qu-vpc-private-subnetwork.ipCidrRange)'],
                'targetTags': ['cloud-sql-proxy-host'],
                'allowed': [{
                    'IPProtocol': 'TCP',
                    'ports': [3306]
                }]
            }
        }
    ]
    return {'resources': resources}