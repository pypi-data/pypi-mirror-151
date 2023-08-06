import boto3
from botocore.exceptions import ClientError
import os
import base64
import json

def __check_kwargs_then_environ__(kwarg_key, environ_key, **kwargs):
    if kwarg_key in kwargs:
        return kwargs[kwarg_key]
    else:
        try:
            return os.environ[environ_key]
        except:
            raise Exception(f'{kwarg_key} was not found in kwargs and {environ_key} was not found in environment variables')

def __get_secrets(default_region_name, **kwargs):
    secrets_name_env_name = kwargs.get('secrets_name_env_name', 'SECRETS_NAME')
    secrets_name = __check_kwargs_then_environ__('secrets_name', secrets_name_env_name, **kwargs)
    region_name_env_name = kwargs.get('region_name_env_name', 'SECRETS_REGION_NAME')
    region_name = os.environ.get(region_name_env_name, default_region_name)
    session = boto3.session.Session()
    try:
        client = session.client(
            service_name=kwargs.get('service_name', 'secretsmanager'),
            region_name=region_name
        )
    except:
        # This uses a try/finally to make sure the key's existence is always checked regardless of the id's existence.
        # It's intended to ensure an error with the id doesn't cover an error with the key.
        try:
            aws_access_key_id_env_name = kwargs.get('aws_access_key_id_env_name', 'AWS_ACCESS_KEY_ID')
            aws_access_key_id = __check_kwargs_then_environ__('aws_access_key_id', aws_access_key_id_env_name, **kwargs)
        finally:
            aws_secret_access_key_env_name = kwargs.get('aws_secret_access_key_env_name', 'AWS_SECRET_ACCESS_KEY')
            aws_secret_access_key = __check_kwargs_then_environ__('aws_secret_access_key', aws_secret_access_key_env_name, **kwargs)
        try:
            client = session.client(
                service_name=kwargs.get('service_name', 'secretsmanager'),
                region_name=region_name,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
        except:
            raise Exception("There was an error with the AWS access key and/or its ID.  Either the values passed to get_secrets were invalid, or the environment variables are configured incorrectly.")
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secrets_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise Exception("Secrets Manager can't decrypt the protected secret text using the provided KMS key.")
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise Exception("An error occurred on the server side.")
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise Exception("You provided an invalid value for a parameter.")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise Exception("You provided a parameter value that is not valid for the current state of the resource.")
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise Exception("We can't find the resource that you asked for.")
        else:
            raise Exception("There was an error getting the secret from the secret manager.")
    except:
        raise Exception("There was an unknown error getting the secret from the secret manager.  This is likely due to an error with secrets_name, aws_access_key_id, or aws_secret_access_key.")

    if 'SecretString' in get_secret_value_response:
        secrets = get_secret_value_response['SecretString']
    else:
        secrets = base64.b64decode(get_secret_value_response['SecretBinary'])
    return json.loads(secrets)

def set_env_variables(default_region_name, stop_on_failure=False, **kwargs):
    try:
        secrets = __get_secrets(default_region_name, **kwargs)
        for k,v in secrets.items():
            os.environ[k] = str(v).strip()
    except Exception as e:
        if stop_on_failure:
            raise Exception(e)
        else:
            print(e)
            pass