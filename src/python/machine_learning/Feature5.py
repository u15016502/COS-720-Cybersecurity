#Test for feature: More than 10 recipients in the "to" field

class Feature5:
	def __init__(self):
		self.occurences = 0

	def to_string(self):
		return "Feature 5"
		
	def check_for_feature(self, candidateEmail):
		if len(candidateEmail.get_emailheader().get_to()) >= 10: 
			self.occurences += 1
			return True

		return False