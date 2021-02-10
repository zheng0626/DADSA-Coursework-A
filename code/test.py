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
print(permutation_store("ABCD"))
