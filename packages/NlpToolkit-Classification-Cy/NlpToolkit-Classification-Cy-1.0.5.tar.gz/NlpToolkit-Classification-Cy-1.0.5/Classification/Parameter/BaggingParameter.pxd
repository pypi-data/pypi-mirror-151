from Classification.Parameter.Parameter cimport Parameter


cdef class BaggingParameter(Parameter):

    cdef int ensembleSize

    cpdef int getEnsembleSize(self)
