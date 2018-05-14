import json 
import random
from XHeader import XHeader
from EmailHeader import EmailHeader
from CandidateEmail import CandidateEmail
from Calculation import Calculation

class FileParser:

	def __init__(self,file_to_be_read,file_to_be_written):
		self.filename = file_to_be_read
		self.outputfilename = file_to_be_written

	def parse_line(self, single_line):
		single_line_json_array = json.loads(single_line)
		xHeader = XHeader()
		emailHeader = EmailHeader()
		counter = 0

		for single_element in single_line_json_array:
			if(counter == 0):
				emailHeader.set_messageID(single_line_json_array[single_element])
			if(counter == 1):
				emailHeader.set_date(single_line_json_array[single_element])
			if(counter == 2):	
				emailHeader.set_from(single_line_json_array[single_element])
			if(counter == 3):
				emailHeader.set_to(single_line_json_array[single_element])
			if(counter == 4):	
				emailHeader.set_subject(single_line_json_array[single_element])
			if(counter == 5):	
				emailHeader.set_cc(single_line_json_array[single_element])
			if(counter == 6):	
				emailHeader.set_mime_version(single_line_json_array[single_element])
			if(counter == 7):	
				emailHeader.set_content_type(single_line_json_array[single_element])
			if(counter == 8):	
				emailHeader.set_content_transfer_encoding(single_line_json_array[single_element])
			if(counter == 9):	
				emailHeader.set_bcc(single_line_json_array[single_element])
			if(counter == 10):	
				xHeader.set_xfrom(single_line_json_array[single_element])
			if(counter == 11):	
				xHeader.set_xto(single_line_json_array[single_element])
			if(counter == 12):	
				xHeader.set_xcc(single_line_json_array[single_element])
			if(counter == 13):	
				xHeader.set_xbcc(single_line_json_array[single_element])
			if(counter == 14):	
				xHeader.set_xfolder(single_line_json_array[single_element])
			if(counter == 15):	
				xHeader.set_xorigin(single_line_json_array[single_element])
			if(counter == 16):
				xHeader.set_xfilename(single_line_json_array[single_element])
			counter += 1

		candidateEmail = CandidateEmail(xHeader, emailHeader);
		return candidateEmail

	def read_file(self):
		candidateEmails = []

		with open(self.filename) as datafile:
			for line in datafile.readlines():
				candidateEmails.append(self.parse_line(line))

		return candidateEmails

	def write_file(self, data):
		print(data)
		
		with open(self.outputfilename,'a+') as datafile:
			datafile.write(data)
			datafile.close()

	def create_training_set(self):
		phishing_emails = ""
		not_phishing_emails = ""
		classification_emails = ""
		coinflip = 0
		calculator = Calculation()

		with open(self.filename) as datafile:
			for line in datafile.readlines():
				coinflip = random.randint(0,1)
				if coinflip == 1:
					if len(phishing_emails) + len(not_phishing_emails) < 70000:
						candidate_email = self.parse_line(line)
						candidate_email.classification = calculator.classify(candidate_email)
						if candidate_email.classification == "phishing":
							phishing_emails.append(line)
						else:
							not_phishing_emails += line
					else:
						classification_emails += line
				else:
					classification_emails += line

		with open("res/training-set-not-phishing.txt",'a+') as datafile:
			datafile.write(not_phishing_emails)
			datefile.close() 

		with open("res/training-set-phishing.txt",'a+') as datafile:
			datafile.write(phishing_emails)
			datefile.close() 

		with open("res/classification.txt",'a+') as datafile:
			datafile.write(classification_emails)
			datefile.close() 



