from csv_data import CsvData
from node import Node
from test_case import TestCase
from decision_tree import DecisionTree

# set data first time
percent = input("Split percent(%) : ")

dataset = CsvData("quality")
dataset.setPath("data.csv")
data_test = dataset.splitData(percent)
dataset.initialize()
dataset.calculate()

root = Node(None, None, None, dataset)
generate = DecisionTree(root, "quality")
generate.generate(root)
root = generate.index

test_case = TestCase(root, data_test)
test_case.generateConfusedMatrix()

print("lenght data test ",len(data_test))

print("tt ", test_case.tt)
print("tf ", test_case.tf)
print("ft ", test_case.ft)
print("ff ", test_case.ff)

total = test_case.tt + test_case.tf + test_case.ft + test_case.ff

print("correctly ", test_case.tt+test_case.ff)
print("incorrectly ", test_case.tf+test_case.ft)

print("empty false ", test_case.empty_false)
print("empty true ", test_case.empty_true)

print("correcly percent (%) ", (test_case.tt+test_case.ff) / total * 100)
print("incorrectly percent (%) ", (test_case.tf+test_case.ft) / total * 100)
# print(dataset.attribute_types, " ", dataset.rows)
