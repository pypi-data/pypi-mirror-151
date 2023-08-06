from Classification.Attribute.Attribute cimport Attribute
from Classification.Instance.Instance cimport Instance


cdef class DecisionCondition(object):

    cdef int __attributeIndex
    cdef str __comparison
    cdef Attribute __value

    cpdef satisfy(self, Instance instance)