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
    # TODO create custom roles that don't require full admin for service networking and compute(vpc peering)
    # TODO wait for service networking to be registered as a gcp type to avoid providing a computeVM with these powers
    resources = [
        {
            'name': 'auth_cloud_sql_client_to_cloud_sql_proxy_sa',
            'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
            'properties': {
                'resource': context.env['project'],
                'role': 'roles/cloudsql.client',
                'member': 'serviceAccount:$(ref.cloud-sql-proxy-service-acc.email)'
            },
        }
        # {
        #     'name': 'auth_svc_networking_to_cloud_sql_proxy_sa',
        #     'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
        #     'properties': {
        #         'resource': context.env['project'],
        #         'role': 'roles/servicenetworking.networksAdmin',
        #         'member': 'serviceAccount:$(ref.cloud-sql-proxy-service-acc.email)'
        #     },
        # },
        # {
        #     'name': 'auth_compute_networking_to_cloud_sql_proxy_sa',
        #     'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
        #     'properties': {
        #         'resource': context.env['project'],
        #         'role': 'roles/compute.networkAdmin',
        #         'member': 'serviceAccount:$(ref.cloud-sql-proxy-service-acc.email)'
        #     },
        # }
    ]
    return {'resources': resources}