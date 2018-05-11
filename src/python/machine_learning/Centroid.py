import random
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

class Centroid:

	def __init__(self):
		self.features = []
		self.static_features = []
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
		self.cluster_data = []

		for x in range(0,12):
			self.features.append(random.randint(0,1))
			self.static_features.append(False)

	def to_string(self):
		print_string = ""
		for x in range(0,12):
			print_string += str(x) + ":" + str(self.features[x]) + " "

		return print_string

	def distance_from(self, candidate_email):
		candidate_email_feature_values = []
		distance = 0

		candidate_email_feature_values.append(self.f1.check_for_feature(candidate_email))
		candidate_email_feature_values.append(self.f2.check_for_feature(candidate_email))
		candidate_email_feature_values.append(self.f3.check_for_feature(candidate_email))
		candidate_email_feature_values.append(self.f4.check_for_feature(candidate_email))
		candidate_email_feature_values.append(self.f5.check_for_feature(candidate_email))
		candidate_email_feature_values.append(self.f6.check_for_feature(candidate_email))
		candidate_email_feature_values.append(self.f7.check_for_feature(candidate_email))
		candidate_email_feature_values.append(self.f8.check_for_feature(candidate_email))
		candidate_email_feature_values.append(self.f9.check_for_feature(candidate_email))
		candidate_email_feature_values.append(self.f10.check_for_feature(candidate_email))
		candidate_email_feature_values.append(self.f11.check_for_feature(candidate_email))

		for x in range(0,11):
			if candidate_email_feature_values[x] == True and self.features[x] == 0:
				distance += 1
			elif candidate_email_feature_values[x] == False and self.features[x] == 1:
				distance += 1

		return distance

	def add_to_cluster(self, candidate_email):
		self.cluster_data.append(candidate_email)

	def split_cluster(self):
		new_centroids = []
		centroid1 = Centroid()
		centroid2 = Centroid()

		for x in range(0,12):
			if self.static_features[x] == True:
				centroid1.features.append(self.features[x])
				centroid1.static_features.append(self.static_features[x])
				centroid2.feature.append(self.features[x])
				centroid2.static_features.append(self.static_features[x])

		new_centroids.append(centroid1)
		new_centroids.append(centroid2)

		return new_centroids




