"""

    | **Properties**

        | {
        |     'aws_access_key_id' = 'string', 
        |     'aws_secret_access_key' = 'string', 
        |     'aws_session_token' = 'string', 
        |     'region_name' = 'string', 
        |     'botocore_session' = `botocore.session.Session <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html>`_, 
        |     'profile_name' = 'string'
        | }

"""

import boto3

def create(properties):
    """Create a Session to access the AWS Environment."""
    response = boto3.session.Session(
        aws_access_key_id = properties.get('aws_access_key_id', None), 
        aws_secret_access_key = properties.get('aws_secret_access_key', None),
        aws_session_token = properties.get('aws_session_token', None),
        region_name = properties.get('region_name', None),
        botocore_session = properties.get('botocore_session', None),
        profile_name = properties.get('profile_name', None),
    ) 
    return response
