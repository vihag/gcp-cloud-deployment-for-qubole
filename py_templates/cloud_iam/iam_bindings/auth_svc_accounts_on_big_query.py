# Authorizes the Compute Service Account with
# 1. Big Query Data Viewer Role
#
# Authorizes the Instance Service Account with
# 1. Big Query Read Session User Role
#
# This is required so that once Qubole can
# 1. Show Big Query Datasets in the Workbench UI
# 2. Perform Data Preview on Big Query Datasets in the Workbench UI
# 3. Allow Spark Clusters to read data from Big Query
#
# References
# https://github.com/GoogleCloudPlatform/deploymentmanager-samples/issues/94
# https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/setIamPolicy
# https://cloud.google.com/iam/reference/rest/v1/Policy

"""Authorizes the Instance Service Account as a Big Query Read Session User. Authorizes the Compute Service Account as a Big Query Data Viewer"""

def GenerateConfig(context):
    """Authorizes the Instance Service Account as a Big Query Read Session User. Authorizes the Compute Service Account as a Big Query Data Viewer"""

    resources = [
        {
            'name': 'auth_isa_on_big_query',
            'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
            'properties': {
                'resource': context.env['project'],
                'role': 'roles/bigquery.readSessionUser',
                'member': 'serviceAccount:$(ref.qubole-instance-service-acc.email)'
            },
        },
        {
            'name': 'auth_csa_on_big_query',
            'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
            'properties': {
                'resource': context.env['project'],
                'role': 'roles/bigquery.dataViewer',
                'member': 'serviceAccount:$(ref.qubole-compute-service-acc.email)'
            },
        }
    ]
    return {'resources': resources}