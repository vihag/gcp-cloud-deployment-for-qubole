# Authorizes the Compute Service Account with
# 1. Service Account User Role
# on the Instance Service Account
#
# This is required so that once Qubole has launched the cluster using the CSA,
# it can provide the cluster with the ISA which will be used to by the cluster
# to AutoScale and if required access data buckets, thus securing the data from Qubole access
#
# References
# https://github.com/GoogleCloudPlatform/deploymentmanager-samples/issues/94
# https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/setIamPolicy
# https://cloud.google.com/iam/reference/rest/v1/Policy

"""Authorizes the Compute Service Account as a user to the Compute Service Account."""

def GenerateConfig(context):
    """Authorize the CSA with serviceAccountUser and serviceAccountTokenCreator on ISA."""

    resources = [
        {
            'name': 'auth-csa-to-isa-svc-acct-usr',
            'type': 'gcp-types/iam-v1:iam.projects.serviceAccounts.setIamPolicy',
            'properties': {
                'resource': 'serviceAccount:$(ref.qubole-instance-service-account.email)',
                'role': 'roles/iam.serviceAccountUser',
                'member': '$(ref.qubole-compute-service-account)'
            },
            'metadata': {
                'dependsOn': ['$(ref.qubole-compute-service-account)', '$(ref.qubole-instance-service-account)']
            }
        }
    ]
    return {'resources': resources}