#!/usr/bin/env python3.6

from DecisionTree import DecisionTree
from FileParser import FileParser
from TreeBuilder import TreeBuilder
from TreeNode import TreeNode
from Calculation import Calculation
import random

file_parser = FileParser("res/headers_clean.dat","res/decision_tree.dat")
calculator = Calculation()
all_emails = file_parser.read_file()

phishing_emails = []
nonphishing_emails = []
training_set = []
classification_set = []

coinflip = 0

for email in all_emails:
	email.classification = calculator.classify(email)
	if email.classification == "phishing":
		phishing_emails.append(email)
	else:	
		nonphishing_emails.append(email)

for email in nonphishing_emails:
	coinflip = random.randint(0,1)
	if coinflip == 1:
		training_set.append(email)
	else:
		classification_set.append(email)

for email in phishing_emails:
	coinflip = random.randint(0,1)
	if coinflip == 1:
		training_set.append(email)
	else:
		classification_set.append(email)


decision_tree = DecisionTree()
tree_builder = TreeBuilder()
tree_node = TreeNode()

tree_builder.induce_tree(decision_tree.root_node, training_set)

file_parser.write_file(decision_tree.traverse_entire_tree(0, decision_tree.root_node,None,'x',""))

file_parser.write_file("Phishing emails within the classification set: \n \n")
for email in classification_set:
	email.classification = decision_tree.classify(email)
	if email.classification == "phishing":
		file_parser.write_file(email.string_representation())

