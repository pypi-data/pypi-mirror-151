from Math.DiscreteDistribution cimport DiscreteDistribution
from Classification.Instance.Instance cimport Instance
from Classification.Model.ValidatedModel cimport ValidatedModel


cdef class GaussianModel(ValidatedModel):

    cdef DiscreteDistribution priorDistribution

    cpdef double calculateMetric(self, Instance instance, str Ci)
    cpdef str predict(self, Instance instance)