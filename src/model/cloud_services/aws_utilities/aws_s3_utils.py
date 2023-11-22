# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:48:58 2023

@author: nicol
"""

import boto3
import json

def save_to_s3(data, bucket_name, file_name):
    s3 = boto3.resource('s3')
    s3_object = s3.Object(bucket_name, file_name)
    s3_object.put(Body=json.dumps(data))

def check_s3():
    pass