from Classification.Instance.Instance cimport Instance


cdef class CompositeInstance(Instance):

    cdef list __possibleClassLabels

    cpdef list getPossibleClassLabels(self)
    cpdef setPossibleClassLabels(self, list possibleClassLabels)
