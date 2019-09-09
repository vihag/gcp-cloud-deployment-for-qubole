# Authorize Compute Service Account and Instance Service Account to use
# 1. Qubole Custom Compute Role
#
#
# This is required so that once Qubole can use this role and its permissions to work with the compute engine in the customers GCP org,
#
# References
# https://github.com/GoogleCloudPlatform/deploymentmanager-samples/issues/94
# https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/setIamPolicy
# https://cloud.google.com/iam/reference/rest/v1/Policy
# https://github.com/GoogleCloudPlatform/cloud-foundation-toolkit/blob/master/dm/templates/iam_member/iam_member.py

"""Authorizes the Instance Service Account as a user to the Instance Service Account."""

def GenerateConfig(context):
    """Authorize the ISA with serviceAccountUser and serviceAccountTokenCreator on ISA."""
#TODO roles/servicenetworking.networksAdmin
#TODO roles/compute.networkAdmin
    resources = [
        {
            'name': 'bind_cloud_sql_to_proxy_sa_admin',
            'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
            'properties': {
                'resource': context.env['project'],
                #'role': '$(ref.cloud_sql_connect_role.name)',
                'role': 'roles/cloudsql.client',
                'member': 'serviceAccount:$(ref.cloud-sql-proxy-service-acc.email)'
            },
        }
    ]
    return {'resources': resources}