import csv


def getNumHouseholds(num,fileB):
    with open(fileB,'r') as csvFile:
        reader = csv.reader(csvFile)
        
        num_households = len(set(list(reader)[0]))-1

    return num_households

def getTotalBuyList(num,fileB):
    with open(fileB, 'r') as csvFile:
        reader = csv.reader(csvFile)
        num_households = getNumHouseholds(num,fileB)
        csvFile.seek(0)
        next(reader)
        next(reader)
        buylist = []
        totalBuylist = []
        for i in range(1,num_households+1):
            for row in reader:
                if row[i] != '':
                    buylist.append(row[0])
            #print(buylist)
            totalBuylist.insert(len(totalBuylist),list(buylist))
            buylist.clear()
            csvFile.seek(0)
            next(reader)
            next(reader)
    return totalBuylist


def cleanUp(buylist):
    temp_list = []
    i = 0
    for house in buylist:
        temp_list = []
        hasA = False
        hasB = False
        hasC = False
        hasD = False
        for item in house:
            if item == ' D ':
                hasD = True
            if item == ' C ':
                hasC = True
            if item == ' B ':
                hasB = True
            if item == ' A ':
                hasA = True
        for item in house:
            if hasD == True and item.count('D')>0:
                temp_item = 'D'
                temp_list.append(temp_item)
            elif hasC == True and item.count('C')>0:
                temp_item = 'C'
                temp_list.append(temp_item)
            elif hasB == True and item.count('B')>0:
                temp_item = 'B'
                temp_list.append(temp_item)
            elif hasA == True and item.count('A')>0:
                temp_item = 'A'
                temp_list.append(temp_item)
            else:
                temp_list.append(item)
        print(i)
        i += 1
        print(list(set(temp_list)))




def openFileA(num):
    if num == 1 or num == 2:
        fileA = 'fileA.csv'
        fileB = 'fileB.csv'
    elif num == 3 or num == 4:
        fileA = 'file2A.csv'
        fileB = 'file2B.csv'
    else:
        print("This week is not included")

    with open(fileA, 'r') as csvFile:
        num_households = getNumHouseholds(num,fileB)
        location = []
        temp_location = []
        reader = csv.DictReader(csvFile,delimiter = ',',quotechar='|')
        next(reader)
        totalBuylist = getTotalBuyList(num,fileB)
        print("WEEK : " + str(num))
        for j in range(num_households):
            print("HOUSE " + str(j))
            print("=====================================================")
            for row in reader:
                for i in totalBuylist[j]:
                    if i == row['NAME']:
                        temp_string = ''
                        if row['STORE A'] == 'Y':
                            temp_string += " A "
                        if row['STORE B'] == 'Y':
                            temp_string += ' B '
                        if row['STORE C'] == 'Y':
                            temp_string += ' C '
                        if num > 2:
                            if row['CHEAP STORE'] == 'Y':
                                temp_string += ' D '
 #                               print(row['NAME'])
                        temp_location.append(temp_string)
            location.insert(len(location),list(set(temp_location)))
#            print(set(temp_location))
            print("===================================")
            temp_location.clear()
            csvFile.seek(0)
        cleanUp(location)

        for i in location:
            i.sort()
            print(i)


num = int(input("Week : "))
openFileA(num)


