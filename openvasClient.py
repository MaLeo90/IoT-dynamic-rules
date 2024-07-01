from gvm.connections import UnixSocketConnection
from gvm.transforms import EtreeCheckCommandTransform
from gvm.protocols.latest import Gmp
import app

path = "/var/run/openvasmd.sock"
connection = UnixSocketConnection(path=path)
transform = EtreeCheckCommandTransform()
user="admin"
password="admin"
gmp = Gmp(connection=connection, transform=transform)
with gmp:
	gmp.authenticate(user,password)
	tasks = gmp.get_tasks()
	for id_task in tasks.xpath('//task/@id'):
		print("Id_Task: "+id_task)
		task = gmp.get_task(id_task)
		for id_report in task.xpath('//reports/report/@id'):
			print("Id_Report: "+id_report)
			body = ""
			body += "Debug: "+task.xpath('//reports/report[@id=\''+id_report+'\']/result_count/debug')[0].text+"\n"
			body += "Hole: "+task.xpath('//reports/report[@id=\''+id_report+'\']/result_count/hole')[0].text+"\n"
			body += "Info: "+task.xpath('//reports/report[@id=\''+id_report+'\']/result_count/info')[0].text+"\n"
			body += "Log: "+task.xpath('//reports/report[@id=\''+id_report+'\']/result_count/log')[0].text+"\n"
			body += "Warning: "+task.xpath('//reports/report[@id=\''+id_report+'\']/result_count/warning')[0].text+"\n"
			body += "Severity: "+task.xpath('//reports/report[@id=\''+id_report+'\']/severity')[0].text
			print(body)
#			app.sendVulnerabilityAlert(body)
			
			
