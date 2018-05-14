from TreeNode import TreeNode
from FileParser import FileParser

class DecisionTree:

	def __init__(self):
		self.root_node = TreeNode()
		self.file_parser = FileParser("","res/decision_tree_phishing_emails.dat")
		self.file_parser.write_file("Phishing emails within the training set: \n \n")

	def classify(self,candidate_email):
		return self.traverse(candidate_email, self.root_node, 0)

	def traverse(self,candidate_email, current_node, depth):
		if current_node.is_leaf == True:
			return current_node.classification
		else:
			depth += 1

			if current_node.feature.check_for_feature(candidate_email) == True:
				return self.traverse(candidate_email, current_node.right_child, depth)
			else:
				return self.traverse(candidate_email, current_node.left_child, depth)	

	def traverse_entire_tree(self,depth,current_node,parent_node,direction, print_string):

		for x in range(0,depth):
			print_string += '\t'

		if current_node.is_leaf == True:
			if direction == 'l':
				print_string += "LC of: "
				print_string += parent_node.string_representation()
			else:
				print_string += "RC of: "
				print_string += parent_node.string_representation()

			if current_node.classification == "not-phishing":
				print_string += " - not phishing"
			else:
				print_string += " - phishing"
				for candidate_email in current_node.candidate_emails:
					self.file_parser.write_file(candidate_email.string_representation())
				
				self.file_parser.write_file("\n-----------------------------------\n")

			print_string += " - " + str(len(current_node.candidate_emails))
			print_string += "\n"
			return print_string
		else:
			if parent_node == None:
				print_string += "Root"
				print_string += " - " + current_node.string_representation()
				print_string += "\n"
				depth += 1
				print_string += self.traverse_entire_tree(depth, current_node.left_child, current_node, 'l', "")
				return self.traverse_entire_tree(depth, current_node.right_child, current_node, 'r', print_string)
			else:
				if direction == 'l':
					print_string += "LC of: "
				else:	
					print_string += "RC of: " 

				print_string += parent_node.string_representation()
				print_string += " - " + current_node.string_representation()
				print_string += "\n"
				depth += 1
				print_string += self.traverse_entire_tree(depth, current_node.left_child, current_node, 'l', "")
				return self.traverse_entire_tree(depth, current_node.right_child, current_node, 'r', print_string)