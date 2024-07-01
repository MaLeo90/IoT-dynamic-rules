from androguard.core.bytecodes.apk import APK

class Model_Generator:

	def __init__(self,args**):
		self.apk_loader = args
		self.all_permissions = []
		self.all_lines = []
		self.current_line = []
		self.head = """% 1. Title: Cyberintelligence for IoT Machine Learning Model (APK)

% 2. Sources:
%	(a) Creator: David Esteban Useche
%	(b) Date: 12 May, 2018
@RELATION classificator\n
"""
		self.body = ""

	def get_permissions(self,file_path):
		return APK(file_path).get_permissions()

	def add_named_signatures(self,file_path):
		loaded_permissions = get_permissions(file_path)
		for i in loaded_permissions:
			if(not i in self.all_permissions):
				self.all_permissions.append(i)

	def load_new_line(self,file_path, classification):
		loaded_permissions = get_permissions(file_path)
		self.current_line = ["0" for n in range(len(self.all_permissions)+1)]
		for i in loaded_permissions:
			self.current_line[self.all_permissions.index(i)] = "1"
		self.current_line.[len(self.all_permissions)] = classification
		self.all_lines.append(self.current_line)

	def parse_head(self):
		for file_path in self.apk_loader:
			add_named_signatures(file_path)
		for permission in self.all_permissions:
			self.head += "@ATTRIBUTE "+permission+" NUMERIC\n"
		self.head+="@DATA\n"

	def parse_body(self):
		for line in self.all_lines:
			self.body += ",".join(line)

	def get_model(self):
		parse_head()
		parse_body()
		return self.head + self.body
