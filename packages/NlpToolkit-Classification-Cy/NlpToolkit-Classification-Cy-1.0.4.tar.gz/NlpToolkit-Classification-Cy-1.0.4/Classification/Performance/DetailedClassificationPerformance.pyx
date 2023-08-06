cdef class DetailedClassificationPerformance(ClassificationPerformance):

    def __init__(self, confusionMatrix: ConfusionMatrix):
        """
        A constructor that  sets the accuracy and errorRate as 1 - accuracy via given ConfusionMatrix and also sets the
        confusionMatrix.

        PARAMETERS
        ----------
        confusionMatrix : ConfusionMatrix
            ConfusionMatrix input.
        """
        super().__init__(confusionMatrix.getAccuracy())
        self.__confusionMatrix = confusionMatrix

    cpdef ConfusionMatrix getConfusionMatrix(self):
        """
        Accessor for the confusionMatrix.

        RETURNS
        -------
        ConfusionMatrix
            ConfusionMatrix.
        """
        return self.__confusionMatrix
