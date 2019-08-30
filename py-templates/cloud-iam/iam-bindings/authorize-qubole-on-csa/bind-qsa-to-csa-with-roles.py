# Authorizes the Qubole Service Account (unique per customer per Qubole account) with
# 1. Service Account User Role
# 2. Service Account Token User Role
# on the Compute Service Account created in the customer's GCP Project
#
#
# References
# https://github.com/GoogleCloudPlatform/deploymentmanager-samples/issues/94
# https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/setIamPolicy
# https://cloud.google.com/iam/reference/rest/v1/Policy

"""Authorizes the Qubole Service Account as a user to the Compute Service Account."""

def GenerateConfig(context):
    """Authorize the QSA with serviceAccountUser and serviceAccountTokenCreator on CSA."""

    resources = [
        {
            'name': 'auth-qsa-to-csa-svc-acct-usr',
            'type': 'gcp-types/iam-v1:iam.projects.serviceAccounts.setIamPolicy',
            'properties': {
                'resource': 'serviceAccount:$(ref.qubole-compute-service-account.email)',
                'role': 'roles/iam.serviceAccountUser',
                'member': context.properties['qubole-service-account']
            },
            'metadata': {
                'dependsOn': ['$(ref.qubole-compute-service-account)']
            }
        },
        {
            'name': 'auth-qsa-to-csa-svc-acct-tkn-create',
            'type': 'gcp-types/iam-v1:iam.projects.serviceAccounts.setIamPolicy',
            'properties': {
                'resource': 'serviceAccount:$(ref.qubole-compute-service-account.email)',
                'role': 'roles/iam.serviceAccountTokenCreator',
                'member': context.properties['qubole-service-account']
            },
            'metadata': {
                'dependsOn': ['$(ref.qubole-compute-service-account)']
            }
        }
    ]
    return {'resources': resources}