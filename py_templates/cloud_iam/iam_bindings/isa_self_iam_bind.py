# Authorizes the Instance Service Account with
# 1. Service Account User Role
# on the Instance Service Account
#
# This is required so that once Qubole has handed the ISA to the cluster,
# the cluster can spawn new VMs and pass ISA to them in the event of workload aware AutoScaling
#
# References
# https://github.com/GoogleCloudPlatform/deploymentmanager-samples/issues/94
# https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/setIamPolicy
# https://cloud.google.com/iam/reference/rest/v1/Policy

"""Authorizes the Instance Service Account as a user to the Instance Service Account."""

def GenerateConfig(context):
    """Authorize the ISA with serviceAccountUser and serviceAccountTokenCreator on ISA."""

    resources = [
        {
            'name': 'auth_isa_on_itself',
            'type': 'gcp-types/iam-v1:iam.projects.serviceAccounts.setIamPolicy',
            'properties': {
                'resource': 'projects/'+context.env['project']+'/serviceAccounts/'+'$(ref.qubole-instance-service-acc.email)',
                'policy': {
                    'bindings': [
                        {
                            'role': 'roles/iam.serviceAccountUser',
                            'members': ['serviceAccount:'+'$(ref.qubole-instance-service-acc.email)']
                        }
                    ]
                }
            }
        }
    ]
    return {'resources': resources}