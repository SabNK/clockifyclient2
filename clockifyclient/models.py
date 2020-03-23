""" Models the objects with which the clockify API works. One level above json dicts.
Models as simply as possible, omitting any fields not used by this package
"""
from abc import abstractmethod
import datetime

import dateutil
import dateutil.parser as date_parser

from clockifyclient.exceptions import ClockifyClientException


class ClockifyDatetime:
    """For converting between python datetime and clockify datetime string

    ClockifyDatetime is always timezone aware. If initialized with a naive datetime, local time is assumed
    """

    clockify_datetime_format = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, datetime_in):
        """Create

        Parameters
        ----------
        datetime_in: datetime
            Set this date time. If no timezone is set, will assume local timezone
        """
        if not datetime_in.tzinfo:
            datetime_in = datetime_in.replace(tzinfo=dateutil.tz.tzlocal())
        self.datetime = datetime_in

    @property
    def datetime_utc(self):
        """This datetime in the UTC time zone"""
        return self.datetime.astimezone(dateutil.tz.UTC)

    @property
    def datetime_local(self):
        """This datetime as local time"""
        return self.datetime.astimezone(dateutil.tz.tzlocal())

    @property
    def clockify_datetime(self):
        """This datetime a clockify-format string"""
        return self.datetime_utc.strftime(self.clockify_datetime_format)

    @classmethod
    def init_from_string(cls, clockify_date_string):
        return cls(date_parser.parse(clockify_date_string))

    def __str__(self):
        return self.clockify_datetime

class APIObject:
    """An object that is used in the clockify API and can be intiated from API response"""

    def __str__(self):
        return f"{self.__class__.__name__} "

    @classmethod
    def get_item(cls, dict_in, key, raise_error=True):
        """ Get item from dict, raise exception or return None if not found

        Parameters
        ----------
        dict_in: Dict
            dict to search in
        key: str
            dict key
        raise_error: Bool, optional
            If True raises error when key not found. Otherwise returns None. Defaults to True

        Raises
        ------
        ObjectParseException
            When key is not found in dict and raise_error is False

        Returns
        -------
        object
            Dict item at key
        None
            If item not found and raise_error is True

        """
        try:
            return dict_in[key]
        except KeyError:
            msg = f"Could not find key '{key}' in '{dict_in}'"
            raise ObjectParseException(msg)

    @classmethod
    def get_datetime(cls, dict_in, key, raise_error=True):
        """ Try to find key in dict and parse to datetime

        Parameters
        ----------
        dict_in: Dict
            dict to search in
        key: str
            dict key
        raise_error: Bool, optional
            If True raises error when key not found. Otherwise returns None. Defaults to True

        Raises
        ------
        ObjectParseException
            When key is not found in dict (if raise_error is True) or could not be parsed to datetime.
            Exception is always raised when value cannot be parsed

        Returns
        -------
        datetime
            parsed date from dict[key]
        None
            If item not found and raise_error is True
        """
        date_str = cls.get_item(dict_in, key, raise_error=raise_error)
        if not date_str:
            return None
        try:
            return ClockifyDatetime.init_from_string(date_str).datetime
        except ValueError as e:
            msg = f"Error parsing {date_str} to datetime: '{e}'"
            raise ObjectParseException(msg)

    @classmethod
    @abstractmethod
    def init_from_dict(cls, dict_in):
        """ Create an instance of this class from the expected json dict returned from Clockify API
        Parameters
        ----------
        dict_in: Dict
            As returned from Clockify API

        Raises
        ------
        ObjectParseException
            If dict_in does not contain all required field for creating an object

        Returns
        -------
        instance of this class, initialized to the values in dict_in

        """
        return

class HourlyRate(APIObject):
    """Feature of users per project and per workspace and default for workspaces"""
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return super().__str__() + f"{self.amount} {self.currency}"

    @classmethod
    def init_from_dict(cls, dict_in):
        return cls(amount=cls.get_item(cls.get_item(dict_in=dict_in, key='hourlyRate'), key='amount'),
                   currency=cls.get_item(cls.get_item(dict_in=dict_in, key='hourlyRate'), key='currency'))

