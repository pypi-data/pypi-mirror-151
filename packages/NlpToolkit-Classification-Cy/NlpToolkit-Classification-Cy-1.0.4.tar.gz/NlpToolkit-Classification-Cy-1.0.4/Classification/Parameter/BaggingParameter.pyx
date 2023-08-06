from Classification.Parameter.Parameter cimport Parameter


cdef class BaggingParameter(Parameter):

    def __init__(self, seed: int, ensembleSize: int):
        """
        Parameters of the bagging trees algorithm.

        PARAMETERS
        ----------
        seed : int
            Seed is used for random number generation.
        ensembleSize : int
            The number of trees in the bagged forest.
        """
        super().__init__(seed)
        self.ensembleSize = ensembleSize

    cpdef int getEnsembleSize(self):
        """
        Accessor for the ensemble size.

        RETURNS
        -------
        int
            The ensemble size.
        """
        return self.ensembleSize
