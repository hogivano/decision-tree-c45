import math

class C45:
    def __init__ (self, csv_data, classifier, entropy_s):
        self.csv_data = csv_data
        self.entropy_s = entropy_s
        self.median = 0
        self.classifier_col_index = -1
        self.classifier = classifier
        self.comparator = []
        self.arr_plus_minus = []
        self.total_plus_minus = 0
        self.arr_entropy = []
        self.entropy_total = 0
        self.gain = 0
        self.split_info = 0
        self.gain_ratio = 0
        self.rows_true = []
        self.rows_false = []

    def calculate(self):
        self.checkEntropyS()
        self.classifier_col_index = self.getClassifierColIndex()
        self.median = self.searchMedian()
        self.entropy_total = self.entropyTotal()
        self.gain = self.gainTotal()
        self.split_info = self.splitInfo()
        self.gain_ratio = self.gainRatio()
        # calculate entropy

    def getState(self, rows):
        yes = 0
        no = 0
        for row in rows:
            if (row[self.csv_data.decision_col_index] == 1 or row[self.csv_data.decision_col_index] == 1.0):
                yes = yes + 1
            elif (row[self.csv_data.decision_col_index] == 0 or row[self.csv_data.decision_col_index] == 0.0):
                no = no + 1
        if yes == 0 and no != 0:
            return "no"
        elif no == 0 and yes != 0:
            return "yes"
        else:
            print("(c45) yes : ", yes, " ", "no : ", no, " ", len(rows))
            return None

    def getStateCount(self, rows):
        yes = 0
        no = 0
        for row in rows:
            for i in range(len(row)):
                if (row[self.csv_data.decision_col_index] == 1 or row[self.csv_data.decision_col_index] == 1.0):
                    yes+=1
                elif (row[self.csv_data.decision_col_index] == 0 or row[self.csv_data.decision_col_index] == 0.0):
                    no+=1
        if yes == 0 and no != 0:
            return no
        elif no == 0 and yes != 0:
            return yes
        else:
            return 0

    def searchMedian(self):
        rows = self.csv_data.rows

        arr_temp = []
        for i in range(len(rows)):
            arr_temp.append(rows[i][self.classifier_col_index])
        arr_temp.sort()
        print(arr_temp)
        if (len(arr_temp) % 2 == 2):
            center = int(len(arr_temp)/2)
            median = (arr_temp(center) + arr_temp(center-1))/2
        else:
            median = arr_temp[int(len(arr_temp)/2)]

        # if (len(arr_temp) == 0):
        #     median = 0
        # else:
        #     median = arr_temp[int(len(arr_temp)/2)]

        return median

    def getClassifierColIndex(self):
        for i in range(len(self.csv_data.attributes)):
            if self.classifier == self.csv_data.attributes[i]:
                return i
                break

    def checkEntropyS(self):
        if self.entropy_s == 0:
            result = self.getPlusMinus(self.csv_data.decision_class, True)
            self.entropy_s = self.entropy(result[0], result[1])

    def getPlusMinus(self, classifier, state):
        plus = 0
        minus = 0
        if self.csv_data.decision_class == classifier:
            rows = self.csv_data.rows
            for i in range(len(rows)):
                    if (rows[i][self.csv_data.decision_col_index] == 1 or rows[i][self.csv_data.decision_col_index] == 1.0):
                        plus+=1
                    else:
                        minus+=1
            return [plus, minus]
        else:
            decision_col_index = self.csv_data.decision_col_index
            for row in self.csv_data.rows:
                if row[decision_col_index] == 1 and (row[self.classifier_col_index] >= self.median) == state:
                    plus+=1
                    if state == True:
                        self.rows_true.append(row)
                    elif state == False:
                        self.rows_false.append(row)
                elif row[decision_col_index] == 0 and (row[self.classifier_col_index] >= self.median) == state:
                    minus+=1
                    if state == True:
                        self.rows_true.append(row)
                    elif state == False:
                        self.rows_false.append(row)
            return [plus, minus]

    def entropy(self, plus, minus):
        total = plus+minus
        if (plus == 0):
            p = 0
        else:
            p = plus/total

        if (minus == 0):
            m = 0
        else:
            m = minus/total

        print("entropy ", p, m)
        if (p == 0.0):
            left = 0
        else:
            left = (-p*math.log(p, 2))

        if (m == 0.0):
            right = 0
        else:
            right = (-m*math.log(m, 2))
        return left + right

    def entropyTotal(self):
        plus_minus_down = self.getPlusMinus(self.classifier, False)
        plus_minus_up =  self.getPlusMinus(self.classifier, True)

        self.arr_plus_minus = [plus_minus_down, plus_minus_up]

        total_down = plus_minus_down[0] + plus_minus_down[1]
        total_up = plus_minus_up[0] + plus_minus_up[1]

        entropy_down =  self.entropy(plus_minus_down[0], plus_minus_down[1])
        entropy_up =  self.entropy(plus_minus_up[0], plus_minus_up[1])

        self.arr_entropy = [entropy_down, entropy_up]

        total = total_down + total_up

        self.total_plus_minus = total

        if (total_down == 0 or total == 0):
            down = 0
        else:
            down = total_down/total

        if (total_up == 0 or total == 0):
            up = 0
        else:
            up = total_up/total

        return down * entropy_down + up * entropy_up

    def splitInfo(self):
        result = 0
        for arr in self.arr_plus_minus:
            nominator = 0
            for value in arr:
                nominator+=value
            if (nominator == 0):
                total = 0
                mathLog = 0
            else:
                total = nominator/self.total_plus_minus
                mathLog = math.log(total, 2)

            result = result + (-1 * total) * mathLog
        return result

    def gainRatio(self):
        if (self.gain == 0 or self.split_info == 0):
            return 0
        else:
            return self.gain / self.split_info

    def gainTotal(self):
        return self.entropy_s - self.entropy_total
