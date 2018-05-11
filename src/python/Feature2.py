#Test for feature: keywords associated with phishing appear in the subjectline 

class Feature2:

	def __init__(self):
		self.occurences = 0
		self.dict = set(open('phishing-words-dict.txt').read().split('\n')) 

	def to_string(self):
		return "Feature 2"
		
	def check_for_feature(self, candidateEmail):
		subjectline = "-".join(candidateEmail.get_emailheader().get_subject())
		subjectline = subjectline.translate({ord(i):None for i in '!@#$:&'})

		if any([word in subjectline for word in self.dict]):
			return True

		self.occurences += 1
		return False