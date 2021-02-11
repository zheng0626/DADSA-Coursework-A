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
    lowest_p = permutation_shop_list[0]

    for p in permutation_shop_list:
        #to record the number of substituition require for this permutation
        sub = 0
        #get the head of the linked list from shop_list
        current = shop_list.optimise_item_list.head
        #will keep running if the current is not empty
        while current != None:
            #if current item store did not meet the permutation shop requirment
            if current.get_store().count(p[0]) == 0 and current.get_store().count(p[1]) == 0:
                sub += 1
            current = current.get_next()
        #if sub smaller than lowest_sub than change the sub to lowest_sub
        if sub < lowest_sub:
            lowest_sub = sub
            #record the lowest substituition require permutation
            lowest_p = p
        #because the code need not much about shop c so i add this code
        if sub == lowest_sub and p.count("C") > 0:
            lowest_p = p
    #if the lowest require subtituition is not 0 than substitue the item inside shop_list
    if lowest_sub != 0:
        substituition(shop_list,item_linked,lowest_p)

    #return the lowest require subtituition permutation
    return lowest_p

def substituition(shop_list,item_list,best_permutation):
    #best permutation get from optimise_list()
    p = best_permutation
    current = shop_list.optimise_item_list.head
    current_store = shop_list.optimise_item_list.head.get_store()

    while(current != None):
        #find the item that is needed to substitue
        if current.get_store().count(p[0]) == 0 and current.get_store().count(p[1]) == 0:
            #find the item in item_list linked list
            item = item_list.search(current.data.item.name)
            #get the previous list in linked list
            prev_item = item_list.getPreNode(item.data.name)
            #get the next list in linked list
            next_item = item.get_next()
            #for debugging
            if(False):
                print("ITEM CANNOT BE FULL FILLED IS :", end= ' ')
                print(item.data.name)
                print("FIRST CANDIDATE :",end= ' ')
                print(prev_item.data.name)
                print("NEXT CANDIDATE :", end= ' ')
                print(next_item.data.name)
            #to compare the nearest name with the item
            prev_w = 0
            next_w = 0
            for word in list(item.data.name):
                if prev_item.get_name().count(word) > next_item.get_name().count(word):
                    prev_w += 1
                elif prev_item.get_name().count(word) < next_item.get_name().count(word):
                    next_w += 1
            if prev_w > next_w:
                current.data.setItem(prev_item.data)
            elif prev_w < next_w:             
                current.data.setItem(next_item.data)
            else:
                print("CANNOT FOUND ANY SUBSTITUITION")
        current = current.get_next()

def delivery(best_delivery_day,shop_list,best_permutation,item_dict,item_price_dict):
    num_day_buy = len(best_delivery_day)
    bdd = best_delivery_day
    bp = best_permutation
    num = 0
    shopping_schedule = []
    households_delivery_day = []
    for i in range(num_day_buy):
        temp_item_dict = item_dict.copy()
        temp_hdd = []
        for num_household,household in enumerate(shop_list):
            current_day = bp[num_household].count(bdd[i])
            if i == num_day_buy-1:
                next_day = 1
            else:
                next_day = bp[num_household].count(bdd[i+1])
            if (current_day > 0 and next_day > 0) or household.next_delivery == True:
                current = household.optimise_item_list.head
                if household.next_delivery == True:
                    household.next_delivery = False
                else:
                    household.next_delivery = True
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
    for i,shop_schedule in enumerate(shopping_schedule):
        input("Press Enter to continue...")
        print("DAY "+ str(i+1))
        print("STORE "+bdd[i])
        for key,value in shop_schedule.items():
            if value != 0:
                print(key,end=' , ')
                print("Quantity : "+str(value))
        print()
    print("Delivery Schedule")
    print("-----------------------------")
    for i,deliver_schedule in enumerate(households_delivery_day):
        if i == 0:
            pass
        else:
            input("Press Enter to continue...")
            print("DAY "+str(i+1))
            for household in deliver_schedule:
                print(household,end=' ')
            print()
            print()
        

def delivery_date(best_permutation):
    delivery_date = []
    num_households = len(best_permutation)
    for p in permutation("ABC",True):
        temp_list = best_permutation
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
                delivery_date.append(extra_day)
    delivery_date = min(delivery_date,key = len)
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
                    temp_shoppingList.optimise_item_list.add(item_quantity)
                num_row += 1
            temp_shoppingList.optimise_item_list.reverse()
            shoppingList.append(temp_shoppingList)
            csvFile.seek(0)
            next(reader)
            next(reader)
        
        return shoppingList


        

        
item_list = UnorderedList()
item_dict = {}
item_price_dict = {}
item = setItem(item_list,item_dict,item_price_dict)
for i in item:
    item_dict[i.name] = 0
    item_price_dict[i.name] = i.price
item_list.reverse()

for week in range(1,3):
    print("WEEK "+str(week))
    shop_list = setShoppingList(item,week)
    best_permutation = []
    for i in range(len(shop_list)):
        best_permutation.append(optimise_list(shop_list[i],item_list))
    best_delivery_day = delivery_date(best_permutation)  
    delivery(best_delivery_day,shop_list,best_permutation,item_dict,item_price_dict)






    
        


