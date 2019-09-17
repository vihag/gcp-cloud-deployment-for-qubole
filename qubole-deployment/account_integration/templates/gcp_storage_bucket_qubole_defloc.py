# Creates a Google Cloud Storage Bucket that will act as the "default location" for the Qubole account
# Qubole saves
# 1. Cluster Start/Scale Logs
# 2. Engine Logs
# 3. Results
# 4. Notebooks
# 5. Py/R environments
# in this location
#
# This is for the following reason:
# 1. Qubole performs Cluster Lifecycle Management. Which means it terminates idle clusters, downscales VMs to save cost and recreates clusters in catastrophic failures
# 2. Qubole also makes available the logs, results, command histories, command UIs offline (and indefinetly)
# 3. Qubole achieves this by storing all the above data in the defloc and loading it when the user requests for it
#
# Caveats:
# 1. Deleting content from this location can have unintended consequences on the platform including loss of work and data
# 2. Consult Qubole Support before moving this location


"""Creates the Qubole Default Location(defloc)."""

def GenerateConfig(context):
    """Creates the Qubole Default Location(defloc)."""

    resources = [
        {
            'name': 'qubole_defloc_'+context.properties['deployment-suffix'],
            'type': 'storage.v1.bucket',
            'properties': {
                'projectId': context.env['project'],
                'location': 'asia-southeast1'
            },
            'accessControl':{
                'gcpIAMPolicy': {
                    'bindings': [
                        {
                            'role': '$(ref.qubole_custom_storage_role.selfLink)',
                            'members': [
                                        'serviceAccount:$(ref.qubole-compute-service-acc.email)',
                                        'serviceAccount:$(ref.qubole-instance-service-acc.email)'
                            ]
                        }
                    ]
                }
            }
        }
    ]

    return {'resources': resources}
