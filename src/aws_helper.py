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
            'Key': source_key
        }
        try:
            self.s3.meta.client.copy(copy_source, self.NEW_BUCKET, destination_key)
        except botocore.exceptions.ClientError:
            raise AWSHelperException('Error copying key')

    def check_key(self, key):
        bucket = self.NEW_BUCKET
        data = {
            'Bucket': bucket,
            'Key': key
        }
        try:
            self.s3.meta.client.head_object(**data)
        except botocore.exceptions.ClientError:
            raise AWSHelperException(
                'Could not find object: {bucket}/{key}'.format(
                    bucket,
                    key
                )
            )

    def delete_key(self, key):
        bucket = self.OLD_BUCKET
        data = {
            'Bucket': bucket,
            'Key': key
        }
        try:
            self.s3.meta.client.delete_object(**data)
        except botocore.exceptions.ClientError:
            raise AWSHelperException(
                'Could not delete object: {bucket}/{key}'.format(
                    bucket,
                    key
                )
            )
