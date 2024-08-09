import json
from datetime import datetime


def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def response_200(data, message="Success"):
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "body": json.dumps({
            'status': 'success',
            'message': message,
            "data": data
        }, default=datetime_handler),
    }


def response_400(message="Bad Request"):
    return {
        'statusCode': 400,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps({
            'status': 'error',
            'message': message,
            "data": None
        }, default=datetime_handler),
    }


def response_401(message="Unauthorized"):
    return {
        'statusCode': 401,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps({
            'status': 'error',
            'message': message,
            "data": None
        }, default=datetime_handler),
    }


def response_403(message="Forbidden"):
    return {
        'statusCode': 403,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps({
            'status': 'error',
            'message': message,
            "data": None
        }, default=datetime_handler),
    }


def response_500(message="Internal Server Error"):
    return {
        'statusCode': 500,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps({
            'status': 'error',
            'message': message,
            "data": None
        }, default=datetime_handler),
    }