from Math.DiscreteDistribution cimport DiscreteDistribution


cdef class KMeansModel(GaussianModel):

    def __init__(self, priorDistribution: DiscreteDistribution, classMeans: InstanceList,
                 distanceMetric: DistanceMetric):
        """
        The constructor that sets the classMeans, priorDistribution and distanceMetric according to given inputs.

        PARAMETERS
        ----------
        priorDistribution : DiscreteDistribution
            DiscreteDistribution input.
        classMeans : InstanceList
            InstanceList of class means.
        distanceMetric : DistanceMetric
            DistanceMetric input.
        """
        self.__classMeans = classMeans
        self.priorDistribution = priorDistribution
        self.__distanceMetric = distanceMetric

    cpdef double calculateMetric(self, Instance instance, str Ci):
        """
        The calculateMetric method takes an {@link Instance} and a String as inputs. It loops through the class means,
        if the corresponding class label is same as the given String it returns the negated distance between given
        instance and the current item of class means. Otherwise it returns the smallest negative number.

        PARAMETERS
        ----------
        instance : Instance
            Instance input.
        Ci : str
            String input.

        RETURNS
        -------
        float
            The negated distance between given instance and the current item of class means.
        """
        cdef int i
        for i in range(self.__classMeans.size()):
            if self.__classMeans.get(i).getClassLabel() == Ci:
                return -self.__distanceMetric.distance(instance, self.__classMeans.get(i))
        return -1000000
