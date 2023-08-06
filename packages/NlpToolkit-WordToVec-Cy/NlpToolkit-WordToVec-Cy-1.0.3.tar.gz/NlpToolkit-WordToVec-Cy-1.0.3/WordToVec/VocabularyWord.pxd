from Dictionary.Word cimport Word


cdef class VocabularyWord(Word):

    cdef int __count, __codeLength
    cdef list __code, __point

    cpdef int getCount(self)
    cpdef setCodeLength(self, int codeLength)
    cpdef setCode(self, int index, int value)
    cpdef setPoint(self, int index, int value)
    cpdef int getCodeLength(self)
    cpdef int getPoint(self, int index)
    cpdef int getCode(self, int index)
