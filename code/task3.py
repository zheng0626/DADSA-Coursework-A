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
    best_set = set(best_permutation)
    len_best_set = len(best_set)
    b1 = permutation("ABCD",False)
    b2 = permutation("ABCD",False)
    permu_list = []
    for i in range(len(b1)):
        for j in range(len(b2)):
            permu_list.append(str(b1[i])+str(b2[j]))
    permu = permutation("ABCD",True)
    for i in range(len(permu)):
        permu_list.append(permu[i])
    print(best_set)
    print(len_best_set)
    delivery_date = []
    for p in permu_list:
        temp_list = best_set
        num_done = 0
        extra_day = p
        for bp in temp_list:
            complete = False
            for i in range(len(extra_day) - 1):
                same_word = False
                if len(bp) == 3 and (i+2)!=len(extra_day):
                    for j in range(3):
                        for k in range(3):
                            if j != k:
                                if extra_day[j] == extra_day[k]:
                                    same_word = True
                                    break
                    if same_word == True:
                        pass
                    elif bp.count(extra_day[i]) != 0 and bp.count(extra_day[i+1]) != 0 and bp.count(extra_day[i+2]) != 0:
                        complete = True
                        num_done += 1
                        break
                elif len(bp) == 2: 
                    if bp.count(extra_day[i]) != 0 and bp.count(extra_day[i+1]) != 0:
                        complete = True
                        num_done += 1
                        break
            if complete == False:
                for day in "ABCD":
                    if len(bp) == 3:
                        if bp.count(day) != 0 and day != extra_day[-1] and bp.count(extra_day[-1]) != 0 and bp.count(extra_day[-2]) !=0:
                            extra_day += day
                            complete = True
                            num_done += 1
                            break
                    elif len(bp) == 2:
                        if bp.count(day) != 0 and day != extra_day[-1] and bp.count(extra_day[-1])!= 0:
                            extra_day += day
                            complete = True
                            num_done += 1
                            break
            if complete == False:
                extra_day += bp
                num_done += 1
                complete = True
        if num_done == len_best_set:
            delivery_date.append(extra_day)
        else:
            print(num_done)
            print("ERROR IN delivery_date()")
    delivery_date = min(delivery_date,key=len)
    print("DELIVERY DATE")
    print(delivery_date)
    return delivery_date





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
    best_delivery_day = delivery_date(best_permutation)
    delivery(best_delivery_day,shop_list,best_permutation,item_dict,item_price_dict)
    print(best_delivery_day)
    print(best_permutation)
    for i in range(len(shop_list)):
        print(best_permutation[i])
    for i in range(len(shop_list)):
        print(shop_list[i].house_num)
    shop_list[i].optimise_item_list.listprint()





    
        