class APIObjectID(APIObject):
    """An object that can be returned by the clockify API, has its ID"""
    def __init__(self, obj_id):
        """
        Parameters
        ----------
        obj_id: str
            object id hash
        """
        self.obj_id = obj_id

    def __eq__(self, other):
        return self.obj_id == other.obj_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.obj_id.__hash__()

    def __str__(self):
        return super().__str__() + f"({self.obj_id}) "

    @classmethod
    def init_from_dict(cls, dict_in):
        return cls(obj_id=cls.get_item(dict_in=dict_in, key='id'))

class UserGroup(APIObjectID):
    """Group of Users - is used to assign multi[le users to project"""

    def __init__(self, obj_id):
        super().__init__(obj_id=obj_id)
        self.users = []

    @classmethod
    def init_from_dict(cls, dict_in):

        for membership in cls.get_item(dict_in=dict_in, key='memberships'):
            if membership['membershipType'] == "USERGROUP":
                target_id = membership['targetId']
                return cls(obj_id=target_id)


class NamedAPIObject(APIObjectID):
    """An object of clockify API, with name and ID"""
    def __init__(self, obj_id, name):
        """

        Parameters
        ----------
        obj_id: str
            object id hash
        name: str
            human readable string
        """
        super().__init__(obj_id=obj_id)
        self.name = name

    def __str__(self):
        return super().__str__() + f"'{self.name}' "

    @classmethod
    def init_from_dict(cls, dict_in):
        return cls(obj_id=cls.get_item(dict_in=dict_in, key='id'),
            name=cls.get_item(dict_in=dict_in, key='name'))

class Workspace(NamedAPIObject):

    def __init__(self, obj_id, name, hourly_rate):
        super().__init__(obj_id=obj_id, name=name)
        self.hourly_rate = hourly_rate

    @classmethod
    def init_from_dict(cls, dict_in):
        return cls(obj_id=cls.get_item(dict_in=dict_in, key='id'),
                   name=cls.get_item(dict_in=dict_in, key='name'),
                   hourly_rate=HourlyRate.init_from_dict(dict_in=dict_in))

class User(NamedAPIObject):
    def __init__(self, obj_id, name, email, hourly_rates: {APIObjectID: HourlyRate}):
        super().__init__(obj_id=obj_id, name=name)
        self.email = email
        self.hourly_rates = hourly_rates

    def __str__(self):
        return super().__str__() + f"email:{self.email}"

    @classmethod
    def init_from_dict(cls, dict_in):
        obj_id = cls.get_item(dict_in=dict_in, key='id')
        name = cls.get_item(dict_in=dict_in, key='name')
        email = cls.get_item(dict_in=dict_in, key='email')
        hourly_rates = {}
        for membership in dict_in['memberships']:
            if membership['hourlyRate']:
                hourly_rates[APIObjectID(cls.get_item(dict_in=membership, key='targetId'))] = \
                    HourlyRate.init_from_dict(membership)
        return cls(obj_id=obj_id, name=name, email=email, hourly_rates=hourly_rates)

    def get_hourly_rate(self, workspace, project):
        if project in self.hourly_rates.keys() and self.hourly_rates[project]:
            return self.hourly_rates[project]
        elif project in project.hourly_rates.keys() and project.hourly_rates[project]:
            return project.hourly_rates[project]
        elif workspace in self.hourly_rates.keys() and self.hourly_rates[workspace]:
            return self.hourly_rates[workspace]
        else:
            return workspace.hourly_rate

