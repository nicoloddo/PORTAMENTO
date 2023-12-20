# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:48:58 2023

@author: nicol
"""

import boto3
from botocore.exceptions import BotoCoreError, ClientError
import json

from common.utils import load_env_var

S3_BUCKET_NAME = load_env_var('S3_BUCKET_NAME')
ENDPOINT_URL = load_env_var('ENDPOINT_URL', required=False)

def save_to_s3(data, file_name, endpoint_url=ENDPOINT_URL, bucket_name=S3_BUCKET_NAME):
    """
    Saves data to an S3 bucket. Works with a specified endpoint URL (e.g., LocalStack)
    or defaults to AWS S3 if no endpoint URL is provided.

    :param data: Data to be saved to S3.
    :param file_name: The file name under which the data will be stored in S3.
    :param bucket_name: The name of the S3 bucket.
    :param endpoint_url: Optional. URL of the S3 service endpoint.
    :return: None
    """
    try:
        # Create an S3 client
        if endpoint_url:
            # Use the specified endpoint URL
            s3 = boto3.client('s3', endpoint_url=endpoint_url)
        else:
            # Default to AWS S3
            s3 = boto3.client('s3')

        # Save the data to the specified bucket and file name
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=data)
        print(f"File {file_name} saved successfully to {bucket_name}.")

    except (BotoCoreError, ClientError) as e:
        print(f"An error occurred: {e}")


def read_file_from_s3(key, endpoint_url=ENDPOINT_URL, bucket_name=S3_BUCKET_NAME):
    """
    Reads a file from an S3 bucket and returns its content. It works with a specified
    endpoint URL (e.g., LocalStack) or defaults to AWS S3 if no endpoint URL is provided.
    
    :param bucket: Name of the S3 bucket.
    :param key: Key of the file in the S3 bucket.
    :param endpoint_url: Optional. URL of the S3 service endpoint.
    :return: Content of the file.
    """
    # Create an S3 client
    if endpoint_url:
        # Use the specified endpoint URL
        s3 = boto3.client('s3', endpoint_url=endpoint_url)
    else:
        # Default to AWS S3
        s3 = boto3.client('s3')

    try:
        # Retrieve the file from the specified bucket and key
        response = s3.get_object(Bucket=bucket_name, Key=key)
        
        # Read and return the content of the file
        return response['Body'].read().decode('utf-8')
    except (BotoCoreError, ClientError) as e:
        print(f"An error occurred: {e}")
        return None

def list_folder_files_s3(prefix, endpoint_url=ENDPOINT_URL, bucket_name=S3_BUCKET_NAME):
    """
    Lists all files in a specified folder in an S3 bucket.

    :param prefix: Prefix of the folder to list files from in the S3 bucket.
    :param bucket_name: Name of the S3 bucket.
    :return: A response object containing the listed files under the specified prefix.
    """
    # Create an S3 client
    if endpoint_url:
        # Use the specified endpoint URL
        s3 = boto3.client('s3', endpoint_url=endpoint_url)
    else:
        # Default to AWS S3
        s3 = boto3.client('s3')
        
    try:
        # List objects under the specified prefix in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        return response
    except (BotoCoreError, ClientError) as e:
        print(f"An error occurred while listing files: {e}")
        return {'Contents': []}  # Return an empty list in case of an error
    
def delete_folder_s3(prefix, endpoint_url=ENDPOINT_URL, bucket_name=S3_BUCKET_NAME):
    """
    Deletes a folder (and its contents) in an S3 bucket. This function removes all 
    objects under the specified prefix.

    :param bucket: Name of the S3 bucket.
    :param prefix: Prefix of the folder to delete in the S3 bucket.
    """
    # Create an S3 client
    if endpoint_url:
        # Use the specified endpoint URL
        s3 = boto3.resource('s3', endpoint_url=endpoint_url)
    else:
        # Default to AWS S3
        s3 = boto3.resource('s3')
        
    bucket = s3.Bucket(bucket_name)
    try:
        # Delete all objects under the specified prefix
        bucket.objects.filter(Prefix=prefix).delete()
    except (BotoCoreError, ClientError) as e:
        print(f"An error occurred while deleting folder: {e}")

def get_database_from_s3(database_key="database.csv", bucket_name=S3_BUCKET_NAME):
    """
    Retrieves the CSV file in the given S3 bucket that contains the main database.

    :param bucket_name: Name of the S3 bucket.
    :param database_key: Key of the CSV file in the S3 bucket.
    :return: The Database CSV file or None if an error occurs.
    """
    s3_client = boto3.client('s3')
    try:
        # Retrieve the CSV file from the S3 bucket
        return s3_client.get_object(Bucket=bucket_name, Key=database_key)

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            print(f"File not found: {database_key} does not exist in the bucket {bucket_name}.")
        else:
            print(f"An error occurred while reading the CSV file: {e}")
        return None
    except BotoCoreError as e:
        print(f"An AWS error occurred: {e}")
        return None

def check_s3():
    pass