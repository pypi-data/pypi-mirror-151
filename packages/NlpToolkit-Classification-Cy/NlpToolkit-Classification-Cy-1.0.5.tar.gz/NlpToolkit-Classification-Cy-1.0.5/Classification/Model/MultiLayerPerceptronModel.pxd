from Math.Matrix cimport Matrix
from Classification.Model.LinearPerceptronModel cimport LinearPerceptronModel


cdef class MultiLayerPerceptronModel(LinearPerceptronModel):

    cdef Matrix __V
    cdef object __activationFunction

    cpdef __allocateWeights(self, int H, int seed)
    cpdef calculateOutput(self)
