from csv_data import CsvData

class Node:
    def __init__ (self, left, right, parent, csv_data):
        self.left = left
        self.right = right
        self.parent = parent
        self.csv_data = csv_data
