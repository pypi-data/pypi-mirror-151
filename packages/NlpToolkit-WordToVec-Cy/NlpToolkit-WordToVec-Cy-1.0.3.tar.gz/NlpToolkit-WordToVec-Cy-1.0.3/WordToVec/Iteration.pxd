from Corpus.Corpus cimport Corpus
from Corpus.Sentence cimport Sentence
from WordToVec.WordToVecParameter cimport WordToVecParameter


cdef class Iteration:

    cdef int __wordCount, __lastWordCount, __wordCountActual, __iterationCount, __sentencePosition, __sentenceIndex
    cdef double __startingAlpha, __alpha
    cdef Corpus __corpus
    cdef WordToVecParameter __wordToVecParameter

    cpdef double getAlpha(self)
    cpdef int getIterationCount(self)
    cpdef int getSentenceIndex(self)
    cpdef int getSentencePosition(self)
    cpdef alphaUpdate(self)
    cpdef Sentence sentenceUpdate(self, Sentence currentSentence)