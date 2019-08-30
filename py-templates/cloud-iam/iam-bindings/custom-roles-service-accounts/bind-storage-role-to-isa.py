"""Attaches the Custom Storage Role to the Instance Service Account."""

def GenerateConfig(context):
    """Attaches the Custom Storage Role to the Instance Service Account."""

    resources = [
        {
            'name': 'bind-storage-role-to-isa',
            'type': 'gcp-types/iam-v1:iam.projects.serviceAccounts.setIamPolicy',
            'properties': {
                'role': '$(ref.qubole-custom-storage-role)',
                'resource': 'serviceAccount:$(ref.qubole-instance-service-account.email)'
            },
            'metadata': {
                'dependsOn': ['${ref.qubole-instance-service-account}', '${ref.qubole-custom-compute-role}', '${ref.qubole-custom-storage-role}']
            }
        }
    ]
    return {'resources': resources}