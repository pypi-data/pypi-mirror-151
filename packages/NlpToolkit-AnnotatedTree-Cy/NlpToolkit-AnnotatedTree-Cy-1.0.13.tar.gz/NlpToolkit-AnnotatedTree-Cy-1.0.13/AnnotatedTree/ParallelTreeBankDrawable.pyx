from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable
from AnnotatedTree.TreeBankDrawable cimport TreeBankDrawable
from ParseTree.ParallelTreeBank cimport ParallelTreeBank


cdef class ParallelTreeBankDrawable(ParallelTreeBank):

    def __init__(self, folder1: str, folder2: str, pattern: str = None):
        self.fromTreeBank = TreeBankDrawable(folder1, pattern)
        self.toTreeBank = TreeBankDrawable(folder2, pattern)
        self.removeDifferentTrees()

    cpdef ParseTreeDrawable fromTree(self, int index):
        return self.fromTreeBank.get(index)

    cpdef ParseTreeDrawable toTree(self, int index):
        return self.toTreeBank.get(index)

    cpdef TreeBankDrawable getFromTreeBank(self):
        return self.fromTreeBank

    cpdef TreeBankDrawable getToTreeBank(self):
        return self.toTreeBank
