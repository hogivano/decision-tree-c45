from c45 import C45
from sklearn.model_selection import train_test_split
import pandas as pd

class CsvData:
    def __init__ (self, decision_class):
        self.path = None
        self.rows = []
        self.attributes = []
        self.attribute_types = []
        self.decision_col_index = None
        self.decision_class = decision_class
        self.result_calculate = dict()
        self.max_gain = 0
        self.max_attribute = None
        self.state_true = None
        self.state_false = None

    def splitData(self, percent):
        df = pd.read_csv('data.csv')
        head = list(df.columns)
        X_train, X_test, Y_train, Y_test = train_test_split(df[head], df['quality'], test_size=int(percent)/100, random_state=0)
        rows_train = []

        self.rows = X_train.values.tolist()
        self.attributes = head
        return X_test.values.tolist()

    def initialize(self):
        # read csv file
        f = open(self.path)
        original_file = f.read()
        rowsplit_data = original_file.splitlines()
        if (len(self.rows) == 0):
            self.rows = [rows.split(',') for rows in rowsplit_data]
            self.attributes = self.rows.pop(0)

        self.setAttributeTypesAndDecisionColIndex()
        self.preprocessingData()

    def calculate(self):
        max = 0
        max_attribute = None
        for i in range(len(self.attributes)):
            if (self.attribute_types[i]):
                c45 = C45(self, self.attributes[i], 0)
                c45.calculate()
                if (max <= c45.gain_ratio):
                    max_attribute = self.attributes[i]
                    max = c45.gain_ratio

                self.result_calculate[self.attributes[i]] = c45
                print("entropy_s : ", c45.entropy_s)
                print("gain ratio : ", c45.gain_ratio)
                print("median : ",  c45.median)

        self.max_gain = max
        self.max_attribute = max_attribute

        c45 = self.result_calculate[max_attribute]
        self.state_true = c45.getState(c45.rows_true)
        self.state_false = c45.getState(c45.rows_false)

        print("true : ", self.state_true)
        print("false : ", self.state_false)
        print("max gain : ", max, " ", max_attribute)

    def setPath(self, path):
        self.path = path

    def setRows(self, rows):
        self.rows = rows

    def setAttributes(self, attributes):
        self.attributes = attributes

    def setAttributeTypes(self, attribute_types):
        for i in range(len(attribute_types)):
            self.attribute_types.append(attribute_types[i])

    def setDecisionColIndex(self, decision_col_index):
        self.decision_col_index = decision_col_index

    def setAttributeTypeFromClassifier(self, classifier):
        for i in range(len(self.attributes)):
            attr = self.attributes[i]
            if (attr == classifier):
                self.attribute_types[i] = False

    def setAttributeTypesAndDecisionColIndex(self):
        for i in range(len(self.attributes)):
            attr = self.attributes[i]
            if (attr == self.decision_class):
                self.decision_col_index = i
                self.attribute_types.append(False)
            else:
                self.attribute_types.append(True)

    def preprocessingData(self):
        for i in range(len(self.rows)):
            for j in range(len(self.rows[i])):
                self.rows[i][j] = float(self.rows[i][j])
