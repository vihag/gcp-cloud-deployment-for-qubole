# Creates a Google Compute Engine VM that will host a Cloud SQL Proxy process to connect to the Cloud SQL
# Features(Ideal)
# 1. A networkIP i.e. a static internal address
# 2. No network interfaces i.e. no external IP address
# 3. Instead of a single node GCE setup, setup a GKE to make the Cloud SQL Proxy Highly Available
# In the ideal scenario, we will use Private IP Service Networking between the VPC hosting this Cloud SQL Proxy instance
# Any external application desiring to connect to the Cloud SQL instance, will use the Cloud SQL proxy
# With the private IP setup, we can make sure that neither the Cloud SQL Instance, nor the Proxy has an external IP, hence making connections
#   very secure and removing latency
#
# Features(Practical)
# 1. A network interface with a static external address
# 2. This is an example setup using a shared core GCE VM. Replace with a GKE template
# GCP has not exposed Service Networking as a public GCP type (https://cloud.google.com/deployment-manager/docs/configuration/supported-gcp-types) hence
# we cannot create the Service Peering using the GCP Cloud Deployments Templates right not TODO
# 3. The cloud SQL proxy now connects to the Cloud SQL using the CLoud SQL's public IP
# 4. Since the CLoud SQLs public IP is being used, even the Proxy Host has to have an external IP. TODO remove when we can
#
# Caveats:
# 1. Since we are using public IP addresses
#    - We depend on Google's deny everything firewall defaults to protect connections to the Proxy and transitively the Cloud SQL instance
#    - Public IP usage introduces some visible latency

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