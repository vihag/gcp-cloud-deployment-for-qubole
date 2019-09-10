# Creates a Custom Role to work with Google Cloud Storage to
# 1. To save logs, results and command histories for clusters and queries
# 2. To save notebooks and virtual environments for when clusters terminate and are brought back online
#
# This is for the following reason:
# 1. Qubole periodically syncs all logs, results and resources to GCS so that in case of service outages or cluster terminations, the resources are still available
#
# Caveats:
# 1. The customer should ensure that the listed permissions are not taken away as it might result in loss of functionality


"""Creates the Storage IAM Role to be used by Qubole to save activities onto GCS."""

def GenerateConfig(context):
    """Creates the Storage IAM Role."""

    resources = [{
        'name': 'qubole_custom_storage_role',
        'type': 'gcp-types/iam-v1:projects.roles',
        'properties': {
            'parent': 'projects/'+context.env['project'],
            'roleId': context.properties["roleId"],
            'role': {
                'title': context.properties["title"],
                'description': context.properties["description"],
                'includedPermissions': ['storage.buckets.get','storage.buckets.getIamPolicy','storage.buckets.list','storage.objects.create','storage.objects.delete','storage.objects.get','storage.objects.getIamPolicy','storage.objects.list','storage.objects.setIamPolicy']
            }

        }
    }]
    return {'resources': resources}