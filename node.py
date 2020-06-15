from csv_data import CsvData
from anytree import Node as anyNode, RenderTree

class Node:
    def __init__ (self, left, right, parent, csv_data):
        self.left = left
        self.right = right
        self.parent = parent
        self.csv_data = csv_data
        self.uuid = None
        self.an = None

    def setAn(self, an):
        self.an = an

    def getAn(self):
        self.an
