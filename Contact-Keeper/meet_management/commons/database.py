import json
import pymysql
import boto3
from botocore.exceptions import ClientError

DB_HOST = 'utez-mydatabase-3n21ipzlxzgf.cvk46oagw552.us-east-1.rds.amazonaws.com'
DB_NAME = 'contact_keeper'


def get_db_connection():
    secrets = get_secret()
    host = DB_HOST
    user = secrets['username']
    password = secrets['password']
    db_name = DB_NAME

    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db_name
    )


def get_secret():

    secret_name = "MyDatabaseSecret"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    return json.loads(get_secret_value_response['SecretString'])