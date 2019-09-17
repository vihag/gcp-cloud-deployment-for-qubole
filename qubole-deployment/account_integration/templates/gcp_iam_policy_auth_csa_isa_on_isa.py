# Authorize the Instance Service Account and Compute Service Account (created for Qubole) as
# 1. Service Account User
# on the Instance Service Account (created for Qubole)
#
# This is for the following reason:
# 1. The compute service account is used to initialize the cluster minimum configuration
# 2. Once the minimum cluster is up, Qubole passes the job of handling the cluster lifecycle to the cluster itself
# 3. This means that the cluster needs to use the Instance Service Account role to spin more Vms and access data buckets
# 4. This ensures that Qubole can never access the customers Big Query Datasets and Cloud Storage Buckets


"""Authorizes the Instance Service Account and the Customer Service Account as a Service Account User to the Instance
Service Account. """

def GenerateConfig(context):
    """Authorizes the Instance Service Account and the Customer Service Account as a Service Account User to the
    Instance Service Account. """

    resources = [
        {
            'name': 'auth_csa_isa_on_isa',
            'type': 'gcp-types/iam-v1:iam.projects.serviceAccounts.setIamPolicy',
            'properties': {
                'resource': 'projects/'+context.env['project']+'/serviceAccounts/'+'$(ref.qubole-instance-service-acc'
                                                                                   '.uniqueId)',
                'policy': {
                    'bindings': [
                        {
                            'role': 'roles/iam.serviceAccountUser',
                            'members': ['serviceAccount:'+'$(ref.qubole-instance-service-acc.email)',
                                        'serviceAccount:'+'$(ref.qubole-compute-service-acc.email)']
                        }
                    ]
                }
            }
        }
    ]
    return {'resources': resources}
