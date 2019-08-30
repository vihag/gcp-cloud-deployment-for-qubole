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

    resources = [{
        'name': 'qubole-defloc',
        'type': 'gcp-types/storage.v1.bucket',
        'properties': {
            'project': context.properties['project'],
            'name': ''.join(context.properties['org'])
        },
        'accessControl':{
            'gcpIAMPolicy': {
                'bindings': [
                    {
                        'role': '$(ref.qubole-custom-storage-role)',
                        'members': ['serviceAccount:$(ref.qubole-compute-service-account.email)', 'serviceAccount:$(ref.qubole-instance-service-account.email)']
                    }
                ]
            }
        }
    }]
    return {'resources': resources}