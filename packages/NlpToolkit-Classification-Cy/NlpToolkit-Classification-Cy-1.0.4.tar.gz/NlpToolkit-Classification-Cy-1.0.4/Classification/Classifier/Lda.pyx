from Math.Matrix cimport Matrix
from Math.Vector cimport Vector
from Math.DiscreteDistribution cimport DiscreteDistribution

from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.LdaModel cimport LdaModel
from Classification.Parameter.Parameter cimport Parameter

import math


cdef class Lda(Classifier):

    cpdef train(self, InstanceList trainSet, Parameter parameters):
        """
        Training algorithm for the linear discriminant analysis classifier (Introduction to Machine Learning, Alpaydin,
        2015).

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        parameters : Parameter
            Parameter of the Lda algorithm.
        """
        cdef dict w0, s
        cdef DiscreteDistribution priorDistribution
        cdef Partition classLists
        cdef Matrix covariance, classCovariance
        cdef int i
        cdef Vector averageVector, wi
        cdef str Ci
        cdef double w0i
        w0 = {}
        w = {}
        priorDistribution = trainSet.classDistribution()
        classLists = Partition(trainSet)
        covariance = Matrix(trainSet.get(0).continuousAttributeSize(), trainSet.get(0).continuousAttributeSize())
        for i in range(classLists.size()):
            averageVector = Vector(classLists.get(i).continuousAverage())
            classCovariance = classLists.get(i).covariance(averageVector)
            classCovariance.multiplyWithConstant(classLists.get(i).size() - 1)
            covariance.add(classCovariance)
        covariance.divideByConstant(trainSet.size() - classLists.size())
        covariance.inverse()
        for i in range(classLists.size()):
            Ci = classLists.get(i).getClassLabel()
            averageVector = Vector(classLists.get(i).continuousAverage())
            wi = covariance.multiplyWithVectorFromRight(averageVector)
            w[Ci] = wi
            w0i = -0.5 * wi.dotProduct(averageVector) + math.log(priorDistribution.getProbability(Ci))
            w0[Ci] = w0i
        self.model = LdaModel(priorDistribution, w, w0)
