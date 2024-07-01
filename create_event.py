from pymisp import PyMISP
from keys import misp_url,misp_key
import argparse
import logging

#Iniciar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_event(distribution,threat_level,analysis,info):
    global logger
    
    misp = __init(misp_url, misp_key)
    logger.info("Creating MISP connection")
    logger.info("Creating event")
    event = misp.new_event(distribution,threat_level,analysis,info)
    logger.info("Event created")
    return event

def __init(url, key):
    return PyMISP(url, key, True, 'json', debug=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates an event on MISP.')
    parser.add_argument("-d", "--distrib", type=int, help="The distribution setting used for the attributes and for the newly created event, if relevant. [0-3].")
    parser.add_argument("-i", "--info", help="Used to populate the event info field if no event ID supplied.")
    parser.add_argument("-a", "--analysis", type=int, help="The analysis level of the newly created event, if applicatble. [0-2]")
    parser.add_argument("-t", "--threat", type=int, help="The threat level ID of the newly created event, if applicatble. [1-4]")
    args = parser.parse_args()

    create_event(args.distrib, args.threat, args.analysis, args.info)
