#Test for feature: Matches between addresses in the "to" field

class Feature8:
	def __init__(self):
		self.occurences = 0

	def to_string(self):
		return "Feature 8"
		
	def check_for_feature(self, candidateEmail):

		address_arr = candidateEmail.get_emailheader().get_to()

		if len(address_arr) <= 1:
			return False

		for address1 in address_arr:
			if address1.find("@") != -1:
				for address2 in address_arr:
					if address2.find("@") != -1:
						address1 = address1[address1.find("@")+1:] 
						address2 = address2[address2.find("@")+1:] 
						if address1 == address2:
							return False
		return True