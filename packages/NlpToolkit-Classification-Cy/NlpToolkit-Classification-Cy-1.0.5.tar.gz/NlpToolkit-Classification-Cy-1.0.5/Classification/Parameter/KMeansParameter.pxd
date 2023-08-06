from Classification.DistanceMetric.DistanceMetric cimport DistanceMetric
from Classification.Parameter.Parameter cimport Parameter


cdef class KMeansParameter(Parameter):

    cdef DistanceMetric distanceMetric

    cpdef DistanceMetric getDistanceMetric(self)

