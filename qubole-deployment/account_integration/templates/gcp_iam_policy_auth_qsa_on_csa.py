# Authorizes the Qubole Service Account with
# 1. Service Account User Role
# 2. Service Account Token Creator Role
# on the Compute Service Service Account
#
# This is for the following reason:
# 1. The compute service account is used to initialize the cluster minimum configuration
# 2. Qubole creates a service account for every customer Qubole account - this is the Qubole Service Account
# 3. Once the Qubole Service Account is authorized to use the compute service account, it uses it to initialize the cluster minimum configuration
# 4. Service Account Credentials expire every 1 hour, hence Qubole Service Account requires token creator roles to be able to perform administrative tasks on the cluster

"""Authorizes the Qubole Service Account as a Service Account User & Service Account Token Creator to the Compute
Service Account. """

def GenerateConfig(context):
    """Authorizes the Qubole Service Account as a Service Account User & Service Account Token Creator to the Compute
    Service Account. """

    resources = [
        {
            'name': 'auth_qsa_on_csa',
            'type': 'gcp-types/iam-v1:iam.projects.serviceAccounts.setIamPolicy',
            'properties': {
                'resource': 'projects/'+context.env['project']+'/serviceAccounts/'+'$(ref.qubole-compute-service-acc'
                                                                                   '.uniqueId)',
                'policy': {
                    'bindings': [
                        {
                            'role': 'roles/iam.serviceAccountUser',
                            'members': ['serviceAccount:'+context.properties['qubole-service-account']]
                        },
                        {
                            'role': 'roles/iam.serviceAccountTokenCreator',
                            'members': ['serviceAccount:'+context.properties['qubole-service-account']]
                        }
                    ]
                }
            }
        }
    ]
    return {'resources': resources}
