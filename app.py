import keys
import requests
import middleware_client
def send(filePath, detectedBy):
    for client in middleware_client.getUsers():
        data = {"tittle": "Malware found", "body": "Malware "+filePath+" was detected using "+detectedBy, "idUser":client, "type": "Malware Alert", "serial": keys.serial}																																																																															
        response = requests.post(keys.fcm_sender_url, json=data)
        print(response.status_code, response.reason)

def sendVulnerabilityAlert(body):
    for client in middleware_client.getUsers():
        data = {"tittle": "Vulnerability found", "body": body, "idUser":client, "type": "Vulnerability Alert", "serial": keys.serial}
        response = requests.post(keys.fcm_sender_url, json=data)
        print(response.status_code, response.reason)
