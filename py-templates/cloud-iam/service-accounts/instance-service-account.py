# Qubole Orchestrates Compute Engine VMs on the customer's behalf into "clusters"
#
# Once Qubole has launched a cluster, it relinquishes control of the cluster to the cluster. The Compute Service Account hands the cluster
# to an Instance Service Account which is reponsible for Workload Aware Autoscaling as well access to private GCS buckets. For this, Qubole requires a
# second Service Account called the Instance Service Account
# This deployment template creates a "Instance Service Account" that can be passed to the clusters
#
# SA Templates - https://github.com/GoogleCloudPlatform/deploymentmanager-samples/blob/master/examples/v2/project_creation/service-accounts.py
# Env/Custom Variables - https://cloud.google.com/deployment-manager/docs/configuration/templates/use-environment-variables
# SA REST Reference - https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts


"""Creates the Instance Service Account to be used by Qubole to autoscale clusters."""

def GenerateConfig(context):
    """Creates the Instance Service Account."""

    resources = [
        {
            'name': 'qubole-instance-service-account',
            'type': 'iam.v1.serviceAccount',
            'metadata': {
                'dependsOn': context.properties['project']
            },
            'properties': {
                'projectId': context.properties['project'],
                'accountId': context.properties["accountId"],
                'displayName': context.properties["displayName"]
            }
        },
        {
            'name': 'bind-compute-role-to-isa',
            'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
            'properties': {
                'resource': context.properties['project'],
                'role': '$(ref.qubole-custom-compute-role)',
                'member': 'serviceAccount:$(ref.qubole-instance-service-account.email)'
            },
            'metadata': {
                'dependsOn': ['${ref.qubole-instance-service-account}', '${ref.qubole-custom-compute-role}', '${ref.qubole-custom-storage-role}']
            }
        },
        {
            'name': 'bind-storage-role-to-isa',
            'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
            'properties': {
                'resource': context.properties['project'],
                'role': '$(ref.qubole-custom-storage-role)',
                'member': 'serviceAccount:$(ref.qubole-instance-service-account.email)'
            },
            'metadata': {
                'dependsOn': ['${ref.qubole-instance-service-account}', '${ref.qubole-custom-compute-role}', '${ref.qubole-custom-storage-role}']
            }
        }
    ]
    return {'resources': resources}