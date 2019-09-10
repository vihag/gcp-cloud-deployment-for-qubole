# Creates a two way VPC peering between
# 1. The Qubole Dedicated VPC
# 2. The Cloud SQL Proxy Dedicated VPC
#
# This is for the reason:
# 1. Qubole can access the cloud SQL instance hosting the Hive Metastore in a secure and scalable fashion



""" Peer the Cloud SQL VPC Proxy with the Qubole Dedicated VPC for cluster access to metastore. """


def GenerateConfig(context):
    """Peer the Cloud SQL VPC Proxy with the Qubole Dedicated VPC for cluster access to metastore."""

    resources = [{
        'name': 'peer-cloudsql-proxy-qubole-vpc',
        'type': 'gcp-types/compute-v1:compute.networks.addPeering',
        'properties': {
            'name': 'peer-cloudsql-proxy-qubole-vpc',
            'network': '$(ref.cloud-sql-proxy-vpc.name)',
            'peerNetwork': '$(ref.qubole-dedicated-vpc.selfLink)',
            'autoCreateRoutes': True,
        }
    },
        {
            'name': 'peer-qubole-vpc-cloudsql-proxy',
            'type': 'gcp-types/compute-v1:compute.networks.addPeering',
            'properties': {
                'name': 'peer-qubole-vpc-cloudsql-proxy',
                'network': '$(ref.qubole-dedicated-vpc.name)',
                'peerNetwork': '$(ref.cloud-sql-proxy-vpc.selfLink)',
                'autoCreateRoutes': True,
            }
        }
    ]
    return {'resources': resources}