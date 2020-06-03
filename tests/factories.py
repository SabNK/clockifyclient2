""" Shared classes used in other tests. For generating test data """
from itertools import cycle
from typing import List
from unittest.mock import Mock
from requests.models import Response


class RequestMockResponse:
    """A description of a http server response
    """

    def __init__(self, text, response_code):
        """

        Parameters
        ----------
        text: str
            Text of this response
        response_code: int
            https response code, like 200 or 404
        """

        self.text = text
        self.response_code = response_code


class RequestsMock:
    """ Can be put in place of the requests module. Can be set to return requests.models.Response objects

    """

    def __init__(self):
        self.requests = Mock()  # for keeping track of past requests
        self.http_methods = [self.requests.get,
                             self.requests.post,
                             self.requests.patch,
                             self.requests.update]

    def set_response(self, response: RequestMockResponse):
        """Just for convenience"""
        self.set_responses([response])

    def set_responses(self, responses: List[RequestMockResponse]):
        """Any call to a http method will yield the given response. A list of responses will be looped over
        indefinitely

        Parameters
        ----------
        responses: List[RequestMockResponse]
            List of responses. Will be returned
        """

        objects = [
            self.create_response_object(response.response_code, response.text)
            for response in responses
        ]

        for method in self.http_methods:
            method.side_effect = cycle(objects)

    def set_response_exception(self, exception):
        """Any call to a http method will yield the given exception instance
        """
        for method in self.http_methods:
            method.side_effect = exception

    @staticmethod
    def create_response_object(status_code, text):
        response = Response()
        response.encoding = "utf-8"
        response.status_code = status_code
        response._content = bytes(text, response.encoding)
        response.url = "mock_url"
        return response

    def get(self, *args, **kwargs):
        return self.requests.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.requests.post(*args, **kwargs)

    def reset(self):
        self.requests.reset_mock()

    def called(self):
        """True if any http method was called"""
        return any([x.called for x in self.http_methods])


class ClockifyMockResponses:
    """Some cached examples of http responses from Clockify API v1. These partly come from https://clockify.me/developers-api
    and party were recorded by interacting with the server live around november 2019
    """

    # with non-existent API or missing key
    AUTH_ERROR = RequestMockResponse(
        '{"description":"Full authentication is required to access this resource","code":1000}',
        401,
    )

    # Trying to set something on
    CURRENTLY_RUNNING_ENTRY_NOT_FOUND = RequestMockResponse(
        """{"message":"Currently running time entry doesn't exist on workspace 123456 for user 123456.","code":404}""",
        404)

    # calling get /workspaces
    # TODO replace with final version of hourly rates from Alice
    GET_WORKSPACES = RequestMockResponse(
        """ [
    {
        "id": "5e5b8b0a95ae537fbde06e2f",
        "name": "Lewis Carroll's workspace",
        "hourlyRate": {
            "amount": 0,
            "currency": "USD"
        },
        "memberships": [
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e5b8b0a95ae537fbde06e2f",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            }
        ],
        "workspaceSettings": {
            "timeRoundingInReports": false,
            "onlyAdminsSeeBillableRates": true,
            "onlyAdminsCreateProject": true,
            "onlyAdminsSeeDashboard": false,
            "defaultBillableProjects": true,
            "lockTimeEntries": null,
            "round": {
                "round": "Round to nearest",
                "minutes": "15"
            },
            "projectFavorites": true,
            "canSeeTimeSheet": false,
            "canSeeTracker": true,
            "projectPickerSpecialFilter": false,
            "forceProjects": false,
            "forceTasks": false,
            "forceTags": false,
            "forceDescription": false,
            "onlyAdminsSeeAllTimeEntries": false,
            "onlyAdminsSeePublicProjectsEntries": false,
            "trackTimeDownToSecond": true,
            "projectGroupingLabel": "client",
            "adminOnlyPages": [],
            "automaticLock": null,
            "onlyAdminsCreateTag": false,
            "onlyAdminsCreateTask": true,
            "isProjectPublicByDefault": true
        },
        "imageUrl": "",
        "featureSubscriptionType": null
    },
    {
        "id": "5e5b8b3a95ae537fbde06e58",
        "name": "Alice in Wonderland",
        "hourlyRate": {
            "amount": 10000,
            "currency": "GBP"
        },
        "memberships": [
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e5b8b3a95ae537fbde06e58",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b91837df81c0df5f29609",
                "hourlyRate": null,
                "targetId": "5e5b8b3a95ae537fbde06e58",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b94837df81c0df5f2979c",
                "hourlyRate": null,
                "targetId": "5e5b8b3a95ae537fbde06e58",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b998195ae537fbde0761d",
                "hourlyRate": null,
                "targetId": "5e5b8b3a95ae537fbde06e58",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            }
        ],
        "workspaceSettings": {
            "timeRoundingInReports": false,
            "onlyAdminsSeeBillableRates": true,
            "onlyAdminsCreateProject": true,
            "onlyAdminsSeeDashboard": false,
            "defaultBillableProjects": true,
            "lockTimeEntries": null,
            "round": {
                "round": "Round to nearest",
                "minutes": "15"
            },
            "projectFavorites": true,
            "canSeeTimeSheet": false,
            "canSeeTracker": true,
            "projectPickerSpecialFilter": false,
            "forceProjects": false,
            "forceTasks": false,
            "forceTags": false,
            "forceDescription": false,
            "onlyAdminsSeeAllTimeEntries": false,
            "onlyAdminsSeePublicProjectsEntries": false,
            "trackTimeDownToSecond": false,
            "projectGroupingLabel": "client",
            "adminOnlyPages": [],
            "automaticLock": null,
            "onlyAdminsCreateTag": false,
            "onlyAdminsCreateTask": true,
            "isProjectPublicByDefault": true
        },
        "imageUrl": "https://img.clockify.me/2020-03-01T11%3A07%3A16.041ZIn+Wonderland.jpg",
        "featureSubscriptionType": null
    },
    {
        "id": "5e64e36443f3817e058c24d7",
        "name": "Алиса в Стране чудес",
        "hourlyRate": {
            "amount": 1000,
            "currency": "GBP"
        },
        "memberships": [
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e64e36443f3817e058c24d7",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e64e65643f3817e058c261a",
                "hourlyRate": null,
                "targetId": "5e64e36443f3817e058c24d7",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e64ea19ea0d47492eb3c0a2",
                "hourlyRate": null,
                "targetId": "5e64e36443f3817e058c24d7",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            }
        ],
        "workspaceSettings": {
            "timeRoundingInReports": false,
            "onlyAdminsSeeBillableRates": true,
            "onlyAdminsCreateProject": true,
            "onlyAdminsSeeDashboard": false,
            "defaultBillableProjects": true,
            "lockTimeEntries": null,
            "round": {
                "round": "Round to nearest",
                "minutes": "15"
            },
            "projectFavorites": true,
            "canSeeTimeSheet": false,
            "canSeeTracker": true,
            "projectPickerSpecialFilter": true,
            "forceProjects": false,
            "forceTasks": false,
            "forceTags": false,
            "forceDescription": false,
            "onlyAdminsSeeAllTimeEntries": false,
            "onlyAdminsSeePublicProjectsEntries": false,
            "trackTimeDownToSecond": true,
            "projectGroupingLabel": "client",
            "adminOnlyPages": [],
            "automaticLock": null,
            "onlyAdminsCreateTag": false,
            "onlyAdminsCreateTask": true,
            "isProjectPublicByDefault": true
        },
        "imageUrl": "https://img.clockify.me/2020-03-08T12%3A34%3A07.254Z3626302_original.jpg",
        "featureSubscriptionType": null
    },
    {
        "id": "5e773474b7cf6e317fdef1f1",
        "name": "test",
        "hourlyRate": {
            "amount": 0,
            "currency": "USD"
        },
        "memberships": [
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e773474b7cf6e317fdef1f1",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            }
        ],
        "workspaceSettings": {
            "timeRoundingInReports": false,
            "onlyAdminsSeeBillableRates": true,
            "onlyAdminsCreateProject": true,
            "onlyAdminsSeeDashboard": false,
            "defaultBillableProjects": true,
            "lockTimeEntries": null,
            "round": {
                "round": "Round to nearest",
                "minutes": "15"
            },
            "projectFavorites": true,
            "canSeeTimeSheet": false,
            "canSeeTracker": true,
            "projectPickerSpecialFilter": false,
            "forceProjects": false,
            "forceTasks": false,
            "forceTags": false,
            "forceDescription": false,
            "onlyAdminsSeeAllTimeEntries": false,
            "onlyAdminsSeePublicProjectsEntries": false,
            "trackTimeDownToSecond": true,
            "projectGroupingLabel": "client",
            "adminOnlyPages": [],
            "automaticLock": null,
            "onlyAdminsCreateTag": false,
            "onlyAdminsCreateTask": true,
            "isProjectPublicByDefault": true
        },
        "imageUrl": "",
        "featureSubscriptionType": null
    }
] """, 200)

    # calling get /user
    GET_USER = RequestMockResponse(
        """
               {
        "id": "5e5b8b0a95ae537fbde06e2e",
        "email": "lewis_carroll_1832@mail.ru",
        "name": "Lewis Carroll",
        "memberships": [
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e5b8b0a95ae537fbde06e2f",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e5b8b3a95ae537fbde06e58",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e5b9c7995ae537fbde0778c",
                "membershipType": "PROJECT",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e5b9f0195ae537fbde078bc",
                "membershipType": "PROJECT",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e64e36443f3817e058c24d7",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e64f6804aa5d3718482d06b",
                "membershipType": "PROJECT",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e64f6804aa5d3718482d06b",
                "membershipType": "PROJECT",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e773474b7cf6e317fdef1f1",
                "membershipType": "WORKSPACE",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e78faf4b7cf6e317fe14562",
                "membershipType": "PROJECT",
                "membershipStatus": "ACTIVE"
            }
        ],
                "profilePicture": "https://img.clockify.me/2020-03-01T10%3A33%3A32.180Zcarroll.png",
                "activeWorkspace": "5e64e36443f3817e058c24d7",
                "defaultWorkspace": "5e64e36443f3817e058c24d7",
                "settings": {
                    "weekStart": "MONDAY",
                    "timeZone": "Europe/Moscow",
                    "timeFormat": "HOUR24",
                    "dateFormat": "DD/MM/YYYY",
                    "sendNewsletter": false,
                    "weeklyUpdates": false,
                    "longRunning": false,
                    "timeTrackingManual": false,
                    "summaryReportSettings": {
                        "group": "PROJECT",
                        "subgroup": "TIME_ENTRY"
                    },
                    "isCompactViewOn": false,
                    "dashboardSelection": "ME",
                    "dashboardViewType": "PROJECT",
                    "dashboardPinToTop": false,
                    "projectListCollapse": 50,
                    "collapseAllProjectLists": false,
                    "groupSimilarEntriesDisabled": false,
                    "myStartOfDay": "09:00"
                },
                "status": "ACTIVE"
            }
        """, 200)

    # calling get /workspaces/<workspace id>/users
    # TODO replace with final version of hourly rates from Alice
    GET_USERS = RequestMockResponse(
        """ [
                {
                    "id": "5e5b8b0a95ae537fbde06e2e",
                    "email": "lewis_carroll_1832@mail.ru",
                    "name": "Lewis Carroll",
                    "memberships": [
                        {
                            "userId": "5e5b8b0a95ae537fbde06e2e",
                            "hourlyRate": null,
                            "targetId": "5e5b8b0a95ae537fbde06e2f",
                            "membershipType": "WORKSPACE",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e5b8b0a95ae537fbde06e2e",
                            "hourlyRate": null,
                            "targetId": "5e5b8b3a95ae537fbde06e58",
                            "membershipType": "WORKSPACE",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e5b8b0a95ae537fbde06e2e",
                            "hourlyRate": null,
                            "targetId": "5e5b9c7995ae537fbde0778c",
                            "membershipType": "PROJECT",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e5b8b0a95ae537fbde06e2e",
                            "hourlyRate": null,
                            "targetId": "5e5b9f0195ae537fbde078bc",
                            "membershipType": "PROJECT",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e5b8b0a95ae537fbde06e2e",
                            "hourlyRate": null,
                            "targetId": "5e64e36443f3817e058c24d7",
                            "membershipType": "WORKSPACE",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e5b8b0a95ae537fbde06e2e",
                            "hourlyRate": null,
                            "targetId": "5e64f6804aa5d3718482d06b",
                            "membershipType": "PROJECT",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e5b8b0a95ae537fbde06e2e",
                            "hourlyRate": null,
                            "targetId": "5e64f6804aa5d3718482d06b",
                            "membershipType": "PROJECT",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e5b8b0a95ae537fbde06e2e",
                            "hourlyRate": null,
                            "targetId": "5e773474b7cf6e317fdef1f1",
                            "membershipType": "WORKSPACE",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e5b8b0a95ae537fbde06e2e",
                            "hourlyRate": null,
                            "targetId": "5e78faf4b7cf6e317fe14562",
                            "membershipType": "PROJECT",
                            "membershipStatus": "ACTIVE"
                        }
                    ],
                    "profilePicture": "https://img.clockify.me/2020-03-01T10%3A33%3A32.180Zcarroll.png",
                    "activeWorkspace": "5e64e36443f3817e058c24d7",
                    "defaultWorkspace": "5e64e36443f3817e058c24d7",
                    "settings": {
                        "weekStart": "MONDAY",
                        "timeZone": "Europe/Moscow",
                        "timeFormat": "HOUR24",
                        "dateFormat": "DD/MM/YYYY",
                        "sendNewsletter": false,
                        "weeklyUpdates": false,
                        "longRunning": false,
                        "timeTrackingManual": false,
                        "summaryReportSettings": {
                            "group": "PROJECT",
                            "subgroup": "TIME_ENTRY"
                        },
                        "isCompactViewOn": false,
                        "dashboardSelection": "ME",
                        "dashboardViewType": "PROJECT",
                        "dashboardPinToTop": false,
                        "projectListCollapse": 50,
                        "collapseAllProjectLists": false,
                        "groupSimilarEntriesDisabled": false,
                        "myStartOfDay": "09:00"
                    },
                    "status": "ACTIVE"
                },
                {
                    "id": "5e64e65643f3817e058c261a",
                    "email": "alice.lidell.1852@mail.ru",
                    "name": "Алиса",
                    "memberships": [
                        {
                            "userId": "5e64e65643f3817e058c261a",
                            "hourlyRate": null,
                            "targetId": "5e64e36443f3817e058c24d7",
                            "membershipType": "WORKSPACE",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e64e65643f3817e058c261a",
                            "hourlyRate": null,
                            "targetId": "5e64f6804aa5d3718482d06b",
                            "membershipType": "PROJECT",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e64e65643f3817e058c261a",
                            "hourlyRate": null,
                            "targetId": "5e64f6804aa5d3718482d06b",
                            "membershipType": "PROJECT",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e64e65643f3817e058c261a",
                            "hourlyRate": null,
                            "targetId": "5e660842ea0d47492eb483fa",
                            "membershipType": "WORKSPACE",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e64e65643f3817e058c261a",
                            "hourlyRate": null,
                            "targetId": "5e6613b92fe7db4da05f37f6",
                            "membershipType": "USERGROUP",
                            "membershipStatus": "ACTIVE"
                        }
                    ],
                    "profilePicture": "https://img.clockify.me/2020-03-08T12%3A36%3A29.634Zalice3.jpg",
                    "activeWorkspace": "5e64e36443f3817e058c24d7",
                    "defaultWorkspace": "5e64e36443f3817e058c24d7",
                    "settings": {
                        "weekStart": "MONDAY",
                        "timeZone": "Europe/Moscow",
                        "timeFormat": "HOUR24",
                        "dateFormat": "DD.MM.YYYY",
                        "sendNewsletter": false,
                        "weeklyUpdates": false,
                        "longRunning": false,
                        "timeTrackingManual": true,
                        "summaryReportSettings": {
                            "group": "PROJECT",
                            "subgroup": "TIME_ENTRY"
                        },
                        "isCompactViewOn": false,
                        "dashboardSelection": "ME",
                        "dashboardViewType": "PROJECT",
                        "dashboardPinToTop": false,
                        "projectListCollapse": 50,
                        "collapseAllProjectLists": false,
                        "groupSimilarEntriesDisabled": false,
                        "myStartOfDay": "09:00"
                    },
                    "status": "ACTIVE"
                },
                {
                    "id": "5e64ea19ea0d47492eb3c0a2",
                    "email": "white.rabbit.1865@mail.ru",
                    "name": "Белый Кролик",
                    "memberships": [
                        {
                            "userId": "5e64ea19ea0d47492eb3c0a2",
                            "hourlyRate": null,
                            "targetId": "5e64e36443f3817e058c24d7",
                            "membershipType": "WORKSPACE",
                            "membershipStatus": "ACTIVE"
                        },
                        {
                            "userId": "5e64ea19ea0d47492eb3c0a2",
                            "hourlyRate": null,
                            "targetId": "5e64f6804aa5d3718482d06b",
                            "membershipType": "PROJECT",
                            "membershipStatus": "ACTIVE"
                        }
                    ],
                    "profilePicture": "https://img.clockify.me/2020-03-08T12%3A53%3A11.254Zwhite_rabbit_5.jpg",
                    "activeWorkspace": "5e64e36443f3817e058c24d7",
                    "defaultWorkspace": "5e64e36443f3817e058c24d7",
                    "settings": {
                        "weekStart": "MONDAY",
                        "timeZone": "Europe/Moscow",
                        "timeFormat": "HOUR12",
                        "dateFormat": "MM/DD/YYYY",
                        "sendNewsletter": false,
                        "weeklyUpdates": false,
                        "longRunning": false,
                        "timeTrackingManual": true,
                        "summaryReportSettings": {
                            "group": "Project",
                            "subgroup": "Time Entry"
                        },
                        "isCompactViewOn": false,
                        "dashboardSelection": "ME",
                        "dashboardViewType": "PROJECT",
                        "dashboardPinToTop": false,
                        "projectListCollapse": 50,
                        "collapseAllProjectLists": false,
                        "groupSimilarEntriesDisabled": false,
                        "myStartOfDay": "09:00"
                    },
                    "status": "ACTIVE"
                }
            ] """, 200)

    # calling /workspaces/<workspace id>/projects
    # TODO replace with final version of hourly rates from Alice
    GET_PROJECTS = RequestMockResponse(
        """ [
    {
        "id": "5e5b9c7995ae537fbde0778c",
        "name": "Down the Rabbit Hole",
        "hourlyRate": {
            "amount": 0,
            "currency": "GBP"
        },
        "clientId": "5e78f6d6ff66a323df51be99",
        "workspaceId": "5e5b8b3a95ae537fbde06e58",
        "billable": true,
        "memberships": [
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e5b9c7995ae537fbde0778c",
                "membershipType": "PROJECT",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b91837df81c0df5f29609",
                "hourlyRate": null,
                "targetId": "5e5b9c7995ae537fbde0778c",
                "membershipType": "PROJECT",
                "membershipStatus": "ACTIVE"
            },
            {
                "userId": "5e5b9d2e95ae537fbde077e4",
                "hourlyRate": null,
                "targetId": "5e5b9c7995ae537fbde0778c",
                "membershipType": "PROJECT",
                "membershipStatus": "ACTIVE"
            }
        ],
        "color": "#009688",
        "estimate": {
            "estimate": "PT0S",
            "type": "AUTO"
        },
        "archived": true,
        "duration": "PT2S",
        "clientName": "Reader",
        "note": "",
        "template": false,
        "public": false
    },
    {
        "id": "5e78faf4b7cf6e317fe14562",
        "name": "Down the Rabbit-Hole",
        "hourlyRate": {
            "amount": 0,
            "currency": "USD"
        },
        "clientId": "5e78f6d6ff66a323df51be99",
        "workspaceId": "5e5b8b3a95ae537fbde06e58",
        "billable": true,
        "memberships": [
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e78faf4b7cf6e317fe14562",
                "membershipType": "PROJECT",
                "membershipStatus": "ACTIVE"
            }
        ],
        "color": "#8BC34A",
        "estimate": {
            "estimate": "PT0S",
            "type": "AUTO"
        },
        "archived": false,
        "duration": "PT12H",
        "clientName": "Reader",
        "note": "",
        "template": false,
        "public": false
    },
    {
        "id": "5e5b9f0195ae537fbde078bc",
        "name": "The Pool of Tears",
        "hourlyRate": {
            "amount": 0,
            "currency": "USD"
        },
        "clientId": "",
        "workspaceId": "5e5b8b3a95ae537fbde06e58",
        "billable": true,
        "memberships": [
            {
                "userId": "5e5b8b0a95ae537fbde06e2e",
                "hourlyRate": null,
                "targetId": "5e5b9f0195ae537fbde078bc",
                "membershipType": "PROJECT",
                "membershipStatus": "ACTIVE"
            }
        ],
        "color": "#FF5722",
        "estimate": {
            "estimate": "PT0S",
            "type": "AUTO"
        },
        "archived": false,
        "duration": "PT0S",
        "clientName": "",
        "note": "",
        "template": false,
        "public": false
    }
] """, 200)

    # calling /workspaces/<workspace id>/projects/<project id>/tasks
    GET_TASKS = RequestMockResponse(
        """ [
                {
                    "id": "5e78fa7526b6633c95466520",
                    "name": "to be tired on the bank",
                    "projectId": "5e5b9c7995ae537fbde0778c",
                    "assigneeIds": [
                        "5e5b91837df81c0df5f29609"
                    ],
                    "assigneeId": "5e5b91837df81c0df5f29609",
                    "estimate": "PT0S",
                    "status": "ACTIVE",
                    "duration": "PT0S"
                },
                {
                    "id": "5e78fa5a26b6633c954664f7",
                    "name": "to falling down in weel",
                    "projectId": "5e5b9c7995ae537fbde0778c",
                    "assigneeIds": [
                        "5e5b91837df81c0df5f29609"
                    ],
                    "assigneeId": "5e5b91837df81c0df5f29609",
                    "estimate": "PT0S",
                    "status": "ACTIVE",
                    "duration": "PT0S"
                },
                {
                    "id": "5e78fa32514ca6177298eead",
                    "name": "be late",
                    "projectId": "5e5b9c7995ae537fbde0778c",
                    "assigneeIds": [
                        "5e5b94837df81c0df5f2979c"
                    ],
                    "assigneeId": "5e5b94837df81c0df5f2979c",
                    "estimate": "PT0S",
                    "status": "ACTIVE",
                    "duration": "PT0S"
                },
                {
                    "id": "5e78fa0c514ca6177298ee6d",
                    "name": "get out to the garden",
                    "projectId": "5e5b9c7995ae537fbde0778c",
                    "assigneeIds": [
                        "5e5b91837df81c0df5f29609"
                    ],
                    "assigneeId": "5e5b91837df81c0df5f29609",
                    "estimate": "PT0S",
                    "status": "ACTIVE",
                    "duration": "PT0S"
                },
                {
                    "id": "5e5ba93e7df81c0df5f2a1c2",
                    "name": "drink me",
                    "projectId": "5e5b9c7995ae537fbde0778c",
                    "assigneeIds": [
                        "5e5b91837df81c0df5f29609"
                    ],
                    "assigneeId": "5e5b91837df81c0df5f29609",
                    "estimate": "PT0S",
                    "status": "ACTIVE",
                    "duration": "PT0S"
                },
                {
                    "id": "5e5ba91100352a1175bc90fa",
                    "name": "eat me",
                    "projectId": "5e5b9c7995ae537fbde0778c",
                    "assigneeIds": [
                        "5e5b91837df81c0df5f29609"
                    ],
                    "assigneeId": "5e5b91837df81c0df5f29609",
                    "estimate": "PT0S",
                    "status": "ACTIVE",
                    "duration": "PT0S"
                }
            ]  """, 200)

    # calling /workspaces/<workspace id>/tags
    # TODO replace with final version of tags in Alice
    GET_TAGS = RequestMockResponse(
        """ [
    {
        "id": "5e78f73dbed03611f8b825ae",
        "name": "action",
        "workspaceId": "5e5b8b3a95ae537fbde06e58",
        "archived": false
    },
    {
        "id": "5e78f822e0083d68087a09db",
        "name": "analytics",
        "workspaceId": "5e5b8b3a95ae537fbde06e58",
        "archived": false
    },
    {
        "id": "5e78f857e0083d68087a09f7",
        "name": "communication",
        "workspaceId": "5e5b8b3a95ae537fbde06e58",
        "archived": false
    },
    {
        "id": "5e78f774e0083d68087a0994",
        "name": "meeting",
        "workspaceId": "5e5b8b3a95ae537fbde06e58",
        "archived": false
    },
    {
        "id": "5e78f7cbff66a323df51bec6",
        "name": "procrastination",
        "workspaceId": "5e5b8b3a95ae537fbde06e58",
        "archived": false
    },
    {
        "id": "5e78f75af39d6556cd261ecc",
        "name": "traveling",
        "workspaceId": "5e5b8b3a95ae537fbde06e58",
        "archived": false
    },
    {
        "id": "5e78f763e0083d68087a098f",
        "name": "waiting",
        "workspaceId": "5e5b8b3a95ae537fbde06e58",
        "archived": false
    }
] """, 200)

    # calling /workspaces/<workspace id>/clients
    # TODO replace with English version of Alice
    GET_CLIENTS = RequestMockResponse(
        """ [
    {
        "id": "5e654fc62fe7db4da05e7958",
        "name": "Читатель",
        "workspaceId": "5e64e36443f3817e058c24d7",
        "archived": false
    }
] """, 200)

    # calling /workspaces/<workspace id>/user/<user id>/time-entries
    #TODO replace with English version of Alice
    GET_TIME_ENTRIES = RequestMockResponse(
        """ [
    {
        "id": "5e6542032fe7db4da05e734a",
        "description": "Подошла к закрытой дверце и поняла что забыла ключ",
        "tagIds": [
            "5e6549d7ea0d47492eb3eaa2"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f85f43f3817e058c2d50",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T19:30:00Z",
            "end": "2020-03-08T20:00:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e65412343f3817e058c4e06",
        "description": "Пыталась поместиться в нору",
        "tagIds": [
            "5e6549d7ea0d47492eb3eaa2"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7ef43f3817e058c2d29",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T18:30:00Z",
            "end": "2020-03-08T19:00:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e654100ea0d47492eb3e6a1",
        "description": "Открывала маленькую дверь в сад золотым ключиком",
        "tagIds": [
            "5e6549d7ea0d47492eb3eaa2"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7ef43f3817e058c2d29",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T18:00:00Z",
            "end": "2020-03-08T18:30:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e65408b43f3817e058c4dde",
        "description": "Пыталась открыть двери в конце коридора в зале",
        "tagIds": [
            "5e6549d7ea0d47492eb3eaa2"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7ef43f3817e058c2d29",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T17:30:00Z",
            "end": "2020-03-08T18:00:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e6540582fe7db4da05e729c",
        "description": "Следование за кроликом в коридоре",
        "tagIds": [
            "5e6549dcea0d47492eb3eaa6"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7ef43f3817e058c2d29",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T17:00:00Z",
            "end": "2020-03-08T17:30:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e65402343f3817e058c4db7",
        "description": "Самоосвидетельствование на предмет отсутствия переломов и ушибов при падении в кучу валежника",
        "tagIds": [
            "5e6549d7ea0d47492eb3eaa2"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7b943f3817e058c2d0d",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T16:30:00Z",
            "end": "2020-03-08T17:00:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e653fc943f3817e058c4d88",
        "description": "Контроль кошки Дины на предмет поедания мошек",
        "tagIds": [
            "5e6549d42fe7db4da05e768f"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7b943f3817e058c2d0d",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T16:00:00Z",
            "end": "2020-03-08T16:30:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e653ee92fe7db4da05e71dc",
        "description": "Подготовилась к встрече с антипатиями (Новая Зеландия)",
        "tagIds": [
            "5e6549daea0d47492eb3eaa3"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7b943f3817e058c2d0d",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T15:30:00Z",
            "end": "2020-03-08T16:00:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e653e9543f3817e058c4d10",
        "description": "Пыталась определить свои координаты (местоположение)",
        "tagIds": [
            "5e6549d7ea0d47492eb3eaa2"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7b943f3817e058c2d0d",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T15:00:00Z",
            "end": "2020-03-08T15:30:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e653e552fe7db4da05e71a6",
        "description": "Переместила банку апельсинового варенья с полки в шкаф",
        "tagIds": [
            "5e6549d7ea0d47492eb3eaa2"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7b943f3817e058c2d0d",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T14:30:00Z",
            "end": "2020-03-08T15:00:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e653e09ea0d47492eb3e550",
        "description": "Изучала предметы на стенах колодца",
        "tagIds": [
            "5e6549d42fe7db4da05e768f"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7b943f3817e058c2d0d",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T13:30:00Z",
            "end": "2020-03-08T14:30:00Z",
            "duration": "PT1H"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e653dc72fe7db4da05e716a",
        "description": "Юркнула в нору",
        "tagIds": [
            "5e6549dcea0d47492eb3eaa6"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7b943f3817e058c2d0d",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T13:00:00Z",
            "end": "2020-03-08T13:30:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e653d9e43f3817e058c4cad",
        "description": "Преследовала кролика по полю до норы",
        "tagIds": [
            "5e6549dcea0d47492eb3eaa6"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7a443f3817e058c2d04",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T12:30:00Z",
            "end": "2020-03-08T13:00:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e653d76ea0d47492eb3e4e4",
        "description": "Наблюдала за кроликом с часами",
        "tagIds": [
            "5e6549d7ea0d47492eb3eaa2"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7a443f3817e058c2d04",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T12:00:00Z",
            "end": "2020-03-08T12:30:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e653cc243f3817e058c4c49",
        "description": "Принимала управленческое решение о венке",
        "tagIds": [
            "5e6549d42fe7db4da05e768f"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7a443f3817e058c2d04",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T11:30:00Z",
            "end": "2020-03-08T12:00:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e653c4e2fe7db4da05e70bb",
        "description": "Анализировала книжку сестры без картинок и разговоров",
        "tagIds": [
            "5e6549d42fe7db4da05e768f"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7a443f3817e058c2d04",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T11:00:00Z",
            "end": "2020-03-08T11:30:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e653c1443f3817e058c4c05",
        "description": "Ожидала начала работы с сестрой",
        "tagIds": [
            "5e6549d043f3817e058c51c4"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f7a443f3817e058c2d04",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-08T09:00:00Z",
            "end": "2020-03-08T11:00:00Z",
            "duration": "PT2H"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e6541b42fe7db4da05e7330",
        "description": "Сложилась как подзорная труба",
        "tagIds": [
            "5e6549d7ea0d47492eb3eaa2"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f85f43f3817e058c2d50",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-01T20:30:00Z",
            "end": "2020-03-01T21:00:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e65417e43f3817e058c4e2a",
        "description": "Отпила немного из пузырька и выпила полностью",
        "tagIds": [
            "5e6549d7ea0d47492eb3eaa2"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f85f43f3817e058c2d50",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-01T20:00:00Z",
            "end": "2020-03-01T20:30:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e6541652fe7db4da05e730a",
        "description": "Убедилась в отсутствии яда",
        "tagIds": [
            "5e6549d42fe7db4da05e768f"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f85f43f3817e058c2d50",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-01T19:30:00Z",
            "end": "2020-03-01T20:00:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    },
    {
        "id": "5e65414f43f3817e058c4e15",
        "description": "Нашла пузырек с жидкостью",
        "tagIds": [
            "5e6549d7ea0d47492eb3eaa2"
        ],
        "userId": "5e64e65643f3817e058c261a",
        "billable": true,
        "taskId": "5e64f85f43f3817e058c2d50",
        "projectId": "5e64f6804aa5d3718482d06b",
        "timeInterval": {
            "start": "2020-03-01T19:00:00Z",
            "end": "2020-03-01T19:30:00Z",
            "duration": "PT30M"
        },
        "workspaceId": "5e64e36443f3817e058c24d7",
        "isLocked": false,
        "customFieldValues": null
    }
] """, 200)

    # calling post '/workspaces/<workspace id>/time-entries'
    POST_TIME_ENTRY = RequestMockResponse(
     """{"id": "123456", "description": "testing description", "tagIds": null,
     "userId": "123456", "billable": false, "taskId": null, "projectId": "123456",
     "timeInterval": {"start": "2019-10-23T17:18:58Z", "end": null, "duration": null},
     "workspaceId": "123456", "isLocked": false}
     """, 201
    )
