from DataStructure.CounterHashMap cimport CounterHashMap


cdef class ConfusionMatrix:

    def __init__(self, classLabels: list):
        """
        Constructor that sets the class labels list and creates new dictionary matrix

        PARAMETERS
        ----------
        classLabels : list
            list of String.
        """
        self.__classLabels = classLabels
        self.__matrix = {}

    cpdef classify(self, str actualClass, str predictedClass):
        """
        The classify method takes two Strings; actual class and predicted class as inputs. If the matrix dictionary
        contains given actual class String as a key, it then assigns the corresponding object of that key to a
        CounterHashMap, if not it creates a new CounterHashMap. Then, it puts the given predicted class String to the
        counterHashMap and also put this counterHashMap to the matrix dictionary together with the given actual class
        String.

        PARAMETERS
        ----------
        actualClass : str
            String input actual class.
        predictedClass : str
            String input predicted class.
        """
        cdef CounterHashMap counterHashMap
        if actualClass in self.__matrix:
            counterHashMap = self.__matrix[actualClass]
        else:
            counterHashMap = CounterHashMap()
        counterHashMap.put(predictedClass)
        self.__matrix[actualClass] = counterHashMap

    cpdef addConfusionMatrix(self, ConfusionMatrix confusionMatrix):
        """
        The addConfusionMatrix method takes a ConfusionMatrix as an input and loops through actual classes of that
        dictionary and initially gets one row at a time. Then it puts the current row to the matrix dictionary together
        with the actual class string.

        PARAMETERS
        ----------
        confusionMatrix : ConfusionMatrix
            ConfusionMatrix input.
        """
        cdef str actualClass
        cdef CounterHashMap rowToBeAdded, currentRow
        for actualClass in confusionMatrix.__matrix:
            rowToBeAdded = confusionMatrix.__matrix[actualClass]
            if actualClass in self.__matrix:
                currentRow = self.__matrix[actualClass]
                currentRow.add(rowToBeAdded)
                self.__matrix[actualClass] = currentRow
            else:
                self.__matrix[actualClass] = rowToBeAdded

    cpdef double sumOfElements(self):
        """
        The sumOfElements method loops through the keys in matrix dictionary and returns the summation of all the values
        of the keys. I.e: TP+TN+FP+FN.

        RETURNS
        -------
        float
            The summation of values.
        """
        cdef double result
        cdef str actualClass
        result = 0
        for actualClass in self.__matrix:
            result += self.__matrix[actualClass].sumOfCounts()
        return result

    cpdef double trace(self):
        """
        The trace method loops through the keys in matrix dictionary and if the current key contains the actual key,
        it accumulates the corresponding values. I.e: TP+TN.

        RETURNS
        -------
        float
            Summation of values.
        """
        cdef double result
        cdef str actualClass
        result = 0
        for actualClass in self.__matrix:
            if actualClass in self.__matrix[actualClass]:
                result += self.__matrix[actualClass][actualClass]
        return result

    cpdef double columnSum(self, str predictedClass):
        """
        The columnSum method takes a String predicted class as input, and loops through the keys in matrix dictionary.
        If the current key contains the predicted class String, it accumulates the corresponding values. I.e: TP+FP.

        PARAMETERS
        ----------
        predictedClass : str
            String input predicted class.

        RETURNS
        -------
        float
            Summation of values.
        """
        cdef double result
        cdef str actualClass
        result = 0
        for actualClass in self.__matrix:
            if predictedClass in self.__matrix[actualClass]:
                result += self.__matrix[actualClass][predictedClass]
        return result

    cpdef double getAccuracy(self):
        """
        The getAccuracy method returns the result of  TP+TN / TP+TN+FP+FN

        RETURNS
        -------
        list
            the result of  TP+TN / TP+TN+FP+FN
        """
        return self.trace() / self.sumOfElements()

    cpdef list precision(self):
        """
        The precision method loops through the class labels and returns the resulting Array which has the result of
        TP/FP+TP.

        RETURNS
        -------
        list
            The result of TP/FP+TP.
        """
        cdef list result
        cdef int i
        cdef str actualClass
        result = []
        for i in range(len(self.__classLabels)):
            actualClass = self.__classLabels[i]
            if actualClass in self.__matrix:
                result.append(self.__matrix[actualClass][actualClass] / self.columnSum(actualClass))
        return result

    cpdef list recall(self):
        """
        The recall method loops through the class labels and returns the resulting Array which has the result of
        TP/FN+TP.

        RETURNS
        -------
        list
            The result of TP/FN+TP.
        """
        cdef list result
        cdef int i
        cdef str actualClass
        result = []
        for i in range(len(self.__classLabels)):
            actualClass = self.__classLabels[i]
            if actualClass in self.__matrix:
                result.append(self.__matrix[actualClass][actualClass] / self.__matrix[actualClass].sumOfCounts())
        return result

    cpdef list fMeasure(self):
        """
        The fMeasure method loops through the class labels and returns the resulting Array which has the average of
        recall and precision.

        RETURNS
        -------
        list
            The average of recall and precision.
        """
        cdef list precision, recall, result
        cdef int i
        precision = self.precision()
        recall = self.recall()
        result = []
        for i in range(len(self.__classLabels)):
            result.append(2 / (1 / precision[i] + 1 / recall[i]))
        return result

    cpdef double weightedFMeasure(self):
        """
        The weightedFMeasure method loops through the class labels and returns the resulting Array which has the
        weighted average of recall and precision.

        RETURNS
        -------
        float
            The weighted average of recall and precision.
        """
        cdef double total
        cdef int i
        cdef str actualClass
        cdef list fMeasure
        fMeasure = self.fMeasure()
        total = 0
        for i in range(len(self.__classLabels)):
            actualClass = self.__classLabels[i]
            total += fMeasure[i] * self.__matrix[actualClass].sumOfCounts()
        return total / self.sumOfElements()
