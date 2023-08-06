from Classification.Instance.CompositeInstance cimport CompositeInstance


cdef class GaussianModel(ValidatedModel):

    cpdef double calculateMetric(self, Instance instance, str Ci):
        pass

    cpdef str predict(self, Instance instance):
        """
        The predict method takes an Instance as an input. First it gets the size of prior distribution and loops this
        size times. Then it gets the possible class labels and and calculates metric value. At the end, it returns the
        class which has the maximum value of metric.

        PARAMETERS
        ----------
        instance : Instance
            Instance to predict.

        RETURNS
        -------
        str
            The class which has the maximum value of metric.
        """
        cdef double maxMetric, metric
        cdef str predicatedClass, Ci
        cdef int size, i
        maxMetric = -10000000
        if isinstance(instance, CompositeInstance):
            predicatedClass = instance.getPossibleClassLabels()[0]
            size = len(instance.getPossibleClassLabels())
        else:
            predicatedClass = self.priorDistribution.getMaxItem()
            size = len(self.priorDistribution)
        for i in range(size):
            if isinstance(instance, CompositeInstance):
                Ci = instance.getPossibleClassLabels()[i]
            else:
                Ci = self.priorDistribution.getItem(i)
            if self.priorDistribution.containsItem(Ci):
                metric = self.calculateMetric(instance, Ci)
                if metric > maxMetric:
                    maxMetric = metric
                    predicatedClass = Ci
        return predicatedClass