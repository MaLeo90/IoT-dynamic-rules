from pymisp import PyMISP
from keys import misp_url,misp_key
import argparse
import logging

#Iniciar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def __init(url, key):
    return PyMISP(url, key, True, 'json', debug=True)

def publish_event(eventId):
    global logger

    misp = __init(misp_url, misp_key)
    logger.info("Initializing MISP conecction")

    logger.info("Getting event with id: "+eventId)
    event = misp.get_event(eventId)

    logger.info("Publishing event")
    misp.publish(event)
    logger.info("Done")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Publishes an event to MISP.')
    parser.add_argument("-e", "--event", type=int, help="The id of the event to publish")

    args=parser.parse_args()

    publish_event(args.event)
    
