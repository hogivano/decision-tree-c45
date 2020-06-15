class TestCase:
    def __init__ (self, tree, data_test):
        self.tree = tree
        self.data_test = data_test
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0
        self.empty_false = 0
        self.empty_true = 0

    def generateConfusedMatrix(self):
        root = self.tree
        # print(root.csv_data.result_calculate[root.csv_data.max_attribute].classifier)
        for data in self.data_test:
            self.depthSearchTree(root, data)

    def depthSearchTree(self, node, row):
        csv_data = node.csv_data
        col_index = csv_data.result_calculate[csv_data.max_attribute].classifier_col_index
        if (row[col_index] < csv_data.result_calculate[csv_data.max_attribute].median):
            # if(node.left != None):
            if (csv_data.state_false == None):
                if(node.left != None):
                    self.depthSearchTree(node.left, row)
                else:
                    self.empty_false = self.empty_false +1
                # self.depthSearchTree(node.left, row)
            else:
                if(csv_data.state_false == "yes" and (row[len(row) - 1] == 1.0 or row[len(row) - 1] == 1)):
                    self.tp = self.tp + 1
                elif(csv_data.state_false == "no" and (row[len(row) - 1] == 0.0 or row[len(row) - 1] == 0)):
                    self.fn = self.fn + 1
                elif(csv_data.state_false == "no" and (row[len(row) - 1] == 1.0 or row[len(row) - 1] == 1)):
                    self.fp = self.fp + 1
                elif(csv_data.state_false == "yes" and (row[len(row) - 1] == 0.0 or row[len(row) - 1] == 0)):
                    self.tn = self.tn + 1
        else:
            # if(node.right != None):
            if (csv_data.state_true == None):
                if(node.right != None):
                    self.depthSearchTree(node.right, row)
                else:
                    self.empty_true = self.empty_true + 1
                # self.depthSearchTree(node.right, row)
            else:
                if(csv_data.state_true == "yes" and (row[len(row) - 1] == 1.0 or row[len(row) - 1] == 1)):
                    self.tp = self.tp + 1
                elif(csv_data.state_true == "no" and (row[len(row) - 1] == 0.0 or row[len(row) - 1] == 0)):
                    self.fn = self.fn + 1
                elif(csv_data.state_true == "no" and (row[len(row) - 1] == 1.0 or row[len(row) - 1] == 1)):
                    self.fp = self.fp + 1
                elif(csv_data.state_true == "yes" and (row[len(row) - 1] == 0.0 or row[len(row) - 1] == 0)):
                    self.tn = self.tn + 1
