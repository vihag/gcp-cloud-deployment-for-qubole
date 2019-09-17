# Creates a Custom Service Account that will be used by Qubole to
# 1. Get access to the custom compute role for creating the cluster minimum configuration
# 2. Provide the VMs with the Instance Service Account for further autoscaling and cluster life cycle management
#
# This is for the following reason:
# 1. Qubole uses the custom Compute Role to list networks, create vms, create addresses, tag instances and pass IAM service accounts to other instances
# 2. The Custom Compute Role is bound to the Compute Service Account and hence made available to Qubole
#
# Caveats
# 1. Ensure that this service account does not have IAM permissions to sensitive resources like GCS data buckets or Big Query Read permissions.


"""Creates the Compute Service Account to be used by Qubole to create and launch clusters."""

def GenerateConfig(context):
    """Creates the Compute Service Account."""

    resources = [
        {
            'name': 'qubole-compute-service-acc',
            'type': 'iam.v1.serviceAccount',

            'properties': {
                'projectId': context.env['project'],
                'accountId': 'qubole-compute-service-acc',
                'displayName': 'qubole-compute-service-acc'
            },
        }
    ]
    return {'resources': resources}
