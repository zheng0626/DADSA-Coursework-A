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

def permutation1(shop,fullChar):
    if len(shop) == 1:
        return [shop]
    
    l = []

    for i in range(len(shop)-1):
        m = shop[i:i+2]

        rem = shop[:i] + shop[i+2:]
        if fullChar == False:
            for p in rem:
                l.append(m + p)
        elif fullChar == True:
            for p in permutation(rem,True):
                l.append(m + p)
        else:
            print("ERROR permutation")
    return l


print(permutation('AB',False))
print(permutation('ABCD',False))
b1 = permutation('ABCD',False)
b2 = permutation('ABCD',False)

best = []
for i in range(len(b1)):
    for j in range(len(b2)):
        best.append(str(b1[i])+str(b2[j]))
#print(best)

my_dict = {}
m2_dict = {}
my_dict["Wheat"] = 1
my_dict["Bread"] = 2
m2_dict["lalalla"] = 3
m2_dict["lololol"] = 4
my_list = []
my_list.append(my_dict)
my_list.append(m2_dict)
print(my_list)

my_dict = {'x':500, 'y':5874, 'z': 560}

key_max = max(my_dict.keys(), key=(lambda k: my_dict[k]))
key_min = min(my_dict.keys(), key=(lambda k: my_dict[k]))

print('Maximum Value: ',key_max)
print('Minimum Value: ',my_dict[key_min])
print(key_max)