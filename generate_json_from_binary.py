#Adaptado de https://github.com/Yara-Rules/r2yara/blob/master/generate_report.py
import subprocess
import json
import sys
import logging

#Iniciar el logger
logger = logging.getLogger(__name__)

def rabin2_call(binary):
    """
    rabin2
    -i              imports
    -U              resoUrces
    -S              sections
    -E              globally exportable symbols
    -I              binary info
    -l              linked libraries
    -j              output in json
    """
    args = ["rabin2", "-iUSEIlj", binary]

    value, _ = subprocess.Popen(args, stdout = subprocess.PIPE).communicate()
    value = value.decode("utf-8")
    try:
        #print (value)
        value = json.loads(value.replace('\n', ' '))
    except Exception:
        print ("Cannot generate bin information with rabin2 rahash2")
        #print why
        value = {}
    return value

def rahash2_call(binary):
    args = ["rahash2", "-a", "all", "-j",  binary]

    value, _ = subprocess.Popen(args, stdout = subprocess.PIPE).communicate()
    value = value.decode("utf-8")
    try:
        value = json.loads(value.replace('\n', ' '))
    except Exception:
        print ("Cannot generate hashes with rahash2")
        value = {}
    return value

def generate(binary):
    rabin2_json = rabin2_call(binary)
    rahash2_json = rahash2_call(binary)
    rabin2_json['hash'] = rahash2_json
    logger.warning("Finished creating json report")
    return(json.dumps(rabin2_json))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generates a new event on MISP')
	parser.add_argument("-b","--binary", help="Filepath of the binary")
	args = parser.parse_args()
	generate(args.binary, args.who)	
