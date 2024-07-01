import logging
import smtplib
import argparse
from keys import mail_server, mail_user, mail_pass

TO = []

SUBJECT = "Malware found"
TEXT = SUBJECT+": "+"Hello\nWe have found some malware in your system, the file found is "
MESSAGE = "Subject: {}\n\n{}".format(SUBJECT,TEXT)

#Iniciar el logger
logger = logging.getLogger(__name__)

def send_mail(file_path,who_detected,destiny):
	global logger,TO
	TO.append(destiny)
	logger.info("Getting SMTP server")
	server = smtplib.SMTP(mail_server)
	logger.info("Doing log in")
	server.starttls()
	server.login(mail_user,mail_pass)
	to_send=MESSAGE+file_path+", the detection used was "+who_detected
	logger.info("Sending mail")
	server.sendmail(mail_user,TO,to_send)
	logger.info("Mail sent")
	server.quit()

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Evaluate a file with VirusTotal')
	parser.add_argument("-f","--file", help="Filepath to the file to evaluate")
	parser.add_argument("-d","--detected", help="Tells who detected the filepath")
	parser.add_argument("-t","--to", help="Tells the mail to be sent")
	args = parser.parse_args()

	send_mail(args.file,args.detected,args.to)
	

