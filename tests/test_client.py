#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from dateutil.tz import tzutc, tzlocal
from unittest.mock import Mock

import pytest

from clockifyclient.api import APIServer, APIServerException, APIErrorResponse
from clockifyclient.client import ClockifyAPI, APISession
from clockifyclient.models import APIObject, APIObjectID, HourlyRate, NamedAPIObject,\
    TimeEntry, User, Project, Task, Workspace, Tag, Client, ClockifyDatetime
from tests.factories import ClockifyMockResponses


@pytest.fixture()
def a_server():
    return APIServer("localhost")


@pytest.fixture()
def a_project(an_api_object_id, an_hourly_rate):
    return Project(obj_id='1234',
                   name='testproject',
                   client=an_api_object_id,
                   hourly_rates={an_api_object_id: an_hourly_rate}
                   )

@pytest.fixture()
def a_task():
    return Task(obj_id='123235', name='testtask')

@pytest.fixture()
def a_workspace(an_hourly_rate):
    return Workspace(obj_id='123235', name='testworkspace', hourly_rate=an_hourly_rate)

@pytest.fixture()
def a_tag():
    return Tag(obj_id='123235', name='testtag')

@pytest.fixture()
def a_user(an_api_object_id, an_hourly_rate):
    return User(obj_id='1232356',
                name='testuser',
                email='test_user@mail.ru',
                hourly_rates={an_api_object_id: an_hourly_rate}
                )

@pytest.fixture()
def an_hourly_rate_2():
    return HourlyRate( currency='RUR', amount=1000.90)

@pytest.fixture()
def an_api(a_server):
    return ClockifyAPI(api_server=a_server)

@pytest.fixture()
def a_time_entry(a_project):
    api_123 = APIObjectID(obj_id='123')
    h_rate_10USD = HourlyRate(amount=10, currency='USD')
    rates_123_10USD = {api_123: h_rate_10USD}
    a_user = User('123', 'name', 'email', rates_123_10USD)
    return TimeEntry(obj_id=None,
                     start=datetime.datetime(year=2019, month=10, day=12, hour=14, minute=10, second=1),
                     description='test description',
                     project=a_project,
                     user=a_user)

@pytest.fixture()
def a_mock_api(mock_requests, an_api, a_project, a_user, a_workspace, a_time_entry):
    """A ClockifyAPI that just returns default objects for all methods, not calling any server"""
    mock_api = Mock(spec=ClockifyAPI)
    mock_api.get_projects.return_value = [a_project]
    mock_api.get_user.return_value = a_user
    mock_api.get_users.return_value = [a_user]
    mock_api.get_workspaces.return_value = [a_workspace]
    mock_api.get_tags.return_value = [a_tag]
    mock_api.get_tasks.return_value = [a_task]
    mock_api.add_time_entry.return_value = a_time_entry
    mock_api.set_active_time_entry_end.return_value = a_time_entry
    return mock_api

