from pymisp import PyMISP
from keys import misp_url, misp_key
import argparse
import logging


#Iniciar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def add_attribute(eventId,atType,value):
    global logger
    misp = __init(misp_url, misp_key)

    logger.info("Connecting MISP")

    logger.info("Getting event with id: "+eventId)
    event = misp.get_event(eventId)

    logger.info("Adding attribute to event")
    event = misp.add_named_attribute(event, atType, value, "Artifacts dropped")
    
    logger.info("Done")


def __init(url, key):
    return PyMISP(url, key, True, 'json', debug=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adds an attribute to an event in MISP.')
    parser.add_argument("-e", "--event", type=int, help="The id of the event to update.")
    parser.add_argument("-t", "--type", help="The type of the added attribute")
    parser.add_argument("-v", "--value", help="The value of the attribute")
    args = parser.parse_args()

    add_attribute(args.event,args.type,args.value)
