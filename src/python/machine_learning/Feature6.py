#Test for feature: More than 10 recipients in the "cc" or "bcc" field

class Feature6:
	def __init__(self):
		self.occurences = 0

	def to_string(self):
		return "Feature 6"
		
	def check_for_feature(self, candidateEmail):

		if len(candidateEmail.get_emailheader().get_cc()) >= 10:
			self.occurences += 1
			return True

		if len(candidateEmail.get_emailheader().get_bcc()) >= 10:
			self.occurences += 1
			return True


		return False