###### Plan for development
Add Clockify APIObjects
    Client
    Tag
    Task
    UserGroup
    НourlyRate
Modify User
    Add User specific attributes:
        Update User operations wih new attributes
        Update Tests
Populate Users from workspace (add_users)
    Add Tests
        factories
        a_mock_api

Generate hourly_rates to Users / projects
Add Task
Init tasks from dict
Exceptions
    Exception HourlyRate >=0
APIObject add functionality hashable to add hourly rates in dict with project as a key
    __eq__
    __ne__
    __hash__
