#Test for feature: Checks if the "to" field is missing

class Feature10:
	def __init__(self):
		self.occurences = 0

	def to_string(self):
		return "Feature 10"
		
	def check_for_feature(self, candidateEmail):
		if len(candidateEmail.get_emailheader().get_to()) == 0:
			self.occurences += 1
			return True

		return False