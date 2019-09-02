# Qubole Orchestrates Compute Engine VMs on the customer's behalf into "clusters"
#
# To create and launch "Clusters", Qubole requires Compute IAM credentials
# This deployment template creates a "Compute Service Account" that can be passed to Qubole
#
# SA Templates - https://github.com/GoogleCloudPlatform/deploymentmanager-samples/blob/master/examples/v2/project_creation/service-accounts.py
# Env/Custom Variables - https://cloud.google.com/deployment-manager/docs/configuration/templates/use-environment-variables
# SA REST Reference - https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts
# IAM Bindings to add roles: https://stackoverflow.com/a/55961393/7194982
# Making references in templates: https://cloud.google.com/deployment-manager/docs/configuration/use-references?hl=ru#making_references_in_templates


"""Creates the Compute Service Account to be used by Qubole to create and launch clusters."""

def GenerateConfig(context):
    """Creates the Compute Service Account."""

    resources = [
        {
            'name': 'qubole-compute-service-acc',
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
                            'member': 'serviceAccount:'+context.properties['qubole-service-account']
                        },
                        {
                            'role': 'roles/iam.serviceAccountTokenCreator',
                            'member': 'serviceAccount:'+context.properties['qubole-service-account']
                        }
                    ]
                }
            }
        }
    ]
    return {'resources': resources}