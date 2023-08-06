from Classification.Parameter.Parameter cimport Parameter


cdef class LinearPerceptronParameter(Parameter):

    cdef double learningRate
    cdef double etaDecrease
    cdef double crossValidationRatio
    cdef int __epoch

    cpdef double getLearningRate(self)
    cpdef double getEtaDecrease(self)
    cpdef double getCrossValidationRatio(self)
    cpdef int getEpoch(self)
