from itertools import combinations

def createNextEi(oldEi,i):
    newEi = []
    oldEiset = set()
    for tuple in oldEi:
        oldEiset.add(tuple)
    set1 = set()
    for tuple in oldEi:
        for k in range(0,i):
            set1.add(tuple[k])  #set1 consists of all the vertices involved in edges in oldEi
    print set1
    combs = combinations(set1,i+1)
    for comb in combs:
        smallercombsset = set()
        smallercombs = combinations(comb,i)
        for smallercomb in smallercombs:
            smallercombsset.add(smallercomb)
        if smallercombsset.issubset(oldEiset):
            newEi.append(comb)
    return newEi

def main():
    oldEi = combinations(['e1','e2','e3','e4'],2)
    print list(oldEi)
    print list(createNextEi(oldEi,2)) #should contain [(e1,e2,e3),]

if __name__ == "__main__":
    main()