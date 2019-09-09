# Custom Role that allows the bearer to connect to CloudSQL
#
# Required as per CloudSQL Proxy Auth Requirements here https://cloud.google.com/sql/docs/mysql/sql-proxy#gce
#


"""Custom Role that allows the bearer to connect to CloudSQL."""

def GenerateConfig(context):
    """Custom Role that allows the bearer to connect to CloudSQL."""

    resources = [{
        'name': 'cloud_sql_connect_role',
        'type': 'gcp-types/iam-v1:projects.roles',
        'properties': {
            'parent': 'projects/'+context.env['project'],
            'roleId': 'cloud_sql_connect_role',
            'role': {
                'title': 'cloud_sql_connect_role',
                'description': 'cloud_sql_connect_role',
                'includedPermissions': ['cloudsql.instances.connect']
            }

        }
    }]
    return {'resources': resources}