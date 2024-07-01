import requests
import json
import argparse
import hashlib
import logging
from keys import TOKEN
import time

#Iniciar el logger
logger = logging.getLogger(__name__)

URL = 'https://www.virustotal.com/vtapi/v2/'

def __generate_256_hash(file_path):
	f = open(file_path, 'rb')
	fr = f.read()
	hasher_256 = hashlib.sha256()
	hasher_256.update(fr)
	sha256 = hasher_256.hexdigest()
	f.close()
	return sha256

def __obtain_report(sample):
	logger.info("Generating hash of sample")
	url_to_send = URL + "file/report"
	params = {'apikey':TOKEN, 'resource':__generate_256_hash(sample)}
	
	logger.info("Sending request to get report for hash: "+__generate_256_hash(sample))
	response = requests.get(url_to_send, params=params).json()
	return response

def get_behavior(sample):
	global URL,TOKEN,logger

	url_to_send = URL + "file/behaviour"
	params = {'apikey':TOKEN, 'resource':__generate_256_hash(sample)}
	logger.info("Sending request to get behaviour report for hash: "+__generate_256_hash(sample))

	response = requests.get(url_to_send, params=params).json()
	return response

def get_report_from_sample(sample):
	global URL,TOKEN,logger
	
	response = __obtain_report(sample)
	#print(response)
	if(int(response["response_code"]) == 1):
		if(response["positives"]>0):
			logger.info("File detected as malicius by VirusTotal")
			return True
		else:
			logger.info("File is clean to VirusTotal")
			return False
	elif(int(response["response_code"]) == 0):
		logger.info("File not found, uploading to analysis")
		upload_response=__upload_sample(sample)
		time.sleep(200)
		response = __obtain_report(sample)
		while (not int(response["response_code"]) == 1):
			print(response)
			time.sleep(10)
			response = __obtain_report(sample)			
		if(response["positives"]>0):
			logger.info("File detected as malicius by VirusTotal")
			return True
		else:
			logger.info("File is clean to VirusTotal")
			return False
	else:
		logger.error("Error getting report")
		return False
		

def __upload_sample(sample):
	global URL,TOKEN,logger
	url_to_send = URL + "file/scan"
	params = {'apikey':TOKEN}
	files = {'file':(sample,open(sample,'rb'))}
	logger.info("Uploading file")
	response = requests.post(url_to_send, files=files, params=params).json()
	logger.info("Uploaded")
	#logger.info(response)
	return response

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Evaluate a file with VirusTotal')
	parser.add_argument("-f","--file", help="Filepath to the file to evaluate")
	args = parser.parse_args()

	get_report_from_sample(args.file)
	
		
