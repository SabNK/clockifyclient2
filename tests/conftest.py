"""Conftest.py is loaded for each pytest. Contains fixtures shared by multiple tests, amongs other things """
import datetime

from tests.factories import RequestsMock
from pytest import fixture
from clockifyclient.models import \
    APIObjectID, HourlyRate, NamedAPIObject,\
    TimeEntry, User, Project, Task, Workspace, Tag, Client, ClockifyDatetime

@fixture
def mock_requests(monkeypatch):
    """Make sure the api module does not do any actual http calls. Also makes it possible to set http responses

    Returns
    -------
    RequestsMock
    """
    requests_mock = RequestsMock()
    monkeypatch.setattr("clockifyclient.api.requests", requests_mock.requests)
    return requests_mock


@fixture()
def a_date():
    return datetime.datetime(year=2000, month=1, day=1)

@fixture()
def an_api_object_id():
    return APIObjectID(obj_id='123')

@fixture()
def an_hourly_rate():
    return HourlyRate(amount=100, currency='USD')
