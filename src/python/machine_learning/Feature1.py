#Test for feature: misspelt words in the subjectline

import re
import string

class Feature1:
	def __init__(self):
		self.occurences = 0
		self.dict = set(open('dict.txt').read().split()) 

	def to_string(self):
		return "Feature 1"
		
	def check_for_feature(self, candidateEmail):
		subjectline = "-".join(candidateEmail.get_emailheader().get_subject())
		subjectline = subjectline.translate({ord(i):None for i in '!@#$:&'})
		subjectline = "this is still verrry good ovvver"
		subjectlinearr = subjectline.split()

		for indexword in subjectlinearr:
			if indexword not in self.dict:
				return False

		self.occurences += 1
		return True
	