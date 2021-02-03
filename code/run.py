import csv

def getNumHouseholds():
    with open("fileB.csv",'r') as csvFile:
        reader = csv.reader(csvFile)
        
        num_households = len(set(list(reader)[0]))-1

    return num_households

def getNumStore():
    with open("fileA.csv",'r') as csvFile:
        reader = csv.reader(csvFile)

        num_store = len(list(reader)[0])-3
    return num_store

def permutation():
    shop = list('ABC')
    if len(shop) == 1:
        return [shop]
    
    l = []

    for i in range(len(shop)):
        m = shop[i]

        rem = shop[:i] + shop[i+1:]

        for p in rem:
            l.append(m + p)
    return l

def optimise_list(shop_list):
    permutation_shop_list = permutation()
    lowest_sub = 0
    i = 0
    sub = 0
    lowest_p = []
    store = shop_list.item.store

    for shop in shop_list.item.store:
        if shop.count(p[0][0]) == 0 and shop.count(p[0][1]) == 0:
            sub += 1
    lowest_sub = sub

    for p in permutation_shop_list:
        sub = 0
        for shop in shop_list:
            if shop.count(p[0]) == 0 or shop.count(p[1]) == 0:
                sub += 1
        if sub < lowest_sub:
            lowest_sub = sub
            lowest_p = p



            





class Item:
    def __init__(self, name, price, store):
        self.name = name
        self.price = price
        self.store = store

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getStore(self):
        return self.store

    def __str__(self):
        return "PRODUCT : " + self.name + ", price : " + self.price + ", store : " + str(self.store)

class ShoppingList:
    def __init__(self,house_num):
        self.house_num = house_num
        self.item_list = []
        self.optimise_item_list = []

    def add_item(self,item_quantity):
        self.item_list.append(item_quantity)

    def get_item_list(self):
        return self.item_list

    def __str__(self):
        string = "HOUSE : " + self.house_num + "\n"
        
        for item_quantity in self.item_list:
            string += str(item_quantity)

        return string

class ItemQuantity:
    def __init__(self,item,quantity):
        self.item = item
        self.quantity = quantity

    def getItem(self):
        return self.item

    def __str__(self):
        return str(self.item) + ", Quantity :" + str(self.quantity) + "\n"


def setItem():
    with open("fileA.csv",'r') as csvFile:
        reader = csv.reader(csvFile)
        num_store = getNumStore()
        next(reader)
        item = []
        i = 0
        for row in reader:
            i += 1
            name = row[1]
            price = row[2]
            store_list = []
            if row[3] != "":
                store_list.append("A")
            if row[4] != "":
                store_list.append("B")
            if row[5] != "":
                store_list.append("C")
            item.append(Item(name,price,store_list))
            
    return item

def setShoppingList(item_list):
    with open("fileB.csv", 'r') as csvFile:
        reader = csv.reader(csvFile)
        shoppingList = []
        num_households = getNumHouseholds()
        households = (list(reader)[0])[1:num_households+1]
        csvFile.seek(0)
        next(reader)
        next(reader)
        for i in range(1,num_households+1):
            num_row = 0
            temp_shoppingList = ShoppingList(households[i-1])
            for row in reader:
                if row[i] != '':
                    item_quantity = ItemQuantity(item_list[num_row],int(row[i]))
                    temp_shoppingList.add_item(item_quantity)
                num_row += 1
            shoppingList.append(temp_shoppingList)
            csvFile.seek(0)
            next(reader)
            next(reader)
        
        return shoppingList
            

                

def getHouseHolds():
    with open("fileB.csv", 'r') as csvFile:
        reader = csv.reader(csvFile)
        num_households = getNumHouseholds()
        households = (list(reader)[0])[1:num_households+1]
        print(households)





        

        

item = setItem()
ShoppingList = setShoppingList(item)
print(ShoppingList[2].item_list[0].item.store)

    
        


