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

    resources = [
        {
            'name': 'bind_compute_role_to_comp_svc',
            'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
            'properties': {
                'resource': context.env['project'],
                'role': '$(ref.qubole_custom_compute_role.name)',
                'member': 'serviceAccount:$(ref.qubole-compute-service-acc.email)'
            },
        },
        {
            'name': 'bind_compute_role_to_inst_svc',
            'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
            'properties': {
                'resource': context.env['project'],
                'role': '$(ref.qubole_custom_compute_role.name)',
                'member': 'serviceAccount:$(ref.qubole-instance-service-acc.email)'
            },
        }
    ]
    return {'resources': resources}