import math
from Feature1 import Feature1
from Feature2 import Feature2
from Feature3 import Feature3
from Feature4 import Feature4
from Feature5 import Feature5
from Feature6 import Feature6
from Feature7 import Feature7
from Feature8 import Feature8
from Feature9 import Feature9
from Feature10 import Feature10
from Feature11 import Feature11
from CandidateEmail import CandidateEmail
from EmailHeader import EmailHeader

class Calculation:

	def __init__(self):
		self.f1 = Feature1()
		self.f2 = Feature2()
		self.f3 = Feature3()
		self.f4 = Feature4()
		self.f5 = Feature5()
		self.f6 = Feature6()
		self.f7 = Feature7()
		self.f8 = Feature8()
		self.f9 = Feature9()
		self.f10 = Feature10()
		self.f11 = Feature11()
		self.support_threshold = 20000

	# Apriori algorithm 
	def set_support_threshold(self, support_threshold):
		self.support_threshold = support_threshold

	def calculate_frequency(self, phishing_feature, candidate_emails):
		frequency = 0
		for candidate_email in candidate_emails:
			if phishing_feature.check_for_feature(candidate_email) == True:
				frequency += 1

		return frequency

	def is_over_support_threshold(self, frequency):
		if frequency >= self.support_threshold:
			return True
		else:
			return False

	def check_if_contains_triplet(self,triplet,feature_triplets):
		for ftriplet in feature_triplets:
			if triplet[0] == ftriplet[0]:
				if triplet[1] == ftriplet[1] and triplet[2] == ftriplet[2]:
					return True
				if triplet[1] == ftriplet[2] and triplet[2] == ftriplet[1]:
					return True

		return False


	def check_if_contains_pair(self,pair,feature_pairs):

		for fpair in feature_pairs:
			if pair[0] == fpair[1] and pair[1] == fpair[0]:
				return True
			if pair[0] == fpair[0] and pair[1] == fpair[1]:
				return True

		return False

	
	def remove_duplicate_triplets(self,feature_triplets):
		duplicate_free_feature_triplets = []
		flag = False

		for ftriplet in feature_triplets:
			if self.check_if_contains_triplet(ftriplet, duplicate_free_feature_triplets) == False:
				duplicate_free_feature_triplets.append(ftriplet)

		return duplicate_free_feature_triplets

	def remove_duplicate_pairs(self,feature_pairs):
		duplicate_free_feature_pairs = []
		flag = False

		for fpair in feature_pairs:
			if self.check_if_contains_pair(fpair, duplicate_free_feature_pairs) == False:
				duplicate_free_feature_pairs.append(fpair)

		return duplicate_free_feature_pairs

	def create_feature_pairs(self, features):
		feature_pair = []
		temp_feature_pair = []

		for feature1 in features:
			for feature2 in features:
				if feature1 != feature2:
					temp_feature_pair = []
					temp_feature_pair.append(feature1)
					temp_feature_pair.append(feature2)
					feature_pair.append(temp_feature_pair)


		return self.remove_duplicate_pairs(feature_pair)


	def calculate_frequency_pair(self, feature_pair, candidate_emails):

		occurences = 0

		for candidate_email in candidate_emails:
			if feature_pair[0].check_for_feature(candidate_email) == True:
				if feature_pair[1].check_for_feature(candidate_email) == True:
					occurences += 1

		return occurences


	def feature_self_join(self, feature_pairs):
		feature_triplets = []
		triplet = []

		for fpair1 in feature_pairs:
			for fpair2 in feature_pairs:
				if fpair1[0] == fpair2[0] and fpair1[1] != fpair2[1]:
					triplet = []
					triplet.append(fpair1[0])
					triplet.append(fpair1[1])
					triplet.append(fpair2[1])
					feature_triplets.append(triplet)
				if fpair1[1] == fpair2[1] and fpair1[0] != fpair2[0]:
					triplet = []
					triplet.append(fpair1[1])
					triplet.append(fpair1[0])
					triplet.append(fpair2[0])
					feature_triplets.append(triplet)
				if fpair1[0] == fpair2[1] and fpair1[1] != fpair2[0]:
					triplet = []
					triplet.append(fpair1[0])
					triplet.append(fpair1[1])
					triplet.append(fpair2[0])
					feature_triplets.append(triplet)
				if fpair1[1] == fpair2[0] and fpair1[0] != fpair2[1]:
					triplet = []
					triplet.append(fpair1[1])
					triplet.append(fpair1[0])
					triplet.append(fpair2[1])
					feature_triplets.append(triplet)



		return self.remove_duplicate_triplets(feature_triplets)

	# Decision tree algorithm

	def classify(self,candidate_email):
		counter = 0

		if self.f1.check_for_feature(candidate_email) == True:
			counter += 1
		if self.f2.check_for_feature(candidate_email) == True:
			counter += 1
		if self.f3.check_for_feature(candidate_email) == True:
			counter += 1
		if self.f4.check_for_feature(candidate_email) == True:
			counter += 1
		if self.f5.check_for_feature(candidate_email) == True:
			counter += 1
		if self.f6.check_for_feature(candidate_email) == True:
			counter += 1
		if self.f7.check_for_feature(candidate_email) == True:
			counter += 1
		if self.f8.check_for_feature(candidate_email) == True:
			counter += 1
		if self.f9.check_for_feature(candidate_email) == True:
			counter += 1
		if self.f10.check_for_feature(candidate_email) == True:
			counter += 1
		if self.f11.check_for_feature(candidate_email) == True:
			counter += 1

		if counter >= 5:
			return "phishing"
		else:
			return "not-phishing"

	def get_total_entropy(self,candidate_email_set):
		total_size = len(candidate_email_set)
		total_phishing_emails = 0
		total_not_phishing_emails = 0
		entropy = 0

		for candidate_email in candidate_email_set:
			if candidate_email.classification == "phishing":
				total_phishing_emails += 1
			else:
				total_not_phishing_emails += 1

		if total_not_phishing_emails == 0 or total_phishing_emails == 0:
			return 0
		else:
			entropy = -((total_not_phishing_emails/total_size)*(math.log(total_not_phishing_emails/total_size)/math.log(2)))-((total_phishing_emails/total_size)*(math.log(total_phishing_emails/total_size)/math.log(2)))

		return entropy


	def get_info_gain_for_feature(self,candidate_email_set, feature, entropy_for_set):
		total_number_without_feature = 0
		total_number_with_feature = 0

		total_number_without_feature_phishing = 0
		total_number_with_feature_phishing = 0

		total_number_without_feature_not_phishing = 0
		total_number_with_feature_not_phishing = 0

		entropy_with_feature = 0
		entropy_without_feature = 0

		information_gain = 0

		for candidate_email in candidate_email_set:
			if feature.check_for_feature(candidate_email) == True:
				total_number_with_feature += 1
				if candidate_email.classification == "phishing":
					total_number_with_feature_phishing += 1
				else:
					total_number_with_feature_not_phishing += 1
			else:
				total_number_without_feature += 1
				if candidate_email.classification == "phishing":
					total_number_without_feature_phishing += 1
				else:
					total_number_without_feature_not_phishing += 1

		if total_number_with_feature == 0:
			entropy_with_feature = 0
		else:
			if total_number_with_feature_phishing == 0:
				entropy_with_feature = -(total_number_with_feature_not_phishing/total_number_with_feature)*(math.log(total_number_with_feature_not_phishing/total_number_with_feature)/math.log(2))
			elif total_number_with_feature_not_phishing == 0:
				entropy_with_feature = -(total_number_with_feature_phishing/total_number_with_feature)*(math.log(total_number_with_feature_phishing/total_number_with_feature)/math.log(2))
			else:
				entropy_with_feature = -(total_number_with_feature_not_phishing/total_number_with_feature)*(math.log(total_number_with_feature_not_phishing/total_number_with_feature)/math.log(2))-(total_number_with_feature_phishing/total_number_with_feature)*(math.log(total_number_with_feature_phishing/total_number_with_feature)/math.log(2))

		if total_number_without_feature == 0:
			entropy_without_feature = 0
		else:
			if total_number_without_feature_phishing == 0:
				entropy_without_feature = -(total_number_without_feature_not_phishing/total_number_without_feature)*(math.log(total_number_without_feature_not_phishing/total_number_without_feature)/math.log(2))
			elif total_number_without_feature_not_phishing == 0:
				entropy_without_feature = -(total_number_without_feature_phishing/total_number_without_feature)*(math.log(total_number_without_feature_phishing/total_number_without_feature)/math.log(2))
			else:
				entropy_without_feature = -(total_number_without_feature_not_phishing/total_number_without_feature)*(math.log(total_number_without_feature_not_phishing/total_number_without_feature)/math.log(2))-(total_number_without_feature_phishing/total_number_without_feature)*(math.log(total_number_without_feature_phishing/total_number_without_feature)/math.log(2))

		information_gain = entropy_for_set - ((total_number_with_feature/len(candidate_email_set))*entropy_with_feature) - ((total_number_without_feature/len(candidate_email_set))*entropy_without_feature)

		return information_gain


	# Kmeans algorithm
	def check_cluster_homogeneity(self, cluster):
		isphishing_counter = 0
		isnotphishing_counter = 0

		for candidate_email in cluster:
			if candidate_email.classification == "phishing":
				isphishing_counter += 1
			else:
				isnotphishing_counter += 1


		if isnotphishing_counter == 0 or isphishing_counter == 0:
			return True
		else:
			return False

	def check_all_clusters_homogeneity(self, clusters):
		for cluster in clusters:
			if self.check_cluster_homogeneity(cluster.cluster_data) == False:
				return False

		return True	