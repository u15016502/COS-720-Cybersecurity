from XHeader import XHeader
from EmailHeader import EmailHeader

class CandidateEmail:
	def __init__(self, x_header, email_header):
		self.x_header = x_header
		self.email_header = email_header
		self.classification = "not-phishing"

	def get_xheader(self):
		return self.x_header

	def get_emailheader(self):
		return self.email_header

	def get_classification(self):
		return self.classification

	def string_representation(self):
		string_representation = ""
		# string_representation += "Email Headers: \n"
		string_representation += "messageID: " 
		string_representation += str(self.email_header.get_messageID())
		string_representation += "\n"
		# string_representation += "date: " 
		# string_representation += str(self.email_header.get_date())
		# string_representation += "from: \n"
		# for email in self.email_header.get_from():
		# 	string_representation += email + "\n"

		# string_representation += "to: \n"
		# for email in self.email_header.get_to():
		# 	string_representation += email + "\n"

		string_representation += "subject: " 
		string_representation += str(self.email_header.get_subject())
		string_representation += "\n"
		# string_representation += "cc: \n"
		# for email in self.email_header.get_cc():
		# 	string_representation += email + "\n"

		# string_representation += "bcc: \n"
		# for email in self.email_header.get_bcc():
		# 	string_representation += email + "\n"

		# string_representation += "X-Headers: \n"
		# string_representation += "xfrom: \n"
		# for email in self.x_header.get_xfrom():
		# 	string_representation += email + "\n"

		# string_representation += "xto: \n"
		# for email in self.x_header.get_xto():
		# 	string_representation += email + "\n"

		# string_representation += "xcc: \n"
		# for email in self.x_header.get_xcc():
		# 	string_representation += email + "\n"

		# string_representation += "xbcc: \n"
		# for email in self.x_header.get_xbcc():
		# 	string_represenation += email + "\n"

		return string_representation