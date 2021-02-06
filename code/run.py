import csv

DEBUG = False

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

def optimise_list(shop_list,item_linked):
    permutation_shop_list = permutation("ABC",False)
    lowest_sub = 10
    i = 0
    sub = 0
    lowest_p = permutation_shop_list[0]
    sub_list = []
    lowest_sub_list = []

    for p in permutation_shop_list:
        sub = 0
        for shop in shop_list.item_list:
            store_to_buy = shop.item.store
            if store_to_buy.count(p[0]) == 0 and store_to_buy.count(p[1]) == 0:
                sub += 1
                sub_list.insert(len(sub_list),store_to_buy)
                sub_name = shop.item.name
        if sub < lowest_sub:
            lowest_sub = sub
            lowest_p = p
            lowest_sub_list = sub_list
            if sub != 0:
                lowest_sub_name = sub_name
        if sub ==  lowest_sub and p.count("C") > 0:
            lowest_p = p
            lowest_sub_list = sub_list
            if sub != 0:
                lowest_sub_name = sub_name            
        sub_list = []
    if lowest_sub != 0:
        substituition(shop_list,item_linked,lowest_p)
    #print(lowest_sub)
    print(lowest_p)
    return lowest_p
    # if lowest_sub != 0:
    #     print(lowest_sub_list)
    #     print(lowest_sub_name)


            
def substituition(shop_list,item_list,best_permutation):
    p = best_permutation
    for shop in shop_list.item_list:
        store_to_buy = shop.item.store
        if store_to_buy.count(p[0]) == 0 and store_to_buy.count(p[1]) == 0:
            item = item_list.search(shop.item.name)
            prev_item = item_list.getPreNode(item.data.name)
            next_item = item.get_next()
            if(DEBUG == True):
                print("ITEM CANNOT BE FULL FILLED IS :", end= ' ')
                print(item.data.name)
                print("FIRST CANDIDATE :",end= ' ')
                print(prev_item.data.name)
                print("NEXT CANDIDATE :", end= ' ')
                print(next_item.data.name)
            prev_w = 0
            next_w = 0
            for word in list(item.data.name):
                if prev_item.data.name.count(word) > next_item.data.name.count(word):
                    prev_w += 1
                elif prev_item.data.name.count(item.data.name) < next_item.data.name.count(item.data.name):
                    next_w += 1
            if prev_w > next_w:
                shop.setItem(prev_item.data)
                print("THE NEAREST CANDIDATE IS :",end = ' ')
                print(prev_item.data.name)
            elif next_w > prev_w:
                shop.setItem(next_item.data)
                shop.getItem().name += "(sub)"                
                print("THE NEAREST CANDIDATE IS :",end = ' ')
                print(next_item.data.name)
            else:
                print("CANNOT BE FOUND SUBSTITUITION")
    print(shop_list)

def delivery(best_delivery_day,item_list,shop_list):
    print(shop_list[0].item_list)
    


def delivery_date(best_permutation):
    print("BEST :",end = ' ')
    print(best_permutation)
    delivery_date = []
    num_households = len(best_permutation)
    print(len(best_permutation))
    for p in permutation("ABC",True):
        temp_list = best_permutation
        print(p)
        num_done = 0
        extra_day = p
        for bp in temp_list:
            complete = False
            if bp.count(p[0]) != 0 and bp.count(p[1]) != 0:
                complete = True
                num_done += 1
            elif bp.count(p[1]) != 0 and bp.count(p[2]) != 0:
                complete = True
                num_done += 1
            else:
                if bp.count(extra_day[-1]) != 0:
                    if bp.count(extra_day[-2]) != 0:
                        complete = True
                        num_done += 1
                    for day in p:
                        if complete == True:
                            break
                        if day != extra_day[-1] and bp.count(day) != 0:
                            complete = True
                            num_done += 1
                            extra_day += day
                if complete == False:
                    extra_day += bp
                    num_done += 1
                    complete = True
            if num_done == num_households:
                print("DONE BEST PERMUTATION IS :",end= ' ')
                delivery_date.append(extra_day)
                print(extra_day)
    print("BEST DAY TO DELIVERY IS :", end = ' ')
    print(min(delivery_date,key = len))
    return(delivery_date)                 

            
            
        








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
            if current.get_data() == item:
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
            print(printval.data.name)
            printval = printval.get_next()

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

    def setItem(self,item):
        self.item = item

    def __str__(self):
        return str(self.item) + ", Quantity :" + str(self.quantity) + "\n"


def setItem(item_linked):
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
            item_linked.add(Item(name,price,store_list))
            
    return item

def setShoppingList(item_list,num = 1):
    with open("fileB.csv", 'r') as csvFile:
        reader = csv.reader(csvFile)
        shoppingList = []
        num_households = getNumHouseholds()
        households = (list(reader)[0])[1:num_households+1]
        csvFile.seek(0)
        next(reader)
        next(reader)
        if num == 1:
            first_col = 1
            last_col = num_households + 1
        elif num == 2:
            first_col = 1+num_households
            last_col = num_households*2+1
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





        

        
item_list = UnorderedList()
item = setItem(item_list)
#print("REVERSED")
item_list.reverse()
print(item_list.listprint())
ShoppingList = setShoppingList(item,2)
best_permutation = []
for i in range(len(ShoppingList)):
    best_permutation.append(optimise_list(ShoppingList[i],item_list))
best_delivery_day = delivery_date(best_permutation)
delivery(best_delivery_day,item_list,ShoppingList)


    
        


