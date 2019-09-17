# Authorizes the Compute Service Account & Instance Service account (created for Qubole) with
# 1. A custom storage role that allows working with Google Cloud Storage Buckets
#
# This is for the following reason:
# 1. Qubole uses the Compute Service Account to write logs, results to the Cloud Storage. The Instance Service Account to read data buckets through the engines. This requires Storage Permissions.
#
# Caveats:
# 1. It is the customers responsibility to authorize the custom storage role to the Instance Service Account  on the buckets that need to be accessed via the Qubole Clusters


"""Authorizes the Compute Service Account and Instance Service Account to be able to use the Custom Storage Role."""

def GenerateConfig(context):
    """Authorizes the Compute Service Account and Instance Service Account to be able to use the Custom Storage Role."""

    resources = [
        {
            'name': 'bind_storage_role_to_comp_svc',
            'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
            'properties': {
                'resource': context.env['project'],
                'role': '$(ref.qubole_custom_storage_role.name)',
                'member': 'serviceAccount:$(ref.qubole-compute-service-acc.email)'
            },
        },
        {
            'name': 'bind_storage_role_to_inst_svc',
            'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
            'properties': {
                'resource': context.env['project'],
                'role': '$(ref.qubole_custom_storage_role.name)',
                'member': 'serviceAccount:$(ref.qubole-instance-service-acc.email)'
            },
        }
    ]
    return {'resources': resources}
