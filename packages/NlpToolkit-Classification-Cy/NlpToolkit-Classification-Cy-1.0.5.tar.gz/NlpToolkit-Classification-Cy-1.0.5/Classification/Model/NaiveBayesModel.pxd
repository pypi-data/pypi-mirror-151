from Classification.Instance.Instance cimport Instance
from Classification.Model.GaussianModel cimport GaussianModel


cdef class NaiveBayesModel(GaussianModel):

    cdef dict __classMeans
    cdef dict __classDeviations
    cdef dict __classAttributeDistributions

    cpdef initForContinuous(self, dict classMeans, dict classDeviations)
    cpdef initForDiscrete(self, dict classAttributeDistributions)
    cpdef double calculateMetric(self, Instance instance, str Ci)
    cpdef double __logLikelihoodContinuous(self, str classLabel, Instance instance)
    cpdef double __logLikelihoodDiscrete(self, str classLabel, Instance instance)
