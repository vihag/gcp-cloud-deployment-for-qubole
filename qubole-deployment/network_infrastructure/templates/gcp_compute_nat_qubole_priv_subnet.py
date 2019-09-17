# Creates a GCP Cloud NAT, using a GCP Cloud Router to aggregate/group the NAT configuration options
# It creates
# 1. A Cloud Router Resource (only as an aggregator of the various NATs being configured)
# 2. A Cloud NAT instance that is associated with the private subnetwork in the Qubole Dedicated VPC
# 3. The IP allocation is automatic as Qubole Clusters autoscale very rapidly and manually sizing static IP addresses for NAT is not scalable
#
# This is for the following reason:
# 1. Secure designs will require bringing up Qubole clusters without Public IP addresses
# 2. Having a Cloud NAT allows outbound communication from the Qubole Clusters as needed
#
# Cloud NAT is not a physical device, it is only a configuration that provides NAT configuration to VMs and the VMs do the NAT by themselves
# Hence this is highly scalable. Please see https://cloud.google.com/nat/docs/overview#under_the_hood


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
                    # Associate Specific Subnets with NAT Usage
                    'sourceSubnetworkIpRangesToNat': 'LIST_OF_SUBNETWORKS',
                    'natIpAllocateOption': 'AUTO_ONLY',
                    'subnetworks': [
                        {
                            # Public Subnet only has the bastion, which requires to broadcast an External IP
                            'name': '$(ref.qu-vpc-private-subnetwork.selfLink)'
                        }
                    ]
                }
            ]
        }
    }]
    return {'resources': resources}
