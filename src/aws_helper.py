import boto3
import botocore.exceptions
from dotenv import load_dotenv

class AWSHelperException(Exception):
    pass

class AWSHelper():

    OLD_BUCKET = 'asset-migrator-legacy-s3'
    NEW_BUCKET = 'asset-migrator-production-s3'

    def __init__(self):
        try:
            self.s3 = boto3.resource('s3')
        except botocore.exceptions.NoCredentialsError:
            raise AWSHelperException('No credentials found')

    def copy_key(self, source_key, destination_key):
        copy_source = {
            'Bucket': self.OLD_BUCKET,
            'Key': 'holi'
        }
        try:
            self.s3.meta.client.copy(copy_source, self.NEW_BUCKET, destination_key)
        except botocore.exceptions.ClientError:
            raise AWSHelperException('Error copying key')
