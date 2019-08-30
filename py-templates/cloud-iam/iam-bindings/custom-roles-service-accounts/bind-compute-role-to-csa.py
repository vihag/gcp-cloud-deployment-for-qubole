"""Attaches the Custom Compute Role to the Compute Service Account."""

def GenerateConfig(context):
    """Attaches the Custom Compute Role to the Compute Service Account."""

    resources = [
        {
            'name': 'bind-compute-role-to-csa',
            'type': 'gcp-types/iam-v1:iam.projects.serviceAccounts.setIamPolicy',
            'properties': {
                'role': '$(ref.qubole-custom-compute-role)',
                'resource': 'serviceAccount:$(ref.qubole-compute-service-account.email)'
            },
            'metadata': {
                'dependsOn': ['${ref.qubole-compute-service-account}', '${ref.qubole-custom-compute-role}', '${ref.qubole-custom-storage-role}']
            }
        }
    ]
    return {'resources': resources}