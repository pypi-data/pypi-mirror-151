import os, JsonParser

def get_environment():
    env = os.getenv('APP_ENVIRONMENT')
    if env == None:
        raise Exception("Environment is not set. Set Production or Development by calling 'python Environment.py <env_name>'")
    return env

def get_environment_settings():
    settingsJson = os.getenv('APP_ENVIRONMENT_SETTINGS')
    if settingsJson == None:
        raise Exception("Environment settings are not set")
    env = get_environment()
    settings = JsonParser.parse(settingsJson)
    return JsonParser.get_by_key(settings, env)

def read_settings():
    settings = JsonParser.parse_from_file('../settings.json')
    set_environment_settings(settings)

def set_environment_settings(settings):
    os.environ['APP_ENVIRONMENT_SETTINGS'] = JsonParser.serialize(settings)
    #print(os.environ['APP_ENVIRONMENT_SETTINGS'])

def set_environment(envirment_name):
    os.environ['APP_ENVIRONMENT'] = envirment_name
    read_settings()
    #print('Environment is set to -> ' + os.getenv('APP_ENVIRONMENT'))

