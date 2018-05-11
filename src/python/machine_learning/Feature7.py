#Test for feature: Check for missing or malformed "messageID"

class Feature7:
	def __init__(self):
		self.occurences = 0

	def to_string(self):
		return "Feature 7"
		
	def check_for_feature(self, candidateEmail):

		if "-".join(candidateEmail.get_emailheader().get_messageID()) == "":
			self.occurences += 1
			return True

		if ".JavaMail.evans@thyme" not in "-".join(candidateEmail.get_emailheader().get_messageID()):
			self.occurences += 1
			return True

		return False 