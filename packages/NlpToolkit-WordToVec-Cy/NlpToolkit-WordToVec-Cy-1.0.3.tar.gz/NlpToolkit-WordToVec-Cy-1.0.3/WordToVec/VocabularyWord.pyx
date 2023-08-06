cdef class VocabularyWord(Word):

    MAX_CODE_LENGTH = 40

    def __init__(self, name: str, count: int):
        """
        Constructor for a VocabularyWord. The constructor gets name and count values and sets the corresponding
        attributes. It also initializes the code and point arrays for this word.

        PARAMETERS
        ----------
        name : str
            Lemma of the word
        count : int
            Number of occurrences of this word in the corpus
        """
        super().__init__(name)
        self.__count = count
        self.__code = self.MAX_CODE_LENGTH * [0]
        self.__point = self.MAX_CODE_LENGTH * [0]
        self.__codeLength = 0

    def __lt__(self, other: VocabularyWord) -> bool:
        return self.__count < other.__count

    def __gt__(self, other: VocabularyWord) -> bool:
        return self.__count > other.__count

    def __eq__(self, other: VocabularyWord) -> bool:
        return self.__count == other.__count

    cpdef int getCount(self):
        """
        Accessor for the count attribute.

        RETURNS
        -------
        int
            Number of occurrences of this word.
        """
        return self.__count

    cpdef setCodeLength(self, int codeLength):
        """
        Mutator for codeLength attribute.

        PARAMETERS
        ----------
        codeLength : int
            New value for the codeLength.
        """
        self.__codeLength = codeLength

    cpdef setCode(self, int index, int value):
        """
        Mutator for code attribute.

        PARAMETERS
        ----------
        index : int
            Index of the code
        value : int
            New value for that indexed element of code.
        """
        self.__code[index] = value

    cpdef setPoint(self, int index, int value):
        """
        Mutator for point attribute.

        PARAMETERS
        ----------
        index : int
            Index of the point
        value : int
            New value for that indexed element of point.
        """
        self.__point[index] = value

    cpdef int getCodeLength(self):
        """
        Accessor for the codeLength attribute.

        RETURNS
        -------
        int
            Length of the Huffman code for this word.
        """
        return self.__codeLength

    cpdef int getPoint(self, int index):
        """
        Accessor for point attribute.

        PARAMETERS
        ----------
        index : int
            Index of the point.

        RETURNS
        -------
        int
            Value for that indexed element of point.
        """
        return self.__point[index]

    cpdef int getCode(self, int index):
        """
        Accessor for code attribute.

        PARAMETERS
        ----------
        index : int
            Index of the code.

        RETURNS
        -------
        int
            Value for that indexed element of code.
        """
        return self.__code[index]
