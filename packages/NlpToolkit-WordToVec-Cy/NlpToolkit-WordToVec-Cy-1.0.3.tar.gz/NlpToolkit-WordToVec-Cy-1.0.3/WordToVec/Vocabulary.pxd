from Dictionary.Word cimport Word
from WordToVec.VocabularyWord cimport VocabularyWord


cdef class Vocabulary:

    cdef list __vocabulary
    cdef list __table

    cpdef int size(self)
    cpdef int getPosition(self, Word word)
    cpdef VocabularyWord getWord(self, int index)
    cpdef __constructHuffmanTree(self)
    cpdef __createUniGramTable(self)
    cpdef int getTableValue(self, int index)
    cpdef int getTableSize(self)
