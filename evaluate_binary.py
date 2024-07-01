import argparse
import logging
import subprocess
import generate_event_from_binary
import koodous_api
import virus_total_api
import mail
from keys import alert_mail
import glob
import app
from machine_learning_api import Parser

#Iniciar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

yara_count = 0
external_count = 0
ml_count = 0


def get_count():
	return str(ml_count)+":"+str(yara_count)+":"+str(external_count)

def evaluate(file_path):
	global yara_count, external_count, ml_count
	print("Entered to evaluation with file "+file_path)
	print("ML")
	#logger.info("Nothing detected with Yara rules, sending binary to external analysis")
	parser = Parser()			
	report = parser.send(file_path)
	#Detection
	if(report == "MAL"):
		ml_count+=1
		app.send(file_path, "Machine Learning")
	else:
		print("Yara")
		logger.info("Executing Yara rules on rules in rules.yar")
		args = ["yara","rules.yar",file_path]
		value, _ = subprocess.Popen(args, stdout = subprocess.PIPE).communicate()
		value = value.decode("utf-8").strip()
		if(len(value)>0):
			logger.info("Detected with rule: "+value)
			yara_count+=1
			app.send(file_path, "Yara Rules")
			#mail.send_mail(file_path,"Yara Rules",alert_mail)
			#generate_event_from_binary.generate(file_path,"Yara rules")
		else:
			print("VirusTotal")
			detected = virus_total_api.get_report_from_sample(file_path)
			if (detected):
				external_count+=1
			app.send(file_path, "VirusTotal")
			#mail.send_mail(file_path,"VirusTotal",alert_mail)
			#generate_event_from_binary.generate(file_path, "Virus total")
			#logger.info("Sending to machine learning")

				#mail.send_mail(file_path,"Machine Learning",alert_mail)
				#generate_event_from_binary.generate(file_path,"Machine Learning")
			#else:
			#	logger.info("Nothing detected, file is clean")
                        
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Evaluates a file using the defined Yara Rules, VirusTotal and VirusTotal Sandbox')
	parser.add_argument("-f","--file", help="Filepath to the file to evaluate")
	args = parser.parse_args()
	
	evaluate(args.file)

