def permutation(lst):
    if len(lst) == 1:
        return [lst]
    
    l = []

    for i in range(len(lst)):
        m = lst[i]

        rem = lst[:i] + lst[i+1:]

        for p in rem:
            l.append(m + p)
    return l

data = list('abcd')

for p in permutation(data):
    print(p)
    print(p.count('a'))