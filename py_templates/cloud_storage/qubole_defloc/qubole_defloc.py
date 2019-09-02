# Qubole keeps all customer data in the customer's GCP project. Nothing comes back to Qubole
#
# This data includes
# 1. Cluster Start/Scale Logs
# 2. Engine Logs
# 3. Results
# 4. Notebooks
# 5. Py/R environments
#
# To be able to store this, Qubole requires a dedicated bucked in GCS henceforth called as "defloc"
# This template creates such a bucket
#
# References
# https://github.com/GoogleCloudPlatform/deploymentmanager-samples/blob/master/community/cloud-foundation/templates/gcs_bucket/gcs_bucket.py
#


"""Creates the Qubole Default Location(defloc)."""

def GenerateConfig(context):
    """Creates the Qubole Default Location(defloc)."""

    resources = [
        {
            'name': context.properties['org']+''+'_qubole_defloc',
            'type': 'storage.v1.bucket',
            'properties': {
                'projectId': context.properties['project'],
                'location': 'asia-southeast1'
            },
            'accessControl':{
                'gcpIAMPolicy': {
                    'bindings': [
                        {
                            'role': '$(ref.qubole_custom_storage_role)',
                            'members': ['serviceAccount:$(ref.qubole-compute-service-acc.email)', 'serviceAccount:$(ref.qubole-instance-service-acc.email)']
                        }
                    ]
                }
            }
        }
    ]

    return {'resources': resources}