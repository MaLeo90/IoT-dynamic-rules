import keys
import requests

def register():
	response = requests.post(keys.middleware_url+"/entity/register/sentinel/"+keys.serial)
	print(response.text)

def getUsers():
	response = requests.get(keys.middleware_url+"/entity/get/sentinel/"+ keys.serial + "/users")
	print(response)
	return response.json()

def getMyId():
	response = requests.get(keys.middleware_url+"/entity/get/sentinel/"+keys.serial)
	if(response.status_code == 500):
		return -1
	elif (response.status_code == 200):
		return int(response.text)
