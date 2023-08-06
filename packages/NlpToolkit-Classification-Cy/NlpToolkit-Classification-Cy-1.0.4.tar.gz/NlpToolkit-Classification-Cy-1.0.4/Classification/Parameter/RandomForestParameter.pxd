from Classification.Parameter.BaggingParameter cimport BaggingParameter


cdef class RandomForestParameter(BaggingParameter):

    cdef int __attributeSubsetSize

    cpdef int getAttributeSubsetSize(self)
