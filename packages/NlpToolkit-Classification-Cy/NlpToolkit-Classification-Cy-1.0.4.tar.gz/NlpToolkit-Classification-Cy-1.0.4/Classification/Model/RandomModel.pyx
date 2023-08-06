import random
from Classification.Instance.CompositeInstance cimport CompositeInstance


cdef class RandomModel(Model):

    def __init__(self, classLabels: list, seed: int):
        """
        A constructor that sets the class labels.

        PARAMETERS
        ----------
        classLabels : list
            A List of class labels.
        seed: int
            Seed of the random function
        """
        self.__classLabels = classLabels
        random.seed(seed)

    cpdef str predict(self, Instance instance):
        """
        The predict method gets an Instance as an input and retrieves the possible class labels as an ArrayList. Then
        selects a random number as an index and returns the class label at this selected index.

        PARAMETERS
        ----------
        instance : Instance
            Instance to make prediction.

        RETURNS
        -------
        str
            The class label at the randomly selected index.
        """
        cdef list possibleClassLabels
        cdef int size, index
        if isinstance(instance, CompositeInstance):
            possibleClassLabels = instance.getPossibleClassLabels()
            size = len(possibleClassLabels)
            index = random.randint(0, size)
            return possibleClassLabels[index]
        else:
            size = len(self.__classLabels)
            index = random.randrange(size)
            return self.__classLabels[index]

    cpdef dict predictProbability(self, Instance instance):
        result = {}
        for classLabel in self.__classLabels:
            result[classLabel] = 1.0 / len(self.__classLabels)
        return result
