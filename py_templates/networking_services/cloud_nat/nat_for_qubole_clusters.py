# Create an NAT Gateway to be attached to the public subnet of the VPC network
# The default route of the VPC Subnetwork will be overwritten by the rules and routes
# to this NAT Gateway
#
# The NAT will be used only if the VMs come up without an external IP.
# If an external IP is present, it's usage will take precedence combined with the default route
# Reference https://github.com/GoogleCloudPlatform/deploymentmanager-samples/blob/f6bc786d99ac3883ecde37cdafb24ebba2e0c1c1/community/cloud-foundation/templates/cloud_nat/cloud_nat.py


"""Create aNAT Gateway and Router to be attached to the Qubole Dedicated VPC for routing traffic to internet."""

def GenerateConfig(context):
    """Create aNAT Gateway and Router to be attached to the Qubole Dedicated VPC for routing traffic to internet."""

    resources = [{
        'name': 'nat-router-for-qubole-clusters',
        'type': 'compute.v1.router',
        'properties': {
            'network': '$(ref.qubole-dedicated-vpc.selfLink)',
            'region': context.properties['region'],
            'nats': [
                {
                    'name': 'nat-for-qubole-clusters',
                    'sourceSubnetworkIpRangesToNat': 'LIST_OF_SUBNETWORKS', #Associate Specific Subnets with NAT Usage
                    'natIpAllocateOption': 'AUTO_ONLY',
                    'subnetworks': [
                        {
                            'name': '$(ref.qu-vpc-private-subnetwork.selfLink)' #Public Subnet only has the bastion, which requires to broadcast an External IP
                        }
                    ]
                }
            ]
        }
    }]
    return {'resources': resources}