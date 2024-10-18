# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 13:48:56 2024

@author: nicol
"""

import boto3
from botocore.exceptions import BotoCoreError, ClientError
import json

from common.utils import load_env_var, MAX_IDS_PER_REQUEST

FETCH_STATE_MACHINE_ARN = load_env_var('FETCH_STATE_MACHINE_ARN')
ENDPOINT_URL = load_env_var('ENDPOINT_URL', required=False)

def start_fetch_state_machine(request_id, playlist_uris, req_n_playlists, batch_size = MAX_IDS_PER_REQUEST, endpoint_url=ENDPOINT_URL, fetch_state_machine_arn=FETCH_STATE_MACHINE_ARN):

    try:
        # Create an SQS client
        if endpoint_url:
            # Use the specified endpoint URL (e.g. LocalStack)
            stepfunctions_client = boto3.client('stepfunctions', endpoint_url=endpoint_url)
        else:
            # Default to AWS SQS
            stepfunctions_client = boto3.client('stepfunctions')

        # Prepare input for Step Functions
        step_functions_input = {
            "request_id": request_id,
            "playlist_uris": playlist_uris,
            'req_n_playlists': req_n_playlists,
            'batch_size': batch_size
        }
        
        # Start Step Function Execution
        response = stepfunctions_client.start_execution(
            stateMachineArn=fetch_state_machine_arn,
            input=json.dumps(step_functions_input)
        )
        return {'statusCode': 200, 'body': 'Fetching started.', 'response': response}

    except (BotoCoreError, ClientError) as e:
        print(f"An error occurred while starting the fetch: {e}")
        return {'statusCode': 500, 'body': f"Failed to start the fetch: {e}"}