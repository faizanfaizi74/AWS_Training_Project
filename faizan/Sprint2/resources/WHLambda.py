# Creating Handler for obtaining Latency and Availability for Webresource
import urllib3
from datetime import datetime

URL_TO_MONITOR = "skipq.org"

def lambda_handler(event, context):
    # get latency and availability of the web resource
    availability = getAvailability()
    latency = getLatency()
    print(f"Availability: {availability} Latency: {latency}")


# input parameters: None
# return values: boolean 1 or 0
def getAvailability():
    http = urllib3.PoolManager()
    response = http.request("GET", URL_TO_MONITOR)
    
    if response.status==200:
        return 1.0
    else:
        return 0.0


# input parameters: None
# return values: latency in seconds
def getLatency():
    http = urllib3.PoolManager()
    start = datetime.now()
    response = http.request("GET", URL_TO_MONITOR)

    end = datetime.now()
    diff = end - start  # time difference
    latencySec = round(diff.microseconds * .000001, 6)
    
    return latencySec