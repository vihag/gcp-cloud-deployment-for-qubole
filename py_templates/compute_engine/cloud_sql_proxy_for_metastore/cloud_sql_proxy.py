# Cloud SQL Admin API Required

def getBootstrapAsArray(cloud_sql_instance_name):

    return ''.join([
        '#!/bin/bash\n',
        'cd ~\n'
        'mkdir cloudsql\n'
        'mkdir cloudsqldir\n'
        'cd cloudsql\n'
        'wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy\n',
        'chmod +x cloud_sql_proxy\n',
        #'gcloud iam service-accounts keys create key.json --iam-account='+service_account+'\n',
        #'export GOOGLE_APPLICATION_CREDENTIALS=key.json\n'
        './cloud_sql_proxy -instances='+cloud_sql_instance_name+'=tcp:0.0.0.0:3306 &> /tmp/cloud_sql_proxy.log\n',
        #./cloud_sql_proxy -dir ../cloudsqldir -instances_metadata='+cloud_sql_instance_name+'=tcp:0.0.0.0:3306 &> /tmp/cloud_sql_proxy.log\n'
    ])

def GenerateConfig(context):
    """Creates the cloud SQL proxy host for connections to the Hive Metastore."""

    resources = [{
        'name': 'cloud-sql-proxy-host',
        'type': 'compute.v1.instance',
        'properties': {
            'zone': context.properties['zone'],
            'machineType': '/zones/'+context.properties['zone']+'/machineTypes/'+context.properties['machineType'],
            'canIpForward': True,
            'tags': {
                'items': [
                    'cloud-sql-proxy-host'
                ]
            },
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': 'projects/'+'debian-cloud/global/'+'images/family/debian-9'
                }
            }],
            'networkInterfaces': [{
                'network': '$(ref.cloud-sql-proxy-vpc.selfLink)',
                'subnetwork': '$(ref.cloud-sql-proxy-subnetwork.selfLink)',
                'networkIP': '$(ref.cloud-sql-proxy-internal-ip.address)',
                'accessConfigs': [{
                    'name': 'External NAT',
                    'type': 'ONE_TO_ONE_NAT',
                    'natIP': '$(ref.cloud-sql-proxy-external-ip.address)'
                }]
            }],
            'metadata': {
                'items': [{
                    'key': 'startup-script',
                    'value': ''+getBootstrapAsArray(context.env['project']+':'+context.properties['region']+':$(ref.'+context.properties['org']+'-metastore-inst.name)')
                }]
            },
            'serviceAccounts': [
                {
                    'email': context.properties['serviceAccount'],
                    'scopes': ["https://www.googleapis.com/auth/sqlservice.admin"]
                }
            ]
        }
    }]
    return {'resources': resources}