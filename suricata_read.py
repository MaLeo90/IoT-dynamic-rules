import logging
import glob
import evaluate_binary
import os
import keys
import subprocess
import time

#Iniciar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_interesting_files():
	logger.info("Getting list of .exe objects")
	#temporal_zip = glob.glob("objects/*.zip")

	objects = glob.glob("objects/*")
	#logger.warning(objects)
	return objects

if __name__ == '__main__':
	total = 0
	while (True):
		time.sleep(10)
		objects = get_interesting_files()
		for i in objects:
			if(not ".meta" in i):
				total+=1
				evaluate_binary.evaluate(i)
				os.remove(i)
				os.remove(i+".meta")
		print(evaluate_binary.get_count())
		print("Total :"+str(total))
	
