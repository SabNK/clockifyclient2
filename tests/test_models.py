#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import dateutil
import pytest

from clockifyclient.models import \
    APIObject, APIObjectID, HourlyRate, NamedAPIObject,\
    TimeEntry, User, Project, Task, Workspace, Tag, Client, ClockifyDatetime
from tests.factories import ClockifyMockResponses

@pytest.fixture()
def a_user(an_api_object_id, an_hourly_rate):
    hourly_rates = {an_api_object_id: an_hourly_rate}
    return User('123', 'Lenin', 'lenin@mail.ru', hourly_rates)

@pytest.fixture()
def a_project(an_api_object_id, an_hourly_rate):
    hourly_rates = {alter_api_object_id: an_hourly_rate}
    return Project('123', 'Revolution', an_api_object_id, hourly_rates)

@pytest.fixture()
def alter_hourly_rate():
    return HourlyRate(amount=99, currency='GBP')

@pytest.fixture()
def alter_api_object_id():
    return APIObjectID(obj_id='456')

@pytest.fixture()
def a_workspace(an_api_object_id):
    return Workspace('123', "Russia'1917", alter_hourly_rate)

@pytest.fixture()
def mock_models_timezone(monkeypatch):
    """Set timezone to +8/+8"""
    monkeypatch.setattr('clockifyclient.models.dateutil.tz.tzlocal', lambda: dateutil.tz.gettz('Asia/Irkutsk'))

#TODO review
def test_time_entry_from_dict(mock_models_timezone):
    time_entry_dict = json.loads(ClockifyMockResponses.POST_TIME_ENTRY.text)
    time_entry = TimeEntry.init_from_dict(time_entry_dict)
    assert time_entry.description == 'testing description'

    time_entry_dict_again = TimeEntry.to_dict(time_entry)
    assert time_entry_dict_again['start'] == '2019-10-23T17:18:58Z'
    assert time_entry_dict_again['userId'] == '123456'
    assert time_entry_dict_again['description'] == 'testing description'
    assert time_entry_dict_again['projectId'] == '123456'

def test_time_entry(a_date):
    """Test with different input parameters"""
    # minimal parameters
    entry = TimeEntry(obj_id=None,
                      start=a_date,
                      user=APIObjectID(obj_id='123'),
                      description='test description')
    entry.to_dict()

#TODO review
def test_date_conversion(mock_models_timezone):
    example_string = "2018-06-12T14:01:41+00:00"
    datetime = ClockifyDatetime.init_from_string(example_string).datetime_utc
    assert datetime.year == 2018
    assert datetime.month == 6
    assert datetime.day == 12
    assert datetime.hour == 14
    assert datetime.minute == 1

    # str representation should always be UTC in Clockify format, ending in Z (for UTC)
    assert str(ClockifyDatetime(datetime)) == "2018-06-12T14:01:41Z"
    # Naive datetime should have been branded with local (mock +8)
    assert str(ClockifyDatetime.init_from_string("2018-06-12T14:01:41")) == "2018-06-12T06:01:41Z"

    # naive datetime, should be branded as local timezone, so the mock +8 timezone should have been subtracted for utc
    assert ClockifyDatetime.init_from_string("2018-06-12T14:01:41").datetime_utc.hour == 6
    # but the normal datetime should be unaffected: should be as input
    assert ClockifyDatetime.init_from_string("2018-06-12T14:01:41").datetime.hour == 14

    cltime = ClockifyDatetime(datetime)
    ClockifyDatetime.init_from_string(str(cltime))


def test_str(a_date, an_hourly_rate, an_api_object_id):
    """Getting coverage up 11 classes"""
    str(APIObject())
    str(an_hourly_rate)
    str(an_api_object_id)
    str(NamedAPIObject(obj_id='123', name='test'))
    str(Workspace(obj_id='123', name='test', hourly_rate=an_hourly_rate))
    str(User(obj_id='123', name='test', email='test@test.com',
             hourly_rates={an_api_object_id: an_hourly_rate}))
    str(Project(obj_id='123', name='test', client=an_api_object_id,
                hourly_rates={an_api_object_id: an_hourly_rate}))
    str(Tag(obj_id='123', name='test'))
    str(Task(obj_id='123', name='test'))
    str(Client(obj_id='123', name='test'))
    str(TimeEntry(obj_id='123', start=a_date, user=an_api_object_id))

#TODO try to use pytest fixtures
def test_get_hourly_rate(an_api_object_id, an_hourly_rate):
    an_api_object_id = APIObjectID(obj_id='123')
    alter_api_object_id = APIObjectID(obj_id='456')
    hourly_rate_1 = HourlyRate(amount=100, currency='USD')
    hourly_rate_2 = HourlyRate(amount=99, currency='GBP')
    hourly_rate_3 = HourlyRate(amount=98, currency='RUR')
    hourly_rates_1 = {an_api_object_id: hourly_rate_1}
    hourly_rates_2 = {alter_api_object_id: hourly_rate_2}

    user_1 = User('123', 'Lenin', 'lenin@mail.ru', hourly_rates_1)
    user_2 = User('357', 'Stalin', 'stalin@mail.ru', hourly_rates_1)
    project = Project('456', 'Revolution', an_api_object_id, hourly_rates_1)
    a_workspace = Workspace('789', "Russia'1917", hourly_rate_3)
    user_hourly_rate = user_1.get_hourly_rate(a_workspace, project)
    project_hourly_rate = project.get_hourly_rate(a_workspace, user_1)
    assert user_hourly_rate.amount == 98
    assert project_hourly_rate.currency == 'USD'
    project = Project('456', 'Revolution', an_api_object_id, hourly_rates_2)
    project_hourly_rate = project.get_hourly_rate(a_workspace, user_2)
    assert project_hourly_rate.currency == 'GBP'

def test_truncate(a_date):
    entry = TimeEntry(obj_id='123', start=a_date, user=APIObjectID(obj_id='123'))
    assert str(entry). endswith("''")
    entry.description = 'A short description'
    assert str(entry).endswith("description'")
    entry.description = 'A longer description thats 30c'
    assert str(entry).endswith("thats 30c'")
    entry.description = 'A longer description thats a lot longer then 30 characters'
    assert str(entry).endswith("thats ...'")
