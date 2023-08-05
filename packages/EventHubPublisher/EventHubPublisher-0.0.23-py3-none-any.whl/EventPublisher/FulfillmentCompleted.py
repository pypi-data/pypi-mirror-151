import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

import EventHub.SendEvents as SendEvents

def run(env_name, client_code, account_name, events_json):
    return SendEvents.send_events('FulfillmentCompleted', env_name, client_code, account_name, events_json)

# for testing 
if sys.stdin and len(sys.argv) > 0:
    print(SendEvents.run('FulfillmentCompleted'))
    print('order.create events were sent.')


