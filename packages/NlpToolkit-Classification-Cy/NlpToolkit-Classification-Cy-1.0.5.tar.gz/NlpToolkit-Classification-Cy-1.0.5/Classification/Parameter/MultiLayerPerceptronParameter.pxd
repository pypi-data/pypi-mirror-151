from Classification.Parameter.LinearPerceptronParameter cimport LinearPerceptronParameter


cdef class MultiLayerPerceptronParameter(LinearPerceptronParameter):

    cdef int __hiddenNodes
    cdef object __activationFunction

    cpdef int getHiddenNodes(self)
    cpdef object getActivationFunction(self)
