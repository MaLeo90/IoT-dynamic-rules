import requests
import json
import argparse
import hashlib
import logging

#Iniciar el logger
logger = logging.getLogger(__name__)

TOKEN = "Your_Token"
URL = 'https://api.koodous.com/apks/'

HEADERS = {"Authorization": "Token "+TOKEN}

def __generate_256_hash(file_path):
	f = open(file_path, 'rb')
	fr = f.read()
	hasher_256 = hashlib.sha256()
	hasher_256.update(fr)
	sha256 = hasher_256.hexdigest()
	f.close()
	return sha256	

def upload_sample(sample):
	global URL,HEADERS, logger
	logger.warning("Generating hash of sample")
	url_to_send = URL + __generate_256_hash(sample) + "/get_upload_url"
	
	logger.warning("Getting upload url from koodous")
	request = requests.get(url=url_to_send,headers=HEADERS)
	
	if (request.status_code == 200):
		logger.warning("Url recieved, preparing post to Koodous")
		url_recieved = request.json()
		to_upload = {"file":open(sample,'rb')}
		request_of_upload = requests.post(url=url_recieved["upload_url"], files = to_upload)
		
		if(request_of_upload.status_code == 200):
			logger.warning("Sample uploaded")
			return True
		else:
			logger.warning("Error uploading sample")
			return False
	else:
		logger.warning("Error getting url")
		return False

def analyze_sample(sample):
	global URL,HEADERS, logger
	logger.warning("Generating hash of sample")
	url_to_send = URL + __generate_256_hash(sample) + "/analyze"
	
	logger.warning("Requesting analysis to Koodous")
	request = requests.get(url=url_to_send,headers=HEADERS)
	
	analysis = request.json()
	logger.warning("Analysis done")
	return analysis

def get_analysis_from_sample(sample):
	global URL,HEADERS, logger
	logger.warning("Generating hash of sample")
	url_to_send = URL + __generate_256_hash(sample) + "/analysis"
	
	logger.warning("Getting analysis from koodous")
	request = requests.get(url=url_to_send,headers=HEADERS)
	
	analysis = request.json()
	logger.warning("Analysis getted")
	print(analysis)
	return analysis

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Evaluate a file with Yara rule')
	parser.add_argument("-f","--file", help="Filepath to the file to evaluate")
	args = parser.parse_args()
	
	get_analysis_from_sample(args.file)


