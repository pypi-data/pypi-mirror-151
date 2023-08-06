from datetime import datetime,timedelta
import time
import logging

logger = logging.getLogger(__name__)


__all__ = ['call_batch_transform', 'check_if_jobs_finished']

def call_batch_transform(bucket_name: str,
                         batch_transform_path: str,
                         sagemaker_client,
                         client: str,
                         campaign: str,
                         model_type: str,
                         iteration: str,
                         ec2_instance_type: str):
    """
    This functions parametrizes the request and calls a batch transform job using the following:
    Args:
        bucket_name: name of the bucket where the data is stored
        batch_transform_path: path of the S3 folder where the data will be saved
        sagemaker_client: boto3 sagemaker client with proper credentials
        client: SellDifferent client (bairesdev,cor,webee,etc).
        campaign: ID of the campaign
        model_type: Can be probability or bv model
        iteration: Version of the model used
        ec2_instance_type: Instance type used for the batch transform inference

    Returns:
        batch_job_name: string with the name of the batch transform job
    """
    today: datetime = datetime.today() - timedelta(hours=3)  # Argentina time
    started = False
    try:
        logger.info(f"Calling Batch Transform for client {client}, campaign {campaign},estimating {model_type}")
        # Only take the two first part of the model name to reduce the length
        model_name = f'SD-{model_type}-{client}-{iteration}'
        clean_model_name = "-".join(model_name.split("-")[:2])
        batch_job_name = f"DBTest-{model_type}-{client}-{campaign}-{today.strftime('%Y-%m-%d-%H-%M-%S')}"
        batch_input = f's3://{bucket_name}/{batch_transform_path}/input/{client}/{campaign}.csv'
        batch_output = f's3://{bucket_name}/{batch_transform_path}/output/{client}/{campaign}/{model_type}'

        request = {
            "TransformJobName": batch_job_name,
            "ModelName": model_name,
            "BatchStrategy": "MultiRecord",
            "DataProcessing": {
                "InputFilter": "$[2:]",  # The model ignore the first 2 columns IDLead and IDCampaign
                "JoinSource": "Input",
                "OutputFilter": '$[0,1,-1]'  # Return IDLead, IDCampaign and Rating
            },
            "TransformInput": {
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": batch_input
                    }
                },
                "ContentType": "text/csv",
                "SplitType": "Line",
                "CompressionType": "None"
            },
            "TransformOutput": {
                "S3OutputPath": batch_output,
                'Accept': 'text/csv',
                'AssembleWith': 'Line',
            },
            "TransformResources": {
                "InstanceType": ec2_instance_type,
                "InstanceCount": 1
            }
        }
        response = sagemaker_client.create_transform_job(**request)
        if response and response['TransformJobArn']:
            started = True
    except Exception as exception:
        error_message = f'Init batch transform - {repr(exception)}'
        logger.error(error_message)

    return batch_job_name,batch_output





def check_if_jobs_finished(sagemaker_client,
                           job_names_list: list,
                           retries: int = 100,
                           call_frequency: int = 20):
    """

    This functions checks if all the jobs attached to a model ( for example: Probability and business value) are
    complete.
    Args:
        sagemaker_client: boto3 sagemaker client with correct credentials
        job_names_list:  list of the names of the batch transform jobs
        retries:  Number of retries to check if the models are complete
        call_frequency: The function will wait this amount of seconds to retry.

    Returns:
        all_jobs_finished : True if all jobs are complete
        status_list: List of the status of each job at the moment of the end of the function.

    """
    all_jobs_finished = False
    while (all_jobs_finished == False) & (retries > 0):
        status_list = [
            sagemaker_client.describe_transform_job(**{"TransformJobName": job_name})['TransformJobStatus'] for job_name
            in job_names_list]
        if all(status == 'Completed' for status in status_list):
            print('yay, everything finished')
            all_jobs_finished = True
            return all_jobs_finished, status_list
        else:
            print(f'not yet,waiting {call_frequency} seconds')
            retries -= 1
            time.sleep(20)
    return all_jobs_finished, status_list

