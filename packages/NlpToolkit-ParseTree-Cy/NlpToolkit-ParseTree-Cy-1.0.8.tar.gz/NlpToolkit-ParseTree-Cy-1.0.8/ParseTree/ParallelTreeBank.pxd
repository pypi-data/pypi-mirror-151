from ParseTree.ParseTree cimport ParseTree
from ParseTree.TreeBank cimport TreeBank

cdef class ParallelTreeBank:

    cdef TreeBank fromTreeBank
    cdef TreeBank toTreeBank

    cpdef removeDifferentTrees(self)
    cpdef int size(self)
    cpdef ParseTree fromTree(self, int index)
    cpdef ParseTree toTree(self, int index)
    cpdef TreeBank getFromTreeBank(self)
    cpdef TreeBank getToTreeBank(self)
