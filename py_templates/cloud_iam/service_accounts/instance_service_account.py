# Creates a Custom Service Account that will be used by Qubole to
# 1. Provide the VMs with the Instance Service Account for further autoscaling and cluster life cycle management
# 2. Prove the VMs with credentials to access sensitive resources like GCS Data Buckets and Big Query Datasets without exposing them to Qubole
#
# This is for the following reason:
# 1. Qubole uses the custom Instance Role to give clusters self managing capabilities for autoscaling and lifecycle management
# 2. The Custom Compute Role is bound to the Instance Service Account
#
# Caveats
# 1. Ensure that instance service account is IAM authorized to sensitive data buckets and big query datasets if the workloads running on the cluster require access to them


"""Creates the Instance Service Account to be used by Qubole to autoscale clusters."""

def GenerateConfig(context):
    """Creates the Instance Service Account."""

    resources = [
        {
            'name': 'qubole-instance-service-acc',
            'type': 'iam.v1.serviceAccount',

            'properties': {
                'projectId': context.env['project'],
                'accountId': context.properties['accountId'],
                'displayName': context.properties['displayName']
            },
        }

    ]
    return {'resources': resources}