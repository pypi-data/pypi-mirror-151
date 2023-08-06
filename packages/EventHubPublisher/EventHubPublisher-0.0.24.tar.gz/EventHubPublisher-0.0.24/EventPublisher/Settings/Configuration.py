import Settings.Environment

def get():
    return Settings.Environment.get_environment_settings()

def get_connection_string():
    settings = get()
    return settings["ConnectionString"]

def get_eventhub_name():
    settings = get()
    return settings["Name"]
