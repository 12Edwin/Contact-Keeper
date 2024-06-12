import json
import pytest
from events_management.read_event import lambda_handler as read_event
from events_management.update_event import lambda_handler as update_event
from events_management.delete_event import lambda_handler as delete_event
from events_management.create_event_for_group import lambda_handler as create_event


@pytest.fixture()
def sample_event():
    """ Generates a sample event """
    return {
        "body": json.dumps({
            "id": 1,
            "name": "Test Event",
            "description": "This is a test event",
            "start_date": "2024-06-12 15:00:00",
            "end_date": "2024-06-12 16:00:00",
            "type": "session",
            "location": "Test Location",
            "id_group_member": 1
        })
    }


def test_read_event(sample_event):
    mock = {
        "pathParameters": {
            "id": 1
        }
    }
    context = {}
    response = read_event(mock, context)
    data = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert "message" in response["body"]
    assert data["message"] == "Success"
    assert data["data"]["id"] == mock["pathParameters"]["id"]


def test_create_event(sample_event):
    context = {}
    response = create_event(sample_event, context)
    data = json.loads(response["body"])

    assert "message" in response["body"]
    assert data["message"] == "Success"
    assert response["statusCode"] == 200


def test_update_event(sample_event):
    context = {}
    response = update_event(sample_event, context)
    data = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert "message" in response["body"]
    assert data["message"] == "Success"


def test_delete_event(sample_event):
    context = {}
    event = {
        "pathParameters": {
            "id": 1
        }
    }
    response = delete_event(event, context)
    data = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert "message" in response["body"]
    assert data["message"] == "Success"
