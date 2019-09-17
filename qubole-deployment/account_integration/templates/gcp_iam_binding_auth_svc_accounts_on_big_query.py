# Authorizes the Compute Service Account with
# 1. Big Query Data Viewer Role
#
# Authorizes the Instance Service Account with
# 1. Big Query Read Session User Role
#
# This is for the following reason:
# 1. The workbench UI uses the Compute Service Account to list the available Big Query Datasets
# 2. The workbench UI uses the Compute Service Account to provide data preview on the available Big Query Datasets
# 3. The Spark Clusters(via the Notebook and Workbench) uses the Instance Service Account to read Big Query Datasets
#
# Caveats
# 1. It is the customers responsibility to authorize the Instance Service Account as a Data Viewer on the Individual Big Query Datasets
# 2. This is because(as per docs):
#                               When applied to a dataset, dataViewer provides permissions to:
#                                   i. Read the dataset's metadata and to list tables in the dataset.
#                                   ii. Read data and metadata from the dataset's tables.
#                               When applied at the project or organization level, this role can also
#                                   i. enumerate all datasets in the project.
#                                   ii. Additional roles, however, are necessary to allow the running of jobs.


"""Authorizes the Instance Service Account as a Big Query Read Session User. Authorizes the Compute Service Account
as a Big Query Data Viewer """

def GenerateConfig(context):
    """Authorizes the Instance Service Account as a Big Query Read Session User. Authorizes the Compute Service
    Account as a Big Query Data Viewer """

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
