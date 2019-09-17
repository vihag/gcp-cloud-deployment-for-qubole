"""Bring together all the elements required to setup a Hive Metastore with Qubole"""


def GenerateConfig(context):
    """Bring together all the elements required to setup a Hive Metastore with Qubole"""

    resources = [{
        'name': 'cloud_sql_proxy_network',
        'type': 'gcp_compute_network_cloud_sql_proxy.py'
    }, {
        'name': 'cloud_sql_proxy_subnetwork',
        'type': 'gcp_compute_subnetwork_cloud_sql_proxy_subnet.py',
        'properties': {
            'region': context.properties['region']
        }
    }, {
        'name': 'cloud_sql_proxy_host_external_address',
        'type': 'gcp_compute_address_cloud_sql_proxy_ext.py',
        'properties': {
            'region': context.properties['region']
        }
    }, {
        'name': 'cloud_sql_proxy_host_internal_address',
        'type': 'gcp_compute_address_cloud_sql_proxy_int.py',
        'properties': {
            'region': context.properties['region']
        }
    }, {
        'name': 'cloud_sql_proxy_network_private_internal_range',
        'type': 'gcp_compute_address_cloudsql_int_range.py',
        'properties': {
            'region': context.properties['region']
        }
    }, {
        'name': 'cloud_sql_proxy_ingress_rules',
        'type': 'gcp_compute_firewall_cloud_sql_proxy_ingress.py',
        'properties': {
            'qubole_vpc_subnet_cidr': context.properties['qubole_vpc_subnet_cidr'],
            'qubole_bastion_networkIP': context.properties['qubole_bastion_networkIP']
        }
    }, {
        'name': 'cloud_sql_proxy_host',
        'type': 'gcp_compute_instance_cloud_sql_proxy.py',
        'properties': {
            'zone': context.properties['zone'],
            'region': context.properties['region'],
            'proxy-vm-type': context.properties['proxy-vm-type'],
            'deployment-suffix': context.properties['deployment-suffix']
        }
    }, {
        'name': 'cloud_sql_proxy_service_account',
        'type': 'gcp_iam_sa_cloud_sql_proxy.py'
    }, {
        'name': 'peer_sql_proxy_qubole_vpc_networks',
        'type': 'gpc_compute_network_peering_sql_proxy_qubole_vpc.py',
        'properties': {
            'qubole-dedicated-vpc': context.properties['qubole-dedicated-vpc']
        }
    }, {
        'name': 'bind_cloud_proxy_svc_account',
        'type': 'gcp_iam_binding_cloud_proxy_svc_account.py'
    }, {
        'name': 'hive_metastore',
        'type': 'gcp_sql_db_hive_metastore.py',
        'properties': {
            'region': context.properties['region'],
            'db_tier': context.properties['db_tier'],
            'zone': context.properties['zone'],
            'deployment-suffix': context.properties['deployment-suffix'],
            'db_root_password': context.properties['db_root_password'],
            'hive_user_name': context.properties['hive_user_name'],
            'hive_user_password': context.properties['hive_user_password'],
            'hive_schema_file': context.properties['hive_schema_file']
        }
    }
    ]
    return {'resources': resources}
