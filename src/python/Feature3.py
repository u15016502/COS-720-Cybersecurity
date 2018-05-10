#Test for feature: Checks for matches between the to and from field

class Feature3:
	def __init__(self):
		self.occurences = 0

	def to_string(self):
		return "Feature 3"
		
	def check_for_feature(self, candidateEmail):

		to_arr = candidateEmail.get_emailheader().get_to()


		from_string = "-".join(candidateEmail.get_emailheader().get_from())

		if from_string.find("@") != -1:
			for address in to_arr:
				if address.find("@") != -1:
					address = address[address.find("@")+1:]
					if from_string == address:
						return False

		
			self.occurences += 1
			return True
		else:
			return False