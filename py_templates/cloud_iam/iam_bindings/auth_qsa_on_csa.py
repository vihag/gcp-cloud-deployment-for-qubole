# Authorizes the Qubole Service Account with
# 1. Service Account User Role
# 2. Service Account Token Creator Role
# on the Compute Service Service Account
#
# This is required so that once Qubole assume the CS role, create a cluster, and if possible create tokens to access other services,
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
            'name': 'auth_qsa_on_csa',
            'type': 'gcp-types/iam-v1:iam.projects.serviceAccounts.setIamPolicy',
            'properties': {
                'resource': 'projects/'+context.env['project']+'/serviceAccounts/'+'$(ref.qubole-compute-service-acc.uniqueId)',
                'policy': {
                    'bindings': [
                        {
                            'role': 'roles/iam.serviceAccountUser',
                            'members': ['serviceAccount:'+context.properties['qubole-service-account']]
                        },
                        {
                            'role': 'roles/iam.serviceAccountTokenCreator',
                            'members': ['serviceAccount:'+context.properties['qubole-service-account']]
                        }
                    ]
                }
            }
        }
    ]
    return {'resources': resources}