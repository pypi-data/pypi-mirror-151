cdef class WordToVecParameter:

    def __init__(self):
        """
        Empty constructor for Word2Vec parameter
        """
        self.__alpha = 0.025
        self.__cbow = True
        self.__hierarchicalSoftMax = False
        self.__layerSize = 100
        self.__negativeSamplingSize = 5
        self.__numberOfIterations = 3
        self.__window = 5
        self.__seed = 1

    cpdef int getLayerSize(self):
        """
        Accessor for layerSize attribute.

        RETURNS
        -------
        int
            Size of the word vectors.
        """
        return self.__layerSize

    cpdef bint isCbow(self):
        """
        Accessor for CBow attribute.

        RETURNS
        -------
        bool
            True is CBow will be applied, false otherwise.
        """
        return self.__cbow

    cpdef double getAlpha(self):
        """
        Accessor for the alpha attribute.

        RETURNS
        -------
        float
            Current learning rate alpha.
        """
        return self.__alpha

    cpdef int getWindow(self):
        """
        Accessor for the window size attribute.

        RETURNS
        -------
        int
            Current window size.
        """
        return self.__window

    cpdef bint isHierarchicalSoftMax(self):
        """
        Accessor for the hierarchicalSoftMax attribute.

        RETURNS
        -------
        bool
            If hierarchical softmax will be applied, returns true; false otherwise.
        """
        return self.__hierarchicalSoftMax

    cpdef int getNegativeSamplingSize(self):
        """
        Accessor for the negativeSamplingSize attribute.

        RETURNS
        -------
        int
            Number of negative samples that will be withdrawn.
        """
        return self.__negativeSamplingSize

    cpdef int getNumberOfIterations(self):
        """
        Accessor for the numberOfIterations attribute.

        RETURNS
        -------
        int
            Number of epochs to train the network.
        """
        return self.__numberOfIterations

    cpdef int getSeed(self):
        """
        Accessor for the seed attribute.

        RETURNS
        -------
        int
            Seed to train the network.
        """
        return self.__seed

    cpdef setLayerSize(self, int layerSize):
        """
        Mutator for the layerSize attribute.

        PARAMETERS
        ----------
        layerSize : int
            New size of the word vectors.
        """
        self.__layerSize = layerSize

    cpdef setCbow(self, bint cbow):
        """
        Mutator for cBow attribute

        PARAMETERS
        ----------
        cbow : bool
            True if CBow applied; false if SkipGram applied.
        """
        self.__cbow = cbow

    cpdef setAlpha(self, double alpha):
        """
        Mutator for alpha attribute

        PARAMETERS
        ----------
        alpha : float
            New learning rate.
        """
        self.__alpha = alpha

    cpdef setWindow(self, int window):
        """
        Mutator for the window size attribute.

        PARAMETERS
        ----------
        window : int
            New window size.
        """
        self.__window = window

    cpdef setHierarchialSoftMax(self, bint hierarchicalSoftMax):
        """
        Mutator for the hierarchicalSoftMax attribute.

        PARAMETERS
        ----------
        hierarchicalSoftMax : bool
            True is hierarchical softMax applied; false otherwise.
        """
        self.__hierarchicalSoftMax = hierarchicalSoftMax

    cpdef setNegativeSamplingSize(self, int negativeSamplingSize):
        """
        Mutator for the negativeSamplingSize attribute.

        PARAMETERS
        ----------
        negativeSamplingSize : int
            New number of negative instances that will be withdrawn.
        """
        self.__negativeSamplingSize = negativeSamplingSize

    cpdef setNumberOfIterations(self, int numberOfIterations):
        """
        Mutator for the numberOfIterations attribute.

        PARAMETERS
        ----------
        numberOfIterations : int
            New number of iterations.
        """
        self.__numberOfIterations = numberOfIterations

    cpdef setSeed(self, int seed):
        """
        Mutator for the numberOfIterations attribute.

        PARAMETERS
        ----------
        seed : int
            New seed.
        """
        self.__seed = seed
