# Creates a Service Account that
# 1. will be attached to the GCE/GKE hosting the Cloud SQL Proxy
# 2. will provide the Cloud SQL Proxy service with credentials to connect to the Cloud SQL instance hosting the Hive Metastore
#
# This is for the following reason:
# 1. The Cloud SQL Proxy service uses the credentials of the service account associated with its host(GCE/GKE) to connect to the Cloud SQL instance
# 2. Using the Service Account is a clean and safe way to restrict the credentials to this one process


"""Creates the Service Account to be used by the Cloud SQL Proxy to create a Gateway to the Cloud SQL with Hive Metastore."""

def GenerateConfig(context):
    """Creates the Service Account to be used by the Cloud SQL Proxy to create a Gateway to the Cloud SQL with Hive Metastore."""

    resources = [
        {
            'name': 'cloud-sql-proxy-service-acc',
            'type': 'iam.v1.serviceAccount',

            'properties': {
                'projectId': context.env['project'],
                'accountId': 'cloud-sql-proxy-service-acc',
                'displayName': 'cloud-sql-proxy-service-acc',
            },
        }
    ]
    return {'resources': resources}
