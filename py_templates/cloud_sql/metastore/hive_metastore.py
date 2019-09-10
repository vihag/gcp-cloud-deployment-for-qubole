# Creates a Cloud SQL Instance to host the Hive Metastore. It
# 1. Creates a 2nd Gen, MySQL 5.7 instance in the specified region and zone
# 2. Creates a database/schema called hive which will act as the Hive Metastore
# 3. Updates the password for the root user
# 4. Creates a user called hive_user which will be used by Qubole to access the Hive Metastore
# 5. Initializes the hive database with the required tables for it to be a functional Hive Metastore
#
# This is for the following reason:
# 1. Qubole requires a Hive Metastore configured for the account so that the engines can be seamlessly integrated with the metastore
# 2. Qubole provides a hosted metastore, but more often than not, for security and scalability reasons, customers will want to host their own metastore
#
# Caveats:
# 1. Given the networking architecture of Cloud SQL, there are two possibilities of connecting.
#       i. Public IP networking
#            - this requires that we whitelist an external IP to be able to access the Cloud SQL instance
#            - this creates a problem for Qubole as we need to whitelist an entire subnetwork(private subnetwork) to the CloudSQL instance.
#            - in this case, the solution is to setup Google's Cloud SQL proxy infront of the Cloud SQL instance. Since the proxy is hosted on either GCE or GKS, we can not whitelist the subnets
#       ii. Private IP networking
#            - with Private IP networking, we are limited to setting up the private IP networking with one and only one VPC.
#            - the standard pattern hence would be setting up a VPC with a Cloud SQL proxy and setting up private IP networking between them
#            - this opens the possibility of peering Qubole's VPC with the VPC of the proxy and transitively getting access to the Cloud SQL instance
#            - the private IP method is faster and more secure
#            - However, since Service Networking API is not available for Cloud Deployment Manager, we can't setup Private IP perring in this template
#            TODO keep an eye out on when Service Networking becomes a publicly available gcp type and remove the public IP peering between this metastore and the proxy

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