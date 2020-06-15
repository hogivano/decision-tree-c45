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

# print("lenght data test ",len(data_test))

# print("tp ", test_case.tp)
# print("tn ", test_case.tn)
# print("fp ", test_case.fp)
# print("fn ", test_case.fn)

total = test_case.tp + test_case.tn + test_case.fp + test_case.fn

# print("correctly ", test_case.tp+test_case.fn)
# print("incorrectly ", test_case.tn+test_case.fp)

# print("empty false ", test_case.empty_false)
# print("empty true ", test_case.empty_true)
print("Split Test (%) : ", percent)
print("\n====== Accuracy ======")
print("correcly percent (%) ", (test_case.tp+test_case.fn) / total * 100)
print("incorrectly percent (%) ", (test_case.tn+test_case.fp) / total * 100)

print("\n==== Confusion Matrix ====")
print("a : b")
print(test_case.fn, " : ", test_case.tn, " | a = no")
print(test_case.fp, " : ", test_case.tp, " | b = yes")

# print accuracy
yesDict = dict()
noDict = dict()

yesDict["tpRate"] = test_case.fp / (test_case.fp + test_case.tn)
yesDict["fpRate"] = test_case.tp / (test_case.tp + test_case.fn)

noDict["tpRate"] = test_case.fn / (test_case.fn + test_case.tp)
noDict["fpRate"] = test_case.tn / (test_case.tn + test_case.fp)

yesDict["recall"] = yesDict["tpRate"]
noDict["recall"] = noDict["tpRate"]

yesDict["precision"] = test_case.tp / (test_case.tp + test_case.fp)
noDict["precision"] = test_case.fn / (test_case.fn + test_case.tn)

yesDict["f-measure"] = 2 * (yesDict["precision"] * yesDict["recall"] / (yesDict["precision"] + yesDict["recall"]))
noDict["f-measure"] = 2 * (noDict["precision"] * noDict["recall"] / (noDict["precision"] + noDict["recall"]))

print("\n====== Detail accuracy by class =====")
print("Tp Rate : Fp Rate : Precision : Recall : F-Measure")
print(noDict["tpRate"], " : ", noDict["fpRate"], " : ", noDict["precision"], " : ", noDict["tpRate"], " : ", noDict["f-measure"], " -no")
print(yesDict["tpRate"], " : ", yesDict["fpRate"], " : ", yesDict["precision"], " : ", yesDict["tpRate"], " : ", yesDict["f-measure"], " -yes")
# print(dataset.attribute_types, " ", dataset.rows)
