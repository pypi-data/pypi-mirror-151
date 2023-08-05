import sys, traceback, json, asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from azure.eventhub.exceptions import EventHubError
import Settings.Configuration as Configuration
from EventHub.Response import Response

@asyncio.coroutine
async def run(event_type, client_code, account_name, events):
    try:
        producer = get_producer()
        await send_event_data_batch_with_partition_key(producer, event_type, client_code, account_name, events)
        print("Events for client: " + client_code + " has been sent.")
        response = Response(True, "")
        return response.toJSON()
    except EventHubError as eh_err:
        print("Sending error: ", eh_err)
        response = Response(False, traceback.format_exc())
        return response.toJSON()
    except Exception as eh_err:
        response = Response(False, traceback.format_exc())
        return response.toJSON()

async def send_event_data_batch_with_partition_key(producer, event_type, client_code, account_name, events):
    #Specifying partition_key
    event_data_batch_with_partition_key = await producer.create_batch(partition_key=get_partition_key(event_type))

    #Add events to the batch.
    length = len(events)
    for index in range(0, length):
        event_data = create_event_data(events[index], client_code, account_name, event_type)
        event_data_batch_with_partition_key.add(event_data)
        #print(event_data)
        
    await producer.send_batch(event_data_batch_with_partition_key)

def get_producer():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=Configuration.get_connection_string(), 
        eventhub_name=Configuration.get_eventhub_name())
    return producer

def get_partition_key(event_type):
    return event_type

def create_event_data(event_body, client_code, account_name, event_type):
    event_data = EventData(str(event_body))
    event_data.properties = {'event_type': event_type, 'client_code': client_code, 'account_name': account_name}
    return event_data

    


