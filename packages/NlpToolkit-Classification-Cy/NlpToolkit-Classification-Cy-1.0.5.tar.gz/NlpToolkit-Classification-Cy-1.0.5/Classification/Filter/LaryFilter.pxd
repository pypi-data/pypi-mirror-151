from Classification.Filter.FeatureFilter cimport FeatureFilter
from Classification.Instance.Instance cimport Instance


cdef class LaryFilter(FeatureFilter):

    cdef list attributeDistributions

    cpdef removeDiscreteAttributesFromInstance(self, Instance instance, int size)
    cpdef removeDiscreteAttributesFromDataDefinition(self, int size)