def test_api_calls_get(mock_requests, an_api, a_date):
    """Some regular calls to api should yield correct python objects """
    mock_requests.set_response(ClockifyMockResponses.GET_WORKSPACES)
    workspaces = an_api.get_workspaces(api_key='mock_key')
    assert len(workspaces) == 2
    assert workspaces[0].obj_id == "5e5b8b0a95ae537fbde06e2f"
    assert workspaces[1].name == "Alice in Wonderland"
    assert workspaces[0].hourly_rate.amount == 99
    assert workspaces[1].hourly_rate.currency == "GBP"
    assert workspaces[0].forceProjects == False
    assert workspaces[1].forceProjects == True
    assert workspaces[0].forceTasks == False
    assert workspaces[1].forceTasks == True
    assert workspaces[0].forceTags == False
    assert workspaces[1].forceTags == True

    #TODO update factories with real hourlyRates
    mock_requests.set_response(ClockifyMockResponses.GET_USER)
    user = an_api.get_user(api_key='mock_key')
    assert user.obj_id == "5e5b8b0a95ae537fbde06e2e"
    assert user.name == "Lewis Carroll"
    assert user.email == "lewis_carroll_1832@mail.ru"
    assert APIObjectID(obj_id="5e5b8b0a95ae537fbde06e2f") in user.hourly_rates.keys()
    assert APIObjectID(obj_id="5e5b9f0195ae537fbde078bc") in user.hourly_rates.keys()
    assert user.hourly_rates[APIObjectID(obj_id="5e5b9f0195ae537fbde078bc")].currency == "RUR"

    mock_requests.set_response(ClockifyMockResponses.GET_USERS)
    users = an_api.get_users(api_key='mock_key', workspace=workspaces[1])
    assert len(users) == 4
    assert users[0].obj_id == "5e5b91837df81c0df5f29609"
    assert users[1].name == "Cheshire Cat"
    assert users[2].email == "lewis_carroll_1832@mail.ru"

    mock_requests.set_response(ClockifyMockResponses.GET_PROJECTS)
    projects = an_api.get_projects(api_key='mock_key', workspace=workspaces[1])
    assert len(projects) == 2
    assert projects[0].name == "Down the Rabbit Hole"
    assert projects[1].obj_id == "5e5b9f0195ae537fbde078bc"
    assert APIObjectID(obj_id="5e5b9c7995ae537fbde0778c") in projects[0].hourly_rates.keys()
    assert projects[0].hourly_rates[projects[0]].amount == 35
    assert users[0] in projects[0].hourly_rates.keys()
    assert projects[0].hourly_rates[users[0]].amount == 75

    mock_requests.set_response(ClockifyMockResponses.GET_TASKS)
    tasks = an_api.get_tasks(api_key='mock_key', workspace=workspaces[1], project=projects[0])
    assert len(tasks) == 2
    assert tasks[0].name == "drink me"
    assert tasks[1].obj_id == "5e5ba91100352a1175bc90fa"

    mock_requests.set_response(ClockifyMockResponses.GET_TAGS)
    tags = an_api.get_tags(api_key='mock_key', workspace=workspaces[1])
    assert len(tags) == 3
    assert tags[0].name == "test"
    assert tags[1].obj_id == "5e6381b72fe7db4da05dea37"
    assert tags[2].name == "test3"

    mock_requests.set_response(ClockifyMockResponses.GET_CLIENTS)
    clients = an_api.get_clients(api_key='mock_key', workspace=workspaces[1])
    assert len(clients) == 1
    assert clients[0].name == "Читатель"
    assert clients[0].obj_id == "5e654fc62fe7db4da05e7958"

    # TODO test for projects_with_tasks
    #projects_with_tasks = an_api

    # TODO add more asserts to get_time_entries
    mock_requests.set_response(ClockifyMockResponses.GET_TIME_ENTRIES)
    time_entries = an_api.get_time_entries(api_key='mock_key',
                                           workspace=workspaces[0],
                                           user=users[0],
                                           start_datetime=a_date,
                                           end_datetime=a_date)
    assert len(time_entries) == 3
    assert time_entries[0].description.endswith("ключ")
    assert time_entries[2].end == \
           datetime.datetime(2020, 3, 8, hour=18, minute=30, tzinfo=tzutc())

def test_api_add_time_entry(mock_requests, an_api, a_workspace, a_time_entry):
    mock_requests.set_response(ClockifyMockResponses.POST_TIME_ENTRY)

    # should not raise exceptions. Not much else to check with these mocks
    an_api.add_time_entry(api_key='mock_key', workspace=a_workspace, time_entry=a_time_entry)


def test_set_active_time_entry_end(mock_requests, an_api, a_workspace, a_user, a_date):
    mock_requests.set_response(ClockifyMockResponses.POST_TIME_ENTRY)
    response = an_api.set_active_time_entry_end(api_key='test', workspace=a_workspace, user=a_user, end_time=a_date)
    assert response is not None

    # if there is no currently running entry
    mock_requests.set_response(ClockifyMockResponses.CURRENTLY_RUNNING_ENTRY_NOT_FOUND)
    response = an_api.set_active_time_entry_end(api_key='test', workspace=a_workspace, user=a_user, end_time=a_date)
    assert response is None


def test_session(mock_requests, a_mock_api):
    """Run some session commands with a mocked underlying API"""
    session = APISession(api_server=an_api, api_key='test')
    session.api = a_mock_api
    session.add_time_entry(start_time=None, description='test', project=None)
    session.stop_timer()


def test_session_exception(mock_requests, a_mock_api):
    session = APISession(api_server=an_api, api_key='test')
    session.api = a_mock_api
    session.api.get_workspaces.side_effect = APIServerException('Something went wrong with the API',
                                                          error_response=APIErrorResponse(code=999,
                                                                                          message='mock error'))
    with pytest.raises(APIServerException):
        session.add_time_entry(start_time=None, description='test', project=None)
