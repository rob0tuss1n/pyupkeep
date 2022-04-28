import requests
import json

class BaseObject:
        url = ''
        def __init__(self, parent, mainURL):
            self.parent = parent
            self.url = mainURL

        def getAll(self):
            r = requests.get(self.url, headers=self.parent.header)
            self.parent.assets = r.json()['results']
            return r.json()

        def get(self, objID):
            objURL = '{}/{}'.format(self.url, objID)
            r = requests.get(objURL, headers=self.parent.header)
            return r.json()

        def set(self, objID, data):
            objURL = '{}/{}'.format(self.url, objID)
            r = requests.patch(objURL, data=data, headers=self.parent.header)
            return r.json()

class UpkeepClient:
    assets = {}
    assetStatuses = {}
    header = {}
    authUser = ''
    authPassword = ''

    def __init__(self, user, password):
        self.authUser = user
        self.authPassword = password
        self.authentication = self.Authentication(user, password)
        loginResults = self.authentication.logIn()
        if loginResults['success']: 
            self.header['Session-Token'] = self.authentication.sessionToken['value']
        self.asset = self.Asset(self, 'https://api.onupkeep.com/api/v2/assets/')
        self.customer = self.Customer(self, 'https://api.onupkeep.com/api/v2/customers/')
        self.customField = self.Customer(self, 'https://api.onupkeep.com/api/v2/custom-fields/assets')
        self.location = self.Location(self, 'https://api.onupkeep.com/api/v2/locations/')
        self.meter = self.Meter(self,'https://api.onupkeep.com/api/v2/meters/')
        self.part = self.Part(self, 'https://api.onupkeep.com/api/v2/parts/')
        self.preventativeMaintenance = self.PreventativeMaintenance(self,'https://api.onupkeep.com/api/v2/preventative-maintenance/')
        self.requests = self.Requests(self, 'https://api.onupkeep.com/api/v2/requests/')
        self.team = self.Team(self, 'https://api.onupkeep.com/api/v2/teams/')
        self.user = self.User(self, 'https://api.onupkeep.com/api/v2/users/')
        self.vendor = self.Vendor(self, 'https://api.onupkeep.com/api/v2/vendors/')
        self.workOrder = self.WorkOrder(self, 'https://api.onupkeep.com/api/v2/work-orders/')

    class Asset(BaseObject):
        customFieldURL = 'https://api.onupkeep.com/api/v2/custom-fields/assets'
    
        def __init__(self, parent, mainURL):
            self.parent = parent
            self.header = parent.header
            self.url = mainURL
            self.downtimeStatus = self.downtimeStatus(self, "https://api.onupkeep.com/api/v2/asset-downtime-statuses")

        class downtimeStatus(BaseObject):
            statusURL = ''
            def __init__(self, parent, mainURL):
                self.parent = parent
                self.url = mainURL
        
        def setDowntimeStatus(self, assetID, status):
            assetURL = '{}/{}'.format(self.url, assetID)
            content = {}
            content['downtimeStatus'] = status
            r = requests.patch(assetURL, data=content, headers=self.parent.header)
            return r.json()


    class Authentication:
        url = "https://api.onupkeep.com/api/v2/auth/"
        credentials = {}
        sessionToken = {}

        def __init__(self, user, password):
            self.user = user
            self.password = password
            self.updateCredentials()

        def updateCredentials(self, user = '', password = ''):
            if user == '':
                self.credentials['email'] = self.user
            else:
                self.credentials['email'] = user

            if password == '':
                self.credentials['password'] = self.password
            else:
                self.credentials['password'] = password


        def logIn(self, authCredential=credentials):
            # Do login request
            r = requests.post(self.url, authCredential)

            if r.json()['success']:
                self.sessionToken['status'] = 'OK'
                self.sessionToken['value'] = r.json()['result']['sessionToken']
                self.sessionToken['expireTimestamp'] = r.json()['result']['expiresAt']
            else:
                self.sessionToken['status'] = 'NOK'

            return r.json()

    class Customer(BaseObject):
        def __init__(self, parent, mainURL):
            self.parent = parent

    class CustomField(BaseObject):
        def __init__(self, parent, mainURL):
            self.parent = parent

    class Location(BaseObject):
        def __init__(self, parent, mainURL):
            self.parent = parent

    class Meter(BaseObject):
        def __init__(self, parent, mainURL):
            self.parent = parent
            self.url = mainURL

    class Part(BaseObject):
        def __init__(self, parent, mainURL):
            self.parent = parent
            self.url = mainURL

    class PreventativeMaintenance(BaseObject):
        def __init__(self, parent, mainURL):
            self.parent = parent
            self.url = mainURL

    class Requests(BaseObject):
        def __init__(self, parent, mainURL):
            self.parent = parent
            self.url = mainURL

    class Team(BaseObject):
        def __init__(self, parent, mainURL):
            self.parent = parent
            self.url = mainURL

    class User(BaseObject):
        def __init__(self, parent, mainURL):
            self.parent = parent
            self.url = mainURL

    class Vendor(BaseObject):
        def __init__(self, parent, mainURL):
            self.parent = parent
            self.url = mainURL

    class WorkOrder(BaseObject):
        def __init__(self, parent, mainURL):
            self.parent = parent
            self.url = mainURL
