from pymisp import PyMISP
from keys import misp_url, misp_key
import argparse
import logging
import add_attribute
import create_event
import publish_event
import generate_json_from_binary
import sys
import json
import generate_rule

#Iniciar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#Lista que contiene los hashes posibles
hashes = ["md5","sha1","sha224","sha256","sha384","sha512","sha512/224","sha512/256"]

def __init(url, key):
    return PyMISP(url, key, True, 'json', debug=True)

def generate(binary,who_detected):
	global hashes
	logger.info("Generating json report for sample")
	jsonReport = generate_json_from_binary.generate(binary)
	created = create_event.create_event(0,3,0,"Detected by "+who_detected)
	jsonReport = json.loads(jsonReport)
	reportHashes = jsonReport["hash"]
	logger.info("Adding hashes as attributes")
	for i in reportHashes:
		if(i["name"] in hashes):
			add_attribute.add_attribute(created["Event"]["id"],i["name"],i["hash"])
	logger.info("Done")
	if (who_detected != "YaraRules"):
		logger.info("Generating rule from event")
		yara_rules = generate_rule.generate_rule_from_event(created["Event"]["id"],0,0)
		with open("rules.yar",'a') as rule:
			rule.write(yara_rules)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generates a new event on MISP')
	parser.add_argument("-b","--binary", help="Filepath and name of the binary")
	parser.add_argument("-w","--who", help="Who detected the sample")
	args = parser.parse_args()
	generate(args.binary, args.who)