class Project(NamedAPIObject):
    def __init__(self, obj_id, name, client, hourly_rates: {APIObjectID: HourlyRate}):
        super().__init__(obj_id=obj_id, name=name)
        self.client = client
        self.hourly_rates = hourly_rates

    def __str__(self):
        return super().__str__() + f"for client {self.client}"

    @classmethod
    def init_from_dict(cls, dict_in):
        obj_id = cls.get_item(dict_in=dict_in, key='id')
        name = cls.get_item(dict_in=dict_in, key='name')
        client = APIObjectID(cls.get_item(dict_in=dict_in, key='clientId'))
        hourly_rates = {APIObjectID(obj_id): HourlyRate.init_from_dict(dict_in)}
        for membership in dict_in['memberships']:
            if membership['hourlyRate']:
                hourly_rates[APIObjectID(cls.get_item(dict_in=membership, key ='userId'))] = HourlyRate.init_from_dict(membership)
        return cls(obj_id=obj_id, name=name, client=client, hourly_rates=hourly_rates)

    def get_hourly_rate(self, workspace, user):
        if user in self.hourly_rates.keys() and self.hourly_rates[user]:
            return self.hourly_rates[user]
        elif self in self.hourly_rates.keys() and self.hourly_rates[self]:
            return self.hourly_rates[self]
        elif workspace in user.hourly_rates.keys() and user.hourly_rates[workspace]:
            return user.hourly_rates[workspace]
        else:
            return workspace.hourly_rate

class Client(NamedAPIObject):
    pass

class Task(NamedAPIObject):
    pass

class Tag(NamedAPIObject):
    pass

class TimeEntry(APIObjectID):

    def __init__(self, obj_id, start, user, description='', project=None, task=None, tags=None, end=None):
        """
        Parameters
        ----------
        obj_id: str
            object id hash
        start: DateTime
            Start of time entry
        description: str, optional
            Human readable description of this time entry. Defaults to empty string
        project: Project, optional
            Project associated with this entry. Defaults to None
        end: DateTime, optional
            End of time entry. Defaults to None, meaning timer mode is activated
        """
        super().__init__(obj_id=obj_id)
        self.start = start
        self.user = user
        self.description = description
        self.project = project
        self.task = task
        self.tags = tags
        self.end = end

    def __str__(self):
        return super().__str__() + f"- '{self.truncate(self.description)}'"

    @staticmethod
    def truncate(msg, length=30):
        if msg[(length):]:
            return msg[:(length-3)] + "..."
        else:
            return msg

    @classmethod
    def init_from_dict(cls, dict_in):
        # required parameters
        interval = cls.get_item(dict_in, 'timeInterval')
        obj_id = cls.get_item(dict_in=dict_in, key='id')
        start = cls.get_datetime(dict_in=interval, key='start')
        user_id = cls.get_item(dict_in=dict_in, key='userId', raise_error=False)
        user = APIObjectID(obj_id=user_id)

        # optional parameters
        description = cls.get_item(dict_in=dict_in, key='description', raise_error=False)
        project_id = cls.get_item(dict_in=dict_in, key='projectId', raise_error=False)
        project = APIObjectID(obj_id=project_id) if project_id else None
        task_id = cls.get_item(dict_in=dict_in, key='taskId', raise_error=False)
        task = APIObjectID(obj_id=task_id) if task_id else None
        tag_ids = cls.get_item(dict_in=dict_in, key='tagIds', raise_error=False)
        tags = [APIObjectID(obj_id=t_i) for t_i in tag_ids] if tag_ids else None
        end = cls.get_datetime(dict_in=interval, key='end', raise_error=False)

        return cls(obj_id=obj_id,
                   start=start,
                   description=description,
                   user=user,
                   project=project,
                   task=task,
                   tags=tags,
                   end=end
                   )

    def to_dict(self):
        """As dict that can be sent to API"""
        as_dict = {"id": self.obj_id,
                   "start": str(ClockifyDatetime(self.start)),
                   "description": self.description,
                   "userId": self.user.obj_id
                   }
        if self.end:
            as_dict["end"] = str(ClockifyDatetime(self.end))
        if self.project:
            as_dict["projectId"] = self.project.obj_id
        if self.task:
            as_dict["taskId"] = self.task.obj_id
        if self.tags:
            as_dict["tagIds"] = [t.obj_id for t in tags]
        return {x: y for x, y in as_dict.items() if y}  # remove items with None value


class ObjectParseException(ClockifyClientException):
    pass
