import json

class Settings(object):
    def __init__(self, connectionString, name):
        self.connectionString = connectionString
        self.name = name

    def object_decoder(obj):
        if '__type__' in obj and obj['__type__'] == 'Settings':
            return User(obj['connectionString'], obj['name'])
        return obj
