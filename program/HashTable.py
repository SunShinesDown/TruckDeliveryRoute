# implementation of a hashTable data structure
class HashTable:

    def __init__(self, size=7):
        self.size = size
        self.table = [None] * self.size

    def __hash(self, key):
        return key % len(self.table)

    def insert(self, key, item):
        index = self.__hash(key)
        if self.table[index] == None:
            self.table[index] = []
        self.table[index].append([key, item])

    def search(self, key):
        toReturn = None
        index = self.__hash(key)
        if self.table[index] != None:
            pairList = self.table[index]
            for pair in pairList:
                if pair[0] == key:
                    toReturn = pair[1]
                    break
        return toReturn

    def remove(self, key):
        toReturn = False
        index = self.__hash(key)
        if self.table[index] != None:
            for pair in self.table[index]:
                if pair[0] == key:
                    toReturn = True
                    self.table[index].remove(pair)
                    break
            return toReturn
