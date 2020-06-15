from c45 import C45
from csv_data import CsvData
from node import Node
from graphviz import Digraph

import random

class DecisionTree:
    def __init__ (self, index, decision_class):
        self.index = index
        self.root = index
        self.decision_class = decision_class
        self.dot = Digraph(comment='Tree Train')
        self.count_node = 0

    def generate(self, node):
        lengthAttribute = self.lengthAttributes(node.csv_data.attribute_types)
        self.count_node = self.count_node + 1
        if self.index.left == None:
            if (node.csv_data.state_false == None and lengthAttribute > 1):
                if (len(node.csv_data.result_calculate[node.csv_data.max_attribute].rows_false) > 1):
                    csv_data = CsvData(self.decision_class)
                    csv_data.setRows(node.csv_data.result_calculate[node.csv_data.max_attribute].rows_false)
                    csv_data.setAttributes(node.csv_data.attributes)
                    csv_data.setDecisionColIndex(node.csv_data.decision_col_index)
                    csv_data.setAttributeTypes(node.csv_data.attribute_types)
                    csv_data.setAttributeTypeFromClassifier(node.csv_data.max_attribute)
                    csv_data.calculate()

                    print("Parent Node : ", node.csv_data.max_attribute)
                    print("====================================\n")
                    # print("lenght attr type left : ", node.csv_data.attribute_types)

                    node = Node(None, None, self.index, csv_data)
                    self.index.left = node
                    self.index = self.index.left

                    self.generate(self.index)
                    self.index = self.index.parent
                    node = self.index
                    # if (node.csv_data.state_false == None):
                    # else:
                    #     self.index.left = node
                    #     self.index = self.index.left
                else:
                    if (len(node.csv_data.result_calculate[node.csv_data.max_attribute].rows_false) == 1):
                        if (node.csv_data.result_calculate[node.csv_data.max_attribute].rows_false[0][node.csv_data.decision_col_index] == 1):
                            self.index.csv_data.state_false = "yes"
                        else:
                            self.index.csv_data.state_false = "no"
                    else:
                        self.index.csv_data.state_false = "no"
                    self.index.left = None
        if self.index.right == None:
            if (node.csv_data.state_true == None and lengthAttribute > 1):
                if (len(node.csv_data.result_calculate[node.csv_data.max_attribute].rows_true) > 1):
                    # generate new rows
                    csv_data = CsvData(self.decision_class)
                    csv_data.setRows(node.csv_data.result_calculate[node.csv_data.max_attribute].rows_true)
                    csv_data.setAttributes(node.csv_data.attributes)
                    csv_data.setDecisionColIndex(node.csv_data.decision_col_index)
                    csv_data.setAttributeTypes(node.csv_data.attribute_types)
                    csv_data.setAttributeTypeFromClassifier(node.csv_data.max_attribute)
                    csv_data.calculate()

                    print("Parent Node : ", node.csv_data.max_attribute)
                    print("====================================\n")
                    # print("lenght attr type right : ", node.csv_data.attribute_types)

                    node = Node(None, None, self.index, csv_data)
                    self.index.right = node
                    self.index = self.index.right

                    self.generate(self.index)
                    self.index = self.index.parent
                    node = self.index
                    # if (node.csv_data.state_true == None):
                    # else:
                    #     self.index.right = node
                    #     self.index = self.index.right
                else:
                    if (len(node.csv_data.result_calculate[node.csv_data.max_attribute].rows_true) == 1):
                        if (node.csv_data.result_calculate[node.csv_data.max_attribute].rows_true[0][node.csv_data.decision_col_index] == 1):
                            self.index.csv_data.state_true = "yes"
                        else:
                            self.index.csv_data.state_true = "no"
                    else:
                        self.index.csv_data.state_true = "no"

                    self.index.right = None
    def lengthAttributes(self, attribute_types):
        count = 0
        for i in attribute_types:
            if i == True:
                count+=1

        return count

    def generateGraph():
        return None
