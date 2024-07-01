from pymisp import PyMISP
from keys import misp_url,misp_key
import argparse
import logging

#Regla de Yara que empezará a crearse
yara_rule = ''
#Lista que contiene los hashes posibles
hashes = ["md5","sha1","sha224","sha256","sha384","sha512","sha512/224","sha512/256"]
#Lista que contiene los hashes posibles con un filename|<tipo_hash>
filename_hashes = ["filename|"+x for x in hashes]
#Lista que contiene los hashes repetidos
repeated_hashes =[[] for x in range(len(hashes))]
#Iniciar el logger
logger = logging.getLogger(__name__)

def __init(url, key):
    return PyMISP(url, key, True, 'json', debug=True)


def generate_rule_from_event(id_event,printable,r_import):
    global yara_rule,repeated_hashes,hashes, logger
    misp = __init(misp_url, misp_key)
    if(r_import==1):
        yara_rule += 'import "r2" \n\nrule '
    else:
        yara_rule += 'rule '
    logger.info("Initializing MISP conecction")
    logger.info("Getting event: "+str(id_event))
    event = misp.get_event(id_event)

    #yara_rule += "Event_"+str(id_event)+"\n{\n\tstrings:\n\t\t"
    yara_rule += "Event_"+str(id_event)+"\n{\n\t"
    logger.info("Getting atributes from the event")
    for i in event["Event"]["Attribute"]:
        __add_hash(i)
    #Añadir todos los hashes recuperados a los strings
    '''for i in range(len(repeated_hashes)):
        for j in range(len(repeated_hashes[i])):
            #Añadir un string
            yara_rule += "$"+hashes[i]+"_"+str(j)+" = "+'"'+repeated_hashes[i][j]+'"'+"\n\t\t"
    #Añadir las condiciones de detección'''
    yara_rule += "condition:\n\t\t"
    logger.info("Added "+str(len(event["Event"]["Attribute"]))+" hashes")
    logger.info("Adding detection conditions")
    for i in range(len(repeated_hashes)):
        for j in range(len(repeated_hashes[i])):
            #Añadir una condición
            #yara_rule += "$"+hashes[i]+"_"+str(j)+" == r2.hash."+hashes[i]+" or\n\t\t"
            yara_rule += '"'+repeated_hashes[i][j]+'"'+" == r2.hash."+hashes[i]+" or\n\t\t"
    yara_rule = yara_rule[:len(yara_rule)-5]
    yara_rule += "\n}\n"
    logger.info("Rule generated")
    if(printable==1):
        print(yara_rule)
    else:
        return yara_rule

def __add_hash(attribute):
    global hashes,filename_hashes,repeated_hashes,logger
    
    if(attribute["category"] in ["Payload delivery","Payload installation","Artifacts dropped"]):
        #logger.info("Adding hash to Yara rule")
        if(attribute["type"] in hashes):
            repeated_hashes[hashes.index(attribute["type"])].append(attribute["value"])
        elif(attribute["type"] in filename_hashes):
            repeated_hashes[filename_hashes.index(attribute["type"])].append(attribute["value"].split("|")[1])
        #logger.info("Ok")
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate rules to Yara using MISP events.')
    parser.add_argument("-e", "--event", type=int, help="The id of the event to update.")
    parser.add_argument("-p", "--printable", type=int, help="1 if you are printing the rule, 0 otherwise.")
    parser.add_argument("-r", "--r_import", type=int, help="0 if you are generating several rules, 1 otherwise.")
    
    args = parser.parse_args()
    generate_rule_from_event(args.event,args.printable,args.r_import)

