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
from Calculation import Calculation
from TreeNode import TreeNode

class TreeBuilder:

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

		self.features = []

		self.features.append(self.f1)
		self.features.append(self.f2)
		self.features.append(self.f3)
		self.features.append(self.f4)
		self.features.append(self.f5)
		self.features.append(self.f6)
		self.features.append(self.f7)
		self.features.append(self.f8)
		self.features.append(self.f9)
		self.features.append(self.f10)
		self.features.append(self.f11)

		self.calculator = Calculation()

	def induce_tree(self, current_node, subset):
		information_gain_per_feature = []
		entropy_for_set = self.calculator.get_total_entropy(subset)
		index_of_largest_info_gain = 0
		largest_info_gain = 0
		subset_negative_for_feature = []
		subset_positive_for_feature = []

		if entropy_for_set == 0:
			current_node.is_leaf = True
			current_node.candidate_emails = subset
			if len(subset) != 0:
				current_node.classification = subset[0].classification
				return

		for feature in self.features:
			information_gain_per_feature.append(self.calculator.get_info_gain_for_feature(subset, feature, entropy_for_set))

		for x in range(0,11):
			if information_gain_per_feature[x] > largest_info_gain:
				largest_info_gain = information_gain_per_feature[x]
				index_of_largest_info_gain = x

		current_node.feature = self.features[index_of_largest_info_gain]

		new_left_child = TreeNode()
		new_right_child = TreeNode()

		current_node.left_child = new_left_child
		current_node.right_child = new_right_child

		for candidate_email in subset:
			if current_node.feature.check_for_feature(candidate_email) == True:
				subset_positive_for_feature.append(candidate_email)
			else:
				subset_negative_for_feature.append(candidate_email)

		self.induce_tree(current_node.left_child,subset_negative_for_feature)
		self.induce_tree(current_node.right_child,subset_positive_for_feature)




