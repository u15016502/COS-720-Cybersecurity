import random
import sys
from Centroid import Centroid
from FileParser import FileParser
from Calculation import Calculation

# This will be an implementation of a variation on the KMeans clustering algorithm

# 1. Randomly select x amount of centroids
# 2. Select random values for each feature within each centroid
# 3. Further split each cluster (amount of clusters == amount of centroids)

number_of_centroids = sys.argv[0]
calculator = Calculation()
file_parser = FileParser("headers_clean.dat","cluster_definitions.dat")

candidate_emails = file_parser.read_file()

centroids = []

for x in number_of_centroids:
	centroid = Centroid()
	centroids.append(centroid)

for candidate_email in candidate_emails:
	minimum_distance = 12
	distance_from_centroid = 12
	centroid_to_be_assigned = None

	candidate_email.classification = calculator.classify(candidate_email)

	for centroid in centroids:
		distance_from_centroid = centroid.distance_from(candidate_email)
		if  distance_from_centroid < minimum_distance:
			centroid_to_be_assigned = centroid
			minimum_distance = distance_from_centroid

	centroid_to_be_assigned.add_to_cluster(candidate_email)

while calculator.check_all_clusters_homogeneity(centroids) == False:
	expanded_centroids = []
	new_centroids = []

	for centroid in centroids:
		if calculator.check_cluster_homogeneity(centroid.cluster_data) == False:
			new_centroids = centroid.split_cluster()

			for candidate_email in centroid.cluster_data:
				minimum_distance = 12
				distance_from_centroid = 12
				centroid_to_be_assigned = None

				for centroid in new_centroids:
					distance_from_centroid = centroid.distance_from(candidate_email)
					if  distance_from_centroid < minimum_distance:
						centroid_to_be_assigned = centroid
						minimum_distance = distance_from_centroid


				centroid_to_be_assigned.add_to_cluster(candidate_email)
			expanded_centroids.append(new_centroids[0])
			expanded_centroids.append(new_centroids[1])
		else:
			expanded_centroids.append(centroid)
		
	centroids = expanded_centroids


print(str(len(expanded_centroids)))

for x in range(1,len(centroids)+1):
	file_parser.write_file("Centroid " + str(x) + "\n")
	if len(centroids[x-1].cluster_data) == 0:
		file_parser.write_file("Class: unclassified \n")
		file_parser.write_file("No applicable emails \n")
	else:
		file_parser.write_file("Class: " + centroids[x-1].cluster_data[0].classification + "\n")
		if centroids[x-1].cluster_data[0].classification == "phishing":
			file_parser_secondary = FileParser("","kmeans_phishing_emails.dat")
			for email in centroids[x-1].cluster_data:
				file_parser_secondary.write_file(email.string_representation())
				file_parser_secondary.write_file("-------------------------\n")

		file_parser.write_file("Number of associated emails: " + str(len(centroids[x-1].cluster_data)) + "\n")
		for y in range(1,13):
			feature_string = "Feature " + str(y) + ": " +  str(centroids[x-1].features[y-1]) + "\n"
			file_parser.write_file(feature_string)
		file_parser.write_file("---------- \n")