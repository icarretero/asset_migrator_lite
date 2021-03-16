import boto3
import botocore.exceptions

class AWSHelperException(Exception):
    pass


class AWSHelperConnectionError(AWSHelperException):
    pass


class AWSHelperNotFoundError(AWSHelperException):
    pass


def handle_exceptions(method):
    def wrapper(*v, **kw):
        try:
            return method(*v, **kw)
        except botocore.exceptions.NoCredentialsError:
            raise AWSHelperConnectionError('No credentials found')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Message']:
                message = e.response['Error']['Message']
            else:
                message = "Unhandled Error"
            if e.response['Error']['Code']:
                code = e.response['Error']['Code']
            else:
                code = '500'
            if code == '404':
                raise AWSHelperNotFoundError(message)
            elif code == '403':
                raise AWSHelperConnectionError(message)
            else:
                raise AWSHelperException(message)
    return wrapper


class AWSHelper():

    OLD_BUCKET = 'asset-migrator-legacy-s3'
    NEW_BUCKET = 'asset-migrator-production-s3'

    def __init__(self):
        try:
            self.s3 = boto3.resource('s3')
        except botocore.exceptions.NoCredentialsError:
            raise AWSHelperException('No credentials found')

    @handle_exceptions
    def copy_key(self, source_key, destination_key):
        copy_source = {
            'Bucket': self.OLD_BUCKET,
            'Key': source_key
        }
        self.s3.meta.client.copy(copy_source, self.NEW_BUCKET, destination_key)

    @handle_exceptions
    def check_key(self, key):
        bucket = self.NEW_BUCKET
        data = {
            'Bucket': bucket,
            'Key': key
        }
        self.s3.meta.client.head_object(**data)

    @handle_exceptions
    def delete_key(self, key):
        bucket = self.OLD_BUCKET
        data = {
            'Bucket': bucket,
            'Key': key
        }
        self.s3.meta.client.delete_object(**data)
