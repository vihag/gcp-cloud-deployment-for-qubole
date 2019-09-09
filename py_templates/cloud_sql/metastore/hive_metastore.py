# Qubole promotes the "Data Lake" architecture.
# This means, all the data(structured/ unstructured) is placed onto the public cloud's blob storage. This would be GCS in GCP
# The data is then exposed to end users for easy consumption via a Metastore.
# Qubole works with a MySQL based Hive Metastore
#
# This template will spin up a MySQL based CloudSQL instance, with private IP link to the Qubole Dedicated VPC
#
# Further, it will initialize the CloudSQL instance with a Database called HIVE, and populate the required tables for it to function as a metastore
# Further, it will initialize a user of this database with appropriate credentials for Qubole to connect to it securely
#
# References
# https://github.com/GoogleCloudPlatform/deploymentmanager-samples/tree/master/examples/v2/cloudsql_import
# https://github.com/GoogleCloudPlatform/deploymentmanager-samples/blob/master/examples/v2/cloudsql/cloudsql.jinja
# https://cloud.google.com/sql/docs/mysql/admin-api/v1beta4/instances/import
# https://cloud.google.com/sql/docs/mysql/admin-api/v1beta4/instances/insert
#
# Requires Service Networking API
def GenerateConfig(context):
    """Creates the MySQL based Hive Metastore."""

    resources = [
        {
            'name': context.properties['org']+'-metastore-inst',
            'type': 'sqladmin.v1beta4.instance',
            'properties': {
                'region': context.properties['region'],
                'backendType': 'SECOND_GEN',
                'instanceType': 'CLOUD_SQL_INSTANCE',
                'databaseVersion': 'MYSQL_5_7',
                'settings': {
                    'tier': context.properties['tier'],
                    'ipConfiguration': {
                        'authorizedNetworks': [
                        ]
                    },
                    'locationPreference': {
                        'zone': context.properties['zone'],
                    },
                    'activationPolicy': 'ALWAYS'
                }
            }
        },
        {   # TODO figure out how to wait for the metastore instance to come online
            'name': 'hive_metastore_db',
            'type': 'sqladmin.v1beta4.database',
            'properties': {
                'project': context.env['project'],
                'name': 'hive',
                'instance': '$(ref.'+context.properties['org']+'-metastore-inst.name)'
            },
            'metadata': {
                'dependsOn': [context.properties['org']+'-metastore-inst', 'cloud-sql-instance-root-user']
            }
        },
        {
            'name': 'cloud-sql-instance-root-user',
            'type': 'sqladmin.v1beta4.user',
            'properties': {
                'name': 'root',
                'host': '%',
                'instance': '$(ref.'+context.properties['org']+'-metastore-inst.name)',
                'password': context.properties['root_password']
            },
            'metadata': {
                'dependsOn': [context.properties['org']+'-metastore-inst']
            }
        },
        {
            'name': 'hive-metastore-user',
            'type': 'sqladmin.v1beta4.user',
            'properties': {
                'name': context.properties['hive_user_name'],
                'host': '%',
                'instance': '$(ref.'+context.properties['org']+'-metastore-inst.name)',
                'password': context.properties['hive_user_password']
            },
            'metadata': {
                'dependsOn': [context.properties['org']+'-metastore-inst', 'hive_metastore_db']
            }
        },
        {
            'name': 'hive-metastore-init',
            'type': 'gcp-types/sqladmin-v1beta4:sql.instances.import',
            'properties': {
                'instance': '$(ref.'+context.properties['org']+'-metastore-inst.name)',
                'importContext': {
                    'kind': 'sql#importContext',
                    'fileType': 'SQL',
                    'database': '$(ref.hive_metastore_db.name)',
                    'uri': context.properties['hive_schema_file']
                }
            },
            'metadata': {
                'dependsOn': [context.properties['org']+'-metastore-inst', 'hive_metastore_db', 'hive-metastore-user']
            }
        }
    ]
    return {'resources': resources}