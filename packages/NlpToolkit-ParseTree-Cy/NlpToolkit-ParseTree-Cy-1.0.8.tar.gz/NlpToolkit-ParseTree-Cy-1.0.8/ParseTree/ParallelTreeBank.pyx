cdef class ParallelTreeBank:

    def __init__(self, folder1: str, folder2: str, pattern: str = None):
        self.fromTreeBank = TreeBank(folder1, pattern)
        self.toTreeBank = TreeBank(folder2, pattern)
        self.removeDifferentTrees()

    cpdef removeDifferentTrees(self):
        cdef int i, j
        i = 0
        j = 0
        while i < self.fromTreeBank.size() and j < self.toTreeBank.size():
            if self.fromTreeBank.get(i).getName() < self.toTreeBank.get(j).getName():
                self.fromTreeBank.removeTree(i)
            elif self.fromTreeBank.get(i).getName() > self.toTreeBank.get(j).getName():
                self.toTreeBank.removeTree(j)
            else:
                i = i + 1
                j = j + 1
        while i < self.fromTreeBank.size():
            self.fromTreeBank.removeTree(i)
        while j < self.toTreeBank.size():
            self.toTreeBank.removeTree(j)

    cpdef int size(self):
        return self.fromTreeBank.size()

    cpdef ParseTree fromTree(self, int index):
        return self.fromTreeBank.get(index)

    cpdef ParseTree toTree(self, int index):
        return self.toTreeBank.get(index)

    cpdef TreeBank getFromTreeBank(self):
        return self.fromTreeBank

    cpdef TreeBank getToTreeBank(self):
        return self.toTreeBank
