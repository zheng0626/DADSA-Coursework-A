import csv

DEBUG = False

def getNumHouseholds():
    with open("file3B.csv",'r') as csvFile:
        reader = csv.reader(csvFile)
        
        num_households = len(set(list(reader)[0]))-2

    return num_households

def getNumStore():
    with open("file3A.csv",'r') as csvFile:
        reader = csv.reader(csvFile)

        num_store = len(list(reader)[0])-3
    return num_store

def permutation(shop,fullChar):
    if len(shop) == 1:
        return [shop]
    
    l = []

    for i in range(len(shop)):
        m = shop[i]

        rem = shop[:i] + shop[i+1:]
        if fullChar == False:
            for p in rem:
                l.append(m + p)
        elif fullChar == True:
            for p in permutation(rem,True):
                l.append(m + p)
        else:
            print("ERROR permutation")
    return l

def permutation_store(store):
    lenght = len(store)
    looped = store + store
    store_list = []
    for start in range(0,4):
        store_list.append(looped[start:start+3])
    return store_list


def optimise_list(shop_list,item_linked):
    permutation_shop_list = permutation("ABCD",False)
    best_permu_list = []
    for household in shop_list:
        lowest_sub = 10
        lowest_p = []
        permu_dict = {}
        for p in permutation_shop_list:
            sub = 0
            permu_dict[p] = 100
            current = household.optimise_item_list.head
            while current != None:
                if current.get_store().count(p[0]) == 0 and current.get_store().count(p[1]) == 0:
                    sub += 1
                current = current.get_next()
            if sub < lowest_sub:
                lowest_sub = sub
                lowest_p = p
        print(household.house_num,end=' ')
        print(lowest_p,end=' ')
        print(lowest_sub)
        if lowest_sub > 0:
            passed = False
            for p in permutation_store("ABCD"):
                sub = 0
                current = household.optimise_item_list.head
                while current != None:
                    if current.get_store().count(p[0]) == 0 and current.get_store().count(p[1]) == 0 and current.get_store().count(p[2]) == 0:
                        sub += 1
                    current = current.get_next()
                if sub == 0:
                    best_permu_list.append(p)
                    passed = True
                    break
            if passed == False:
                best_permu_list.append("ABCD")
        elif lowest_sub == 0:
            best_permu_list.append(lowest_p)
        else:
            print("ERROR IN optimises_list()")
    print(best_permu_list)
    return best_permu_list
                    
                


def delivery(shop_list,best_permutation,item_dict,item_price_dict):
    num_shop_to_buy = 4
    bdd = "ABCD"
    bp = best_permutation
    num = 0
    shopping_schedule = []
    households_delivery_day = []
    day = 0
    for i in range(num_shop_to_buy):
        temp_item_dict = item_dict.copy()
        temp_hdd = []
        for household in shop_list:
            current = household.optimise_item_list.head
            while(current != None):
                next_current = current.get_next()
                if current.get_store().count(bdd[i]) > 0:
                    if i == 0 and current.get_store().count(bdd[i+1]) > 0:
                        pass
                    else:
                        temp_item_dict[current.data.item.name] += current.data.quantity
                        num += current.data.quantity
                        household.optimise_item_list.remove(current.data.item.name)
                current = next_current
                if household.optimise_item_list.head == None:
                    temp_hdd.append(household.house_num)
        shopping_schedule.insert(len(shopping_schedule),temp_item_dict)
        households_delivery_day.insert(len(households_delivery_day),temp_hdd)

    print("Shopping Schedule")     
    print("-----------------------------")
    i = 0
    shop_day = 0
    for day in range(2):
        input("Press Enter to continue...")
        print("DAY " + str(day + 1))
        print("STORE ",bdd[shop_day])
        for key,value in shopping_schedule[shop_day].items():
            if value != 0:
                print(key,end=' , ')
                print("Quantity : "+str(value))
        shop_day += 1
        print()
        if shop_day == 3:
            print("CHEAP STORE")
        else:
            print("STORE ",bdd[shop_day])
        for key,value in shopping_schedule[shop_day].items():
            if value != 0:
                print(key,end=' , ')
                print("Quantity : "+str(value))
        shop_day += 1


            
    # for shop_schedule in shopping_schedule:
    #     input("Press Enter to continue...")
    #     print("DAY "+ str(i+1))
    #     if shop != 3:
    #         print("STORE ",bdd[shop])
    #         shop += 1
    #     else:
    #         print("CHEAP STORE")

    #     for key,value in shop_schedule.items():
    #         if value != 0:
    #             print(key,end=' , ')
    #             print("Quantity : "+str(value))
    #     print()
    delivery_day = 0
    print("Delivery Schedule")
    print("-----------------------------")
    for day in range(2):
        input("Press Enter to continue...")
        print("DAY " +str(day))
        household = ''
        for deliver_schedule in households_delivery_day[delivery_day]:
            print(deliver_schedule,end=' ')
        delivery_day += 1
        for delivery_schedule in households_delivery_day[delivery_day]:
            print(delivery_schedule,end=' ')
        delivery_day += 1
        print()
        print()
    # for i,deliver_schedule in enumerate(households_delivery_day):
    #     input("Press Enter to continue...")
    #     print("DAY "+str(i+1))
    #     for household in deliver_schedule:
    #         print(household,end=' ')
    #     print()
    #     print()
        



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

class Node:
    def __init__(self,init_data):
        self.data = init_data
        self.next = None

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next
    
    def get_store(self):
        return self.data.item.store
    
    def get_name(self):
        return self.data.name
    
    def set_data(self,new_data):
        self.data = new_data
    
    def set_next(self,new_next):
        self.next = new_next

class UnorderedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head == None

    def add(self,item):
        temp = Node(item)
        temp.set_next(self.head)
        self.head = temp
        

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.get_next()
        return count

    def search(self,item):
        current = self.head
        found = False
        while current != None and not found:
            if current.get_data().name == item:
                found = True
                return current
            else:
                current = current.get_next()
        return None


    def getPreNode(self,item):
        current = self.head
        previous = None
        found = False
        while current != None and not found:
            if current.get_data().name == item:
                found = True
                return previous
            else:
                previous = current
                current = current.get_next()
        return None
    
    def reverse(self):
        current = self.head
        following = self.head
        previous = None

        while(current != None):
            following = following.get_next()
            current.set_next(previous)
            previous = current
            current = following

        self.head = previous

    def remove(self,item):
        current = self.head
        previous = None
        found = False
        while current != None and not found:
            if current.get_data().item.name == item:
                found = True
            else:
                previous = current
                current = current.get_next()
        if previous == None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())
        

    def listprint(self):
        printval = self.head
        while printval is not None:
            print(printval.data.item.name)
            printval = printval.get_next()

class ShoppingList:
    def __init__(self,house_num):
        self.house_num = house_num
        self.item_list = []
        self.optimise_item_list = UnorderedList()
        self.next_delivery = False

    def add_item(self,item_quantity):
        self.item_list.append(item_quantity)

    def get_item_list(self):
        return self.item_list
    
    def del_item(self,item_name):
        for i,item in enumerate(self.item_list):
            print(item.item.name)
            if item.item.name == item_name:
                print(item.item.name)
                print(self.item_list[i].item.name)
                self.item_list.remove(item)
                break

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

    def setItem(self,item):
        self.item = item

    def __str__(self):
        return str(self.item) + ", Quantity :" + str(self.quantity) + "\n"


def setItem(item_linked,item_dict,item_price_dict):
    item_dict = {}
    with open("file3A.csv",'r') as csvFile:
        reader = csv.reader(csvFile)
        num_store = getNumStore()
        next(reader)
        item = []
        i = 0
        for row in reader:
            i += 1
            store_list = []
            name = row[1]
            price = row[2]
            if row[3] != "":
                store_list.append("A")
            if row[4] != "":
                store_list.append("B")
            if row[5] != "":
                store_list.append("C")
            if row[6] != "":
                store_list.append("D")
            item.append(Item(name,price,store_list))
            item_linked.add(Item(name,price,store_list))
            
            
    return item

def setShoppingList(item_list,num):
    with open("file3B.csv", 'r') as csvFile:
        reader = csv.reader(csvFile)
        shoppingList = []
        num_households = getNumHouseholds()
        print(num_households)
        households = (list(reader)[0])[2:num_households+2]
        print(households)
        csvFile.seek(0)
        next(reader)
        next(reader)
        if num == 1:
            first_col = 2
            last_col = num_households + 2
        elif num == 2:
            first_col = 2+num_households
            last_col = num_households*2+2
        else:
            print("ERROR WEEK")
        j = 0
        for i in range(first_col,last_col):
            num_row = 0
            
            temp_shoppingList = ShoppingList(households[j])
            j += 1
            for row in reader:
                if row[i] != '':
                    item_quantity = ItemQuantity(item_list[num_row],int(row[i]))
                    temp_shoppingList.optimise_item_list.add(item_quantity)
                num_row += 1
            temp_shoppingList.optimise_item_list.reverse()
            shoppingList.append(temp_shoppingList)
            csvFile.seek(0)
            next(reader)
            next(reader)

        del temp_shoppingList
        return shoppingList

def getHouseHolds():
    with open("file3B.csv", 'r') as csvFile:
        reader = csv.reader(csvFile)
        num_households = getNumHouseholds()
        households = (list(reader)[0])[1:num_households+1]
        print(households)





        

        
item_list = UnorderedList()
item_dict = {}
item_price_dict = {}
item = setItem(item_list,item_dict,item_price_dict)
for i in item:
    item_dict[i.name] = 0
    item_price_dict[i.name] = i.price
item_list.reverse()

for week in range(1,3):
    print("WEEK + " + str(week+3))
    shop_list = setShoppingList(item,week) 
    best_permutation = []
    best_permutation = optimise_list(shop_list,item_list)
    delivery(shop_list,best_permutation,item_dict,item_price_dict)
    for i in range(len(shop_list)):
        print(shop_list[i].house_num)
    shop_list[i].optimise_item_list.listprint()





    
        


