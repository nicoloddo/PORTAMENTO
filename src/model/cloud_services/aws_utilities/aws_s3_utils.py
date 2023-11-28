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


def read_file_from_s3(bucket, key, endpoint_url=ENDPOINT_URL):
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
        response = s3.get_object(Bucket=bucket, Key=key)
        
        # Read and return the content of the file
        return response['Body'].read().decode('utf-8')
    except (BotoCoreError, ClientError) as e:
        print(f"An error occurred: {e}")
        return None

def check_s3():
    pass