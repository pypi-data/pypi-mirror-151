import sys, argparse, asyncio, JsonParser
import EventHub.Event as Event
import Settings.Environment as Environment

def run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(send_events_using_command_line())
    loop.close()
    return result

def run_send_events(event_type, env_name, client_code, account_name, events_json):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(send_events(event_type, env_name, client_code, account_name, events_json))
    loop.close()
    return result

async def send_events_using_command_line():
    events = JsonParser.parse(args.events)
    event_type = args.type
    client_code = args.code
    account_name = args.account
    return await Event.run(event_type, client_code, account_name, events)

async def send_events(event_type, env_name, client_code, account_name, events):
    Environment.set_environment(env_name)   
    return await Event.run(event_type, client_code, account_name, events)


#Declare script parameters
parser = argparse.ArgumentParser()
parser.add_argument("--env", help="Sets environment. Development, Production, QA or Learn", type=str)
parser.add_argument("--code", help="Sets Storis client code", type=str)
parser.add_argument("--events", help="Sets Storis client code")
parser.add_argument("--account", help="Sets Storis Account name")
parser.add_argument("--type", help="Sets Storis Event type")

args, unknown = parser.parse_known_args()

if args.env != None:
    Environment.set_environment(args.env)


    
