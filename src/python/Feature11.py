#Test for feature: Checks if the email was sent at a time of day that falls outside of business hours eg 23:00 - 04:00

class Feature11:
	def __init__(self):
		self.occurences = 0

	def to_string(self):
		return "Feature 11"
		
	def check_for_feature(self, candidateEmail):
		if " 23:" in "-".join(candidateEmail.get_emailheader().get_date()):
			return True

		if " 24:" in "-".join(candidateEmail.get_emailheader().get_date()):
			return True

		if " 00:" in "-".join(candidateEmail.get_emailheader().get_date()):
			return True

		if " 01:" in "-".join(candidateEmail.get_emailheader().get_date()):
			return True

		if " 02:" in "-".join(candidateEmail.get_emailheader().get_date()):
			return True

		if " 03:" in "-".join(candidateEmail.get_emailheader().get_date()):
			return True

		return False