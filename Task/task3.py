import csv

#Student Name:KUAY TANG ZHENG
#Student ID:  19022570

DEBUG = False
#for storing the individual item information
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
#linked list
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
#linked list
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
#for storing the individual household information
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
#for storing the item and item quantity requirement(stored in with linked list)
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

#set all the item in a linked list
def setItem(item_linked,item_dict,item_price_dict):
    item_dict = {}
    with open("file3A.csv",'r') as csvFile:
        #get reader
        reader = csv.reader(csvFile)
        #get number of store
        num_store = getNumStore()
        next(reader)
        item = []
        i = 0
        for row in reader:
            i += 1
            store_list = []
            name = row[1]
            price = row[2]
            #if row and column not empty, add the store
            if row[3] != "":
                store_list.append("A")
            if row[4] != "":
                store_list.append("B")
            if row[5] != "":
                store_list.append("C")
            if row[6] != "":
                store_list.append("D")
            #create an Item instance append into item list
            item.append(Item(name,price,store_list))
            #create an Item instance add it as linked list
            item_linked.add(Item(name,price,store_list))
            
            
    return item
#set all the household requirent with linked list and item_quantity() class
def setShoppingList(item_list,num):
    with open("file3B.csv", 'r') as csvFile:
        reader = csv.reader(csvFile)
        shoppingList = []
        num_households = getNumHouseholds()
        #get all the household name
        households = (list(reader)[0])[2:num_households+2]
        csvFile.seek(0)
        next(reader)
        next(reader)
        #if week == 1 set the starting point and end point
        if num == 1:
            first_col = 2
            last_col = num_households + 2
        #if week == 2 set the starting point and end point
        elif num == 2:
            first_col = 2+num_households
            last_col = num_households*2+2
        else:
            print("ERROR WEEK")
        hid = 0
        for i in range(first_col,last_col):
            num_row = 0
            #create a shoppingList instance with the household name
            temp_shoppingList = ShoppingList(households[hid])
            hid += 1
            for row in reader:
                #if the item quantity requirement is not empty
                if row[i] != '':
                    #create ItemQuantity instance
                    item_quantity = ItemQuantity(item_list[num_row],int(row[i]))
                    #add the ItemQuantity instance into ShoppingList as linked list
                    temp_shoppingList.optimise_item_list.add(item_quantity)
                num_row += 1
            #reverse the linked list to make it easier to read and get
            temp_shoppingList.optimise_item_list.reverse()
            shoppingList.append(temp_shoppingList)
            csvFile.seek(0)
            next(reader)
            next(reader)

        del temp_shoppingList
        return shoppingList
# get the number of households from the csv file
def getNumHouseholds():
    with open("file3B.csv",'r') as csvFile:
        reader = csv.reader(csvFile)
        
        num_households = len(set(list(reader)[0]))-2

    return num_households
# get the number of store from the csv file
def getNumStore():
    with open("file3A.csv",'r') as csvFile:
        reader = csv.reader(csvFile)

        num_store = len(list(reader)[0])-3
    return num_store
#permutation for finding the best solution tools
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
#another version or permutation
def permutation_store(store):
    lenght = len(store)
    looped = store + store
    store_list = []
    for start in range(0,4):
        store_list.append(looped[start:start+3])
    return store_list

#find the possible and lowest substituition schedule
def optimise_list(shop_list,item_linked):
    #get the combination of 2 shop
    permutation_shop_list = permutation("ABCD",False)
    best_permu_list = []
    for household in shop_list:
        lowest_sub = 10
        lowest_p = []
        #permu_dict will be a dictionary with permutaion as key and substitute as value
        permu_dict = {}
        for p in permutation_shop_list:
            sub = 0
            permu_dict[p] = 100
            #start the ShoppingList item linked list
            current = household.optimise_item_list.head
            while current != None:
                #if item does not match than substitue num +1
                if current.get_store().count(p[0]) == 0 and current.get_store().count(p[1]) == 0:
                    sub += 1
                current = current.get_next()
            #if the number substituition requirement is lower than lowest substituition than change it as the lowest
            if sub < lowest_sub:
                lowest_sub = sub
                lowest_p = p
        if lowest_sub > 0:
            #to check if the other 3 shop combiantion work or not
            passed = False
            #get combination with 3 different shop
            for p in permutation_store("ABCD"):
                sub = 0
                current = household.optimise_item_list.head
                while current != None:
                    if current.get_store().count(p[0]) == 0 and current.get_store().count(p[1]) == 0 and current.get_store().count(p[2]) == 0:
                        sub += 1
                    current = current.get_next()
                #if no substituition require than append it as best combination
                if sub == 0:
                    best_permu_list.append(p)
                    passed = True
                    break
            #if failed than add shop as the best combination
            if passed == False:
                best_permu_list.append("ABCD")
        elif lowest_sub == 0:
            best_permu_list.append(lowest_p)
        else:
            print("ERROR IN optimises_list()")
    return best_permu_list
#print out the the schedule and task
def delivery(shop_list,best_permutation,item_dict,item_price_dict):
    num_shop_to_buy = 4
    bdd = "ABCD"
    bp = best_permutation
    num = 0
    shopping_schedule = []
    households_delivery_day = []
    day = 0
    for i in range(num_shop_to_buy):
        #item_dict is a dictionary with item name as key and 0 as value
        temp_item_dict = item_dict.copy()
        temp_hdd = []
        for household in shop_list:
            current = household.optimise_item_list.head
            while(current != None):
                next_current = current.get_next()
                #check the item that can be bought in the current day
                if current.get_store().count(bdd[i]) > 0:
                    #minimise the different times need to buy the same item
                    if i == 0 and current.get_store().count(bdd[i+1]) > 0:
                        pass
                    else:
                        #add the item_quantity into dictionary with item name as key
                        temp_item_dict[current.data.item.name] += current.data.quantity
                        #for debugging purpose
                        num += current.data.quantity
                        #remove the item from ShoppingList
                        household.optimise_item_list.remove(current.data.item.name)
                current = next_current
                #if the item requirement is empty than set a delivery day for this household
                if household.optimise_item_list.head == None:
                    temp_hdd.append(household.house_num)
        shopping_schedule.insert(len(shopping_schedule),temp_item_dict)
        households_delivery_day.insert(len(households_delivery_day),temp_hdd)
    #print out the schedule
    day_name = ['Monday','Tuesday','Wednesday','Thrusday']
    print("Shopping Schedule")     
    print("-----------------------------")
    i = 0
    shop_day = 0
    for day in range(2):
        input("Press Enter to continue...")
        print("DAY :" + day_name[day])
        print("STORE ",bdd[shop_day])
        for key,value in shopping_schedule[shop_day].items():
            if value != 0:
                print(key,end=' , ')
                print("Quantity : "+str(value))
        shop_day += 1
        input("Press Enter to continue...")
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


    print()
    delivery_day = 0
    print("Delivery Schedule")
    print("-----------------------------")
    for day in range(2):
        input("Press Enter to continue...")
        print("DAY :" +day_name[day])
        household = ''
        for deliver_schedule in households_delivery_day[delivery_day]:
            print(deliver_schedule,end=' ')
        delivery_day += 1
        for delivery_schedule in households_delivery_day[delivery_day]:
            print(delivery_schedule,end=' ')
        delivery_day += 1
        print()
        print()
        



        

#create a linked list     
item_list = UnorderedList()
item_dict = {}
item_price_dict = {}
#set item as linked list
item = setItem(item_list,item_dict,item_price_dict)
#create a dictionary with name as key and 0 as value
for i in item:
    item_dict[i.name] = 0
    item_price_dict[i.name] = i.price
item_list.reverse()

for week in range(1,3):
    print("WEEK  " + str(week+5))
    #set up ShoppingList for each household
    shop_list = setShoppingList(item,week) 
    best_permutation = []
    #find the minimun store requirement for each household
    best_permutation = optimise_list(shop_list,item_list)
    #buy and delivery,print out the schedule
    delivery(shop_list,best_permutation,item_dict,item_price_dict)





    
        


