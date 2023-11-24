# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:48:58 2023

@author: nicol
"""

import boto3
import json

from common.utils import load_env_var

S3_BUCKET_NAME = load_env_var('S3_BUCKET_NAME')

def save_to_s3(data, file_name, bucket_name=S3_BUCKET_NAME):
    s3 = boto3.resource('s3')
    s3_object = s3.Object(bucket_name, file_name)
    s3_object.put(Body=json.dumps(data))

def check_s3():
    pass

def read_file_from_s3():
    pass