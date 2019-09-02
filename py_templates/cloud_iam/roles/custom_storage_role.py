# Qubole Orchestrates Compute Engine VMs on the customer's behalf into "clusters"
# Qubole saves all audit, logs, results, notebooks, environments onto a Qubole designated bucket in the customer's project
#
# To be able to do so, Qubole requires Storage IAM credentials on a desginated bucket
# This deployment template creates a "Storage Role" that can be passed to Qubole
#
# It is important to not be more restrictive than the permissions listed in this template
#
# Role Templates - https://cloud.google.com/iam/docs/maintain-custom-roles-deployment-manager
# Env/Custom Variables - https://cloud.google.com/deployment-manager/docs/configuration/templates/use-environment-variables
#


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