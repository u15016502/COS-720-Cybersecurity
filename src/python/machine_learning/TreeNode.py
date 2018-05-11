class TreeNode:

	def __init__(self):
		self.feature = None
		self.left_child = None 
		self.right_child = None
		self.is_leaf = False
		self.classification = "phishing"
		self.candidate_emails = []

	def string_representation(self):
		if "Feature1" in str(self.feature):
			return "Feature 1"
		elif "Feature2" in str(self.feature):
			return "Feature 2"
		elif "Feature3" in str(self.feature):
			return "Feature 3"
		elif "Feature4" in str(self.feature):
			return "Feature 4"
		elif "Feature5" in str(self.feature):
			return "Feature 5"
		elif "Feature6" in str(self.feature):
			return "Feature 6"
		elif "Feature7" in str(self.feature):
			return "Feature 7"
		elif "Feature8" in str(self.feature):
			return "Feature 8"
		elif "Feature9" in str(self.feature):
			return "Feature 9"
		elif "Feature10" in str(self.feature):
			return "Feature 10"
		elif "Feature11" in str(self.feature):
			return "Feature 11"