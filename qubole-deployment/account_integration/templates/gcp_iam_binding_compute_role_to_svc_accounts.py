# Authorizes the Compute Service Account & Instance Service account (created for Qubole) with
# 1. A custom compute role that allows the Service Account to manage VMs for orchestrating clusters
#
# This is for the following reason:
# 1. Qubole uses the Compute and Instance Service Accounts to perform Complete Cluster LifeCycle Management and Autoscaling. This requires Compute Permissions


"""Authorizes the Compute Service Account and Instance Service Account to be able to use the Custom Compute Role."""

def GenerateConfig(context):
    """Authorizes the Compute Service Account and Instance Service Account to be able to use the Custom Compute Role."""

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
