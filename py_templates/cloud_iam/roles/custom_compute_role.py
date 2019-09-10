# Creates a Custom Role to work with Compute Engine to
# 1. Handle Compute resources like VMs, Disks, Addresses etc
# 2. Handle Network resources like firewalls and list VPCs
#
# This is for the following reason:
# 1. Qubole uses the custom Compute Role to list networks, create vms, create addresses, tag instances and pass IAM service accounts to other instances
#
# Caveats:
# 1. The customer should ensure that the listed permissions are not taken away as it might result in loss of functionality



"""Creates the Compute IAM Role to be used by Qubole to create and launch clusters."""

def GenerateConfig(context):
    """Creates the Compute IAM Role."""

    resources = [{
        'name': 'qubole_custom_compute_role',
        'type': 'gcp-types/iam-v1:projects.roles',
        'properties': {
            'parent': 'projects/'+context.env['project'],
            'roleId': context.properties["roleId"],
            'role': {
                'title': context.properties["title"],
                'description': context.properties["description"],
                'includedPermissions': ['compute.disks.create','compute.disks.delete','compute.disks.get','compute.disks.list','compute.disks.setLabels','compute.disks.use','compute.firewalls.create','compute.firewalls.delete','compute.firewalls.get','compute.firewalls.list','compute.firewalls.update','compute.instances.attachDisk','compute.instances.create','compute.instances.delete','compute.instances.detachDisk','compute.instances.get','compute.instances.list','compute.instances.reset','compute.instances.resume','compute.instances.setLabels','compute.instances.setMetadata','compute.instances.setServiceAccount','compute.instances.setTags','compute.instances.start','compute.instances.stop','compute.instances.suspend','compute.instances.use','compute.networks.updatePolicy','compute.networks.use','compute.networks.useExternalIp','compute.subnetworks.use','compute.subnetworks.useExternalIp','compute.regions.get','compute.networks.list','compute.subnetworks.list','compute.diskTypes.list']
            }

        }
    }]
    return {'resources': resources}