#!/usr/bin/env python3.6

from FileParser import FileParser
from Calculation import Calculation
from XHeader import XHeader
from EmailHeader import EmailHeader
from CandidateEmail import CandidateEmail
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
import json
import sys 


if len(sys.argv) == 2:
	association_rule_size = sys.argv[0]
	support_threshold_single = sys.argv[1]
elif len(sys.argv) == 3:
	association_rule_size = sys.argv[0]
	support_threshold_single = sys.argv[1]
	support_threshold_pair = sys.argv[2]
elif len(sys.argv) == 4:
	association_rule_size = sys.argv[0]
	support_threshold_single = sys.argv[1]
	support_threshold_pair = sys.argv[2]
	support_threshold_triplet = sys.argv[3]
else:
	association_rule_size = 3
	support_threshold_single = 10000
	support_threshold_pair = 10000
	support_threshold_triplet = 10000

file_parser = FileParser("res/headers_clean.dat","res/association_rules.dat")
candidate_emails = file_parser.read_file()

f1 = Feature1()
f2 = Feature2()
f3 = Feature3()
f4 = Feature4()
f5 = Feature5()
f6 = Feature6()
f7 = Feature7()
f8 = Feature8()
f9 = Feature9()
f10 = Feature10()
f11 = Feature11()

#Calculate association rules for single features

calculator = Calculation()
calculator.set_support_threshold(support_threshold_single)

frequency_per_feature = []
features = []
features_within_threshold = []

for x in range(0,11):
	if x == 0:
		features.append(f1)
		frequency_per_feature.append(
		calculator.calculate_frequency(f1,candidate_emails))
	if x == 1:
		features.append(f2)
		frequency_per_feature.append(
		calculator.calculate_frequency(f2,candidate_emails))
	if x == 2:
		features.append(f3)
		frequency_per_feature.append(
		calculator.calculate_frequency(f3,candidate_emails))
	if x == 3:
		features.append(f4)
		frequency_per_feature.append(
		calculator.calculate_frequency(f4,candidate_emails))
	if x == 4:
		features.append(f5)
		frequency_per_feature.append(
		calculator.calculate_frequency(f5,candidate_emails))
	if x == 5:
		features.append(f6)
		frequency_per_feature.append(
		calculator.calculate_frequency(f6,candidate_emails))
	if x == 6:
		features.append(f7)
		frequency_per_feature.append(
		calculator.calculate_frequency(f7,candidate_emails))
	if x == 7:
		features.append(f8)
		frequency_per_feature.append(
		calculator.calculate_frequency(f8,candidate_emails))
	if x == 8:
		features.append(f9)
		frequency_per_feature.append(
		calculator.calculate_frequency(f9,candidate_emails))
	if x == 9:
		features.append(f10)
		frequency_per_feature.append(
		calculator.calculate_frequency(f10,candidate_emails))
	if x == 10:
		features.append(f11)
		frequency_per_feature.append(
		calculator.calculate_frequency(f11,candidate_emails))

for x in range(0,9):
	if calculator.is_over_support_threshold(frequency_per_feature[x]) == True:
		features_within_threshold.append(features[x])

if association_rule_size == 1:
	file_parser.write_file("The single features that are above support threshold:")
	file_parser.write_file("-------------")
	for feature in features_within_threshold:
		file_parser.write_file(feature.to_string())

	sys.exit()

#Calculate association rules for pairs
calculator.set_support_threshold(support_threshold_pair)

feature_pairs = []
frequency_per_feature_pair = []
feature_pairs_within_threshold = []

feature_pairs = calculator.create_feature_pairs(features_within_threshold)

for pair in feature_pairs:
	frequency_per_feature_pair.append(
		calculator.calculate_frequency_pair(pair,candidate_emails))

for x in range(0,len(feature_pairs)):
	if calculator.is_over_support_threshold(frequency_per_feature_pair[x]) == True:
		feature_pairs_within_threshold.append(feature_pairs[x])


if association_rule_size == 2:
	file_parser.write_file("The single features that are above support threshold:")
	file_parser.write_file("-------------")
	for feature in features_within_threshold:
		file_parser.write_file(feature.to_string())

	file_parser.write_file("The feature pairs that are above support threshold:")
	file_parser.write_file("-------------")
	for feature_pair in feature_pairs_within_threshold:
		file_parser.write_file(feature_pair[0].to_string())
		file_parser.write_file(feature_pair[1].to_string())
		file_parser.write_file(" ")
	sys.exit()

#Calculate association rules for triplets
calculator.set_support_threshold(support_threshold_triplet)

feature_triplets = []
frequency_per_feature_triplet = []
feature_triplets_within_threshold = []

feature_triplets = calculator.feature_self_join(feature_pairs_within_threshold)

print(str(feature_triplets))

file_parser.write_file("The single features that are above support threshold:")
file_parser.write_file("\n")
file_parser.write_file("-------------")
file_parser.write_file("\n")
for feature in features_within_threshold:
	file_parser.write_file(feature.to_string())
	file_parser.write_file("\n")
		
file_parser.write_file("\n")
file_parser.write_file("The feature pairs that are above support threshold:")
file_parser.write_file("\n")
file_parser.write_file("-------------")
file_parser.write_file("\n")
for feature_pair in feature_pairs_within_threshold:
	file_parser.write_file(feature_pair[0].to_string())
	file_parser.write_file("\n")
	file_parser.write_file(feature_pair[1].to_string())
	file_parser.write_file("\n")
	file_parser.write_file("\n")
	file_parser.write_file(" ")

file_parser.write_file("The feature triplets that are above support threshold:")
file_parser.write_file("\n")
file_parser.write_file("-------------")
file_parser.write_file("\n")

for feature_triplet in feature_triplets:
	file_parser.write_file(feature_triplet[0].to_string())
	file_parser.write_file("\n")
	file_parser.write_file(feature_triplet[1].to_string())
	file_parser.write_file("\n")
	file_parser.write_file(feature_triplet[2].to_string())
	file_parser.write_file("\n")
	file_parser.write_file("\n")
	file_parser.write_file(" ")

