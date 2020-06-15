from c45 import C45
from csv_data import CsvData
from node import Node
from graphviz import Digraph
from anytree import Node as anyNode, RenderTree
from anytree.exporter import DotExporter
import uuid

import random

class DecisionTree:
    def __init__ (self, index, decision_class):
        self.index = index
        self.root = index
        self.decision_class = decision_class
        self.dot = Digraph(comment='Tree Train')
        self.arrDot = []
        self.count_node = 0

    def generate(self, node):
        lengthAttribute = self.lengthAttributes(node.csv_data.attribute_types)
        self.count_node = self.count_node + 1
        # self.dot.node(node.uuid, node.csv_data.max_attribute + ' >= ' + str(node.csv_data.result_calculate[node.csv_data.max_attribute].median))

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
                    node.uuid = str(uuid.uuid4().fields[-1])[:5]
                    # node.an = anyNode(node.csv_data.max_attribute + ' >= ' + str(node.csv_data.result_calculate[node.csv_data.max_attribute].median), self.index.an)

                    self.index.left = node
                    self.index = self.index.left

                    # self.arrDot.append(self.index.parent.uuid + node.uuid)

                    self.generate(self.index)
                    self.index = self.index.parent
                    node = self.index

                    # if (self.index.parent != None):
                    #     self.index.setAn(anyNode(self.index.csv_data.state_false, self.index.parent.getAn()))
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
                    node.uuid = str(uuid.uuid4().fields[-1])[:5]
                    # node.an = anyNode(node.csv_data.max_attribute + ' >= ' + str(node.csv_data.result_calculate[node.csv_data.max_attribute].median), self.index.an)

                    self.index.right = node
                    self.index = self.index.right

                    # self.arrDot.append(self.index.parent.uuid + node.uuid)

                    self.generate(self.index)
                    self.index = self.index.parent
                    node = self.index

                    # if (self.index.parent != None):
                    #     self.index.setAn(anyNode(self.index.csv_data.state_true, self.index.parent.getAn()))
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

    def generateGraph(self):
        # new = self.arrDot[:len(self.arrDot)//5]
        # print(new)
        # print(len(new))
        # self.dot.edges(new)
        # self.dot.render('./decision-tree.gv', view=True)
        # print(RenderTree(self.index.an))
        if (self.index.left != None):
            self.index = self.index.left
            # if (self.index.csv_data.state_false == None):
            # else:
            self.index.an = anyNode("(" + str(self.index.uuid) + ") " + self.index.csv_data.max_attribute + ' >= ' + str(self.index.csv_data.result_calculate[self.index.csv_data.max_attribute].median), self.index.parent.an)
            # if (self.index.csv_data.state_false == None):
            # elif (self.index.csv_data.state_false != None):
            #     self.index.an = anyNode("(" + str(self.index.uuid) + ") " + self.index.csv_data.state_false, self.index.parent.an)
            # elif (self.index.csv_data.state_true != None):
            #     self.index.an = anyNode("(" + str(self.index.uuid) + ") " + self.index.csv_data.state_true, self.index.parent.an)
            # else:
            #     self.index.an = anyNode("(" + str(self.index.uuid) + ") " + "None", self.index.parent.an)


            self.generateGraph()
            self.index = self.index.parent
                # self.index.an = anyNode("(" + str(self.index.uuid) + ") " + self.index.csv_data.state_false, self.index.parent.an)

        if (self.index.right != None):
            self.index = self.index.right
            self.index.an = anyNode("(" + str(self.index.uuid) + ") "+ self.index.csv_data.max_attribute + ' >= ' + str(self.index.csv_data.result_calculate[self.index.csv_data.max_attribute].median), self.index.parent.an)
            # if (self.index.csv_data.state_true == None):
            # else:
            #     self.index.an = anyNode("(" + str(self.index.uuid) + ") "+ self.index.csv_data.state_true, self.index.parent.an)
            self.generateGraph()
            self.index = self.index.parent
                # self.index.an = anyNode("(" + str(self.index.uuid) + ") " + self.index.csv_data.state_true, self.index.parent.an)
    def copyGenerataGraph(self):
        if (self.index.csv_data.state_false == None and self.index.left != None):
            cek = False
            if (self.index.csv_data.state_false != None):
                cek = True
            self.index = self.index.left
            # if (cek):
            #     self.index.an = anyNode("(" + str(self.index.uuid) + ") " + self.index.csv_data.state_false, self.index.parent.an)
            # else:
            self.index.an = anyNode("(" + str(self.index.uuid) + ") " + self.index.csv_data.max_attribute + ' >= ' + str(self.index.csv_data.result_calculate[self.index.csv_data.max_attribute].median) + " ("+ str(len(self.index.csv_data.rows)) +")", self.index.parent.an)
            self.generateGraph()
            self.index = self.index.parent
        if (self.index.csv_data.state_true == None and self.index.right != None):
            cek = False
            if (self.index.csv_data.state_true != None):
                cek = True
            self.index = self.index.right
            # if (cek):
            #     self.index.an = anyNode("(" + str(self.index.uuid) + ") " + self.index.csv_data.state_true, self.index.parent.an)
            # else:
            self.index.an = anyNode("(" + str(self.index.uuid) + ") " + self.index.csv_data.max_attribute + ' >= ' + str(self.index.csv_data.result_calculate[self.index.csv_data.max_attribute].median) + " ("+ str(len(self.index.csv_data.rows)) +")", self.index.parent.an)
            self.generateGraph()
            self.index = self.index.parent

        # if (self.index.csv_data.state_false != None):
        #     self.index.an = anyNode("(" + str(self.index.uuid) + ") " + self.index.csv_data.state_false, self.index.parent.an)
        # elif (self.index.csv_data.state_true != None):
        #     self.index.an = anyNode("(" + str(self.index.uuid) + ") " + self.index.csv_data.state_true, self.index.parent.an)
        # else:
        #     self.index.an = anyNode("(" + str(self.index.uuid) + ") " + "None", self.index.parent.an)

    def printGraph(self):
        for pre, fill, node in RenderTree(self.index.an):
            print("%s%s" % (pre, node.name))
        DotExporter(self.index.an).to_picture("generate-tree.png")
