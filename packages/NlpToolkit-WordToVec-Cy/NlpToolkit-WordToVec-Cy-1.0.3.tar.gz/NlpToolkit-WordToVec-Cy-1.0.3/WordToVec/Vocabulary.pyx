import math
from Corpus.Corpus cimport Corpus


cdef class Vocabulary:

    def wordComparator(self, word: VocabularyWord):
        return word.getName()

    def __init__(self, corpus: Corpus):
        """
        Constructor for the Vocabulary class. For each distinct word in the corpus, a VocabularyWord
        instance is created. After that, words are sorted according to their occurrences. Unigram table is constructed,
        where after Huffman tree is created based on the number of occurrences of the words.

        PARAMETERS
        ----------
        corpus : Corpus
            Corpus used to train word vectors using Word2Vec algorithm.
        """
        cdef Word word
        cdef set wordList
        wordList = corpus.getWordList()
        self.__vocabulary = []
        for word in wordList:
            self.__vocabulary.append(VocabularyWord(word.getName(), corpus.getCount(word)))
        self.__vocabulary.sort()
        self.__createUniGramTable()
        self.__constructHuffmanTree()
        self.__vocabulary.sort(key=self.wordComparator)

    cpdef int size(self):
        """
        Returns number of words in the vocabulary.

        RETURNS
        -------
        int
            Number of words in the vocabulary.
        """
        return len(self.__vocabulary)

    cpdef int getPosition(self, Word word):
        """
        Searches a word and returns the position of that word in the vocabulary. Search is done using binary search.

        PARAMETERS
        ----------
        word : Word
            Word to be searched.

        RETURNS
        -------
        int
         * @return Position of the word searched.
        """
        cdef int lo, hi, mid
        lo = 0
        hi = len(self.__vocabulary)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.__vocabulary[mid].getName() < word.getName():
                lo = mid + 1
            else:
                hi = mid
        return lo

    cpdef VocabularyWord getWord(self, int index):
        """
        Returns the word at a given index.

        PARAMETERS
        ----------
        index : int
            Index of the word.

        RETURNS
        -------
        VocabularyWord
            The word at a given index.
        """
        return self.__vocabulary[index]

    cpdef __constructHuffmanTree(self):
        """
        Constructs Huffman Tree based on the number of occurences of the words.
        """
        cdef list count, code, point, binary, parentNode
        cdef int a, pos1, pos2, min1i, min2i, i, b
        count = [0] * (len(self.__vocabulary) * 2 + 1)
        code = [0] * VocabularyWord.MAX_CODE_LENGTH
        point = [0] * VocabularyWord.MAX_CODE_LENGTH
        binary = [0] * (len(self.__vocabulary) * 2 + 1)
        parentNode = [0] * (len(self.__vocabulary) * 2 + 1)
        for a in range(len(self.__vocabulary)):
            count[a] = self.__vocabulary[a].getCount()
        for a in range(len(self.__vocabulary), len(self.__vocabulary) * 2):
            count[a] = 1000000000
        pos1 = len(self.__vocabulary) - 1
        pos2 = len(self.__vocabulary)
        for a in range(len(self.__vocabulary) - 1):
            if pos1 >= 0:
                if count[pos1] < count[pos2]:
                    min1i = pos1
                    pos1 = pos1 - 1
                else:
                    min1i = pos2
                    pos2 = pos2 + 1
            else:
                min1i = pos2
                pos2 = pos2 + 1
            if pos1 >= 0:
                if count[pos1] < count[pos2]:
                    min2i = pos1
                    pos1 = pos1 - 1
                else:
                    min2i = pos2
                    pos2 = pos2 + 1
            else:
                min2i = pos2
                pos2 = pos2 + 1
            count[len(self.__vocabulary) + a] = count[min1i] + count[min2i]
            parentNode[min1i] = len(self.__vocabulary) + a
            parentNode[min2i] = len(self.__vocabulary) + a
            binary[min2i] = 1
        for a in range(len(self.__vocabulary)):
            b = a
            i = 0
            while True:
                code[i] = binary[b]
                point[i] = b
                i = i + 1
                b = parentNode[b]
                if b == len(self.__vocabulary) * 2 - 2:
                    break
            self.__vocabulary[a].setCodeLength(i)
            self.__vocabulary[a].setPoint(0, len(self.__vocabulary) - 2)
            for b in range(i):
                self.__vocabulary[a].setCode(i - b - 1, code[b])
                self.__vocabulary[a].setPoint(i - b, point[b] - len(self.__vocabulary))

    cpdef __createUniGramTable(self):
        """
        Constructs the unigram table based on the number of occurences of the words.
        """
        cdef double total, d1
        cdef VocabularyWord vocabularyWord
        cdef int i, a
        total = 0
        self.__table = [0] * (2 * len(self.__vocabulary))
        for vocabularyWord in self.__vocabulary:
            total += math.pow(vocabularyWord.getCount(), 0.75)
        i = 0
        d1 = math.pow(self.__vocabulary[i].getCount(), 0.75) / total
        for a in range(2 * len(self.__vocabulary)):
            self.__table[a] = i
            if a / (2 * len(self.__vocabulary) + 0.0) > d1:
                i = i + 1
                d1 += math.pow(self.__vocabulary[i].getCount(), 0.75) / total
            if i >= len(self.__vocabulary):
                i = len(self.__vocabulary) - 1

    cpdef int getTableValue(self, int index):
        """
        Accessor for the unigram table.

        PARAMETERS
        ----------
        index : int
            Index of the word.

        RETURNS
        -------
        int
            Unigram table value at a given index.
        """
        return self.__table[index]

    cpdef int getTableSize(self):
        """
        Returns size of the unigram table.

        RETURNS
        -------
        int
            Size of the unigram table.
        """
        return len(self.__table)
