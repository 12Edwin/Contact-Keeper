import boto3
import os


def get_cognito_ids():
    cloudformation = boto3.client('cloudformation')
    stack_name = os.environ['AWS_STACK_NAME']

    user_pool_id = None
    user_pool_client_id = None

    try:
        response = cloudformation.describe_stacks(StackName=stack_name)
        outputs = response['Stacks'][0]['Outputs']

        for output in outputs:
            if 'ExportName' in output:
                if output['ExportName'] == f"{stack_name}-UserPoolId":
                    user_pool_id = output['OutputValue']
                elif output['ExportName'] == f"{stack_name}-UserPoolClientId":
                    user_pool_client_id = output['OutputValue']

        return user_pool_id, user_pool_client_id
    except Exception as e:
        print(f"Error getting Cognito IDs: {str(e)}")
        return None, None
