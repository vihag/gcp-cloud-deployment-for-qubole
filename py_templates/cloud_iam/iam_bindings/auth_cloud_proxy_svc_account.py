# Authorizes a Service Account with
# 1. Cloud SQL Client Role
#
# This is for the following reason:
# 1. The Cloud SQL Proxy process uses the service account credentials to connect to the Cloud SQL Instance
# 2. This role ensures that the Cloud SQL Proxy process can generate credentials for the connection


"""Authorizes the a service account to act as a cloudsql client."""

def GenerateConfig(context):
    """Authorizes the a service account to act as a cloudsql client."""

    resources = [
        {
            'name': 'auth_cloud_sql_client_to_cloud_sql_proxy_sa',
            'type': 'gcp-types/cloudresourcemanager-v1:virtual.projects.iamMemberBinding',
            'properties': {
                'resource': context.env['project'],
                'role': 'roles/cloudsql.client',
                'member': 'serviceAccount:$(ref.cloud-sql-proxy-service-acc.email)'
            },
        }
    ]
    return {'resources': resources}