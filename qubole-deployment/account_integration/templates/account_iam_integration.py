"""Bring together all the elements required to complete Qubole Account Setup"""


def GenerateConfig(context):
    """Bring together all the elements required to complete Qubole Account Setup"""

    resources = [
        {
            'name': 'qubole_custom_compute_role',
            'type': 'gcp_iam_role_custom_compute_role.py',
            'properties': {
                'deployment-suffix': context.properties['deployment-suffix']
            }
        }, {
            'name': 'qubole_custom_storage_role',
            'type': 'gcp_iam_role_custom_storage_role.py',
            'properties': {
                'deployment-suffix': context.properties['deployment-suffix']
            }
        },
        {
            'name': 'qubole_compute_service_account',
            'type': 'gcp_iam_sa_compute_service_account.py'
        }, {
            'name': 'qubole_instance_service_account',
            'type': 'gcp_iam_sa_instance_service_account.py'
        }, {
            'name': 'bind_compute_role_to_svc_accounts',
            'type': 'gcp_iam_binding_compute_role_to_svc_accounts.py'
        }, {
            'name': 'bind_storage_role_to_svc_accounts',
            'type': 'gcp_iam_binding_storage_role_to_svc_accounts.py'
        }, {
            'name': 'authorize_qsa_on_csa',
            'type': 'gcp_iam_policy_auth_qsa_on_csa.py',
            'properties': {
                'qubole-service-account': context.properties['qubole-service-account']
            }
        }, {
            'name': 'authorize_csa_isa_on_isa',
            'type': 'gcp_iam_policy_auth_csa_isa_on_isa.py'
        }, {
            'name': 'qubole_defloc',
            'type': 'gcp_storage_bucket_qubole_defloc.py',
            'properties': {
                'deployment-suffix': context.properties['deployment-suffix']
            }
        }, {
            'name': 'bind_auth_svc_accounts_on_big_query',
            'type': 'gcp_iam_binding_auth_svc_accounts_on_big_query.py'
        }]
    return {'resources': resources}
