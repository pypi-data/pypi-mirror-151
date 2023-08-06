from Math.Vector cimport Vector
from Math.Matrix cimport Matrix
from Math.DiscreteDistribution cimport DiscreteDistribution
from copy import deepcopy

from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.QdaModel cimport QdaModel
from Classification.Parameter.Parameter cimport Parameter

import math


cdef class Qda(Classifier):

    cpdef train(self, InstanceList trainSet, Parameter parameters):
        """
        Training algorithm for the quadratic discriminant analysis classifier (Introduction to Machine Learning,
        Alpaydin, 2015).

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        """
        cdef dict w0, w, W
        cdef Partition classLists
        cdef DiscreteDistribution priorDistribution
        cdef int i
        cdef str Ci
        cdef Vector averageVector, wi
        cdef Matrix classCovariance, Wi
        cdef double determinant, w0i
        w0 = {}
        w = {}
        W = {}
        classLists = Partition(trainSet)
        priorDistribution = trainSet.classDistribution()
        for i in range(classLists.size()):
            Ci = classLists.get(i).getClassLabel()
            averageVector = Vector(classLists.get(i).continuousAverage())
            classCovariance = classLists.get(i).covariance(averageVector)
            determinant = classCovariance.determinant()
            classCovariance.inverse()
            Wi = deepcopy(classCovariance)
            Wi.multiplyWithConstant(-0.5)
            W[Ci] = Wi
            wi = classCovariance.multiplyWithVectorFromLeft(averageVector)
            w[Ci] = wi
            w0i = -0.5 * (wi.dotProduct(averageVector) + math.log(determinant)) + math.log(priorDistribution.
                                                                                           getProbability(Ci))
            w0[Ci] = w0i
        self.model = QdaModel(priorDistribution, W, w, w0)
