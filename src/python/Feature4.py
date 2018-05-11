#Test for feature: Checks if subjectline contains a generic salutation

class Feature4:
	def __init__(self):
		self.occurences = 0
		self.dict = set(open('generic-salutation-dict.txt').read().split('\n')) 

	def to_string(self):
		return "Feature 4"
		
	def check_for_feature(self, candidateEmail):
		subjectline = "-".join(candidateEmail.get_emailheader().get_subject())
		subjectline = subjectline.translate({ord(i):None for i in '!@#$:&'})

		if any([word in subjectline for word in self.dict]):
			return True


		self.occurences += 1
		return False