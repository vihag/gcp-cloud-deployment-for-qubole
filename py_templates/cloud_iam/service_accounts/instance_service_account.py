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
            'name': 'qubole-instance-service-acc',
            'type': 'iam.v1.serviceAccount',

            'properties': {
                'projectId': context.env['project'],
                'accountId': context.properties['accountId'],
                'displayName': context.properties['displayName']
            },

            'accessControl':{
                'gcpIAMPolicy': {
                    'bindings': [
                        {
                            'role': '$(ref.qubole_custom_storage_role.selfLink)'
                        },
                        {
                            'role': '$(ref.qubole_custom_compute_role.selfLink)'
                        },
                        {
                            'role': 'roles/iam.serviceAccountUser',
                            'member': 'serviceAccount:$(ref.qubole-compute-service-acc.email)'
                        }
                    ]
                }
            }
        }

    ]
    return {'resources': resources}