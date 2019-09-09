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


"""Creates the Service Account to be used by the Cloud SQL Proxy to create a Gateway to the Cloud SQL with Hive Metastore."""

def GenerateConfig(context):
    """Creates the Service Account to be used by the Cloud SQL Proxy to create a Gateway to the Cloud SQL with Hive Metastore."""

    resources = [
        {
            'name': 'cloud-sql-proxy-service-acc',
            'type': 'iam.v1.serviceAccount',

            'properties': {
                'projectId': context.env['project'],
                'accountId': 'cloud-sql-proxy-service-acc',
                'displayName': 'cloud-sql-proxy-service-acc',
            },
        }
    ]
    return {'resources': resources}