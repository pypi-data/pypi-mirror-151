from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.KMeansModel cimport KMeansModel
from Math.DiscreteDistribution cimport DiscreteDistribution
from Classification.Parameter.Parameter cimport Parameter


cdef class KMeans(Classifier):

    cpdef train(self, InstanceList trainSet, Parameter parameters):
        cdef DiscreteDistribution priorDistribution
        cdef InstanceList classMeans
        cdef Partition classLists
        cdef int i
        priorDistribution = trainSet.classDistribution()
        classMeans = InstanceList()
        classLists = Partition(trainSet)
        for i in range(classLists.size()):
            classMeans.add(classLists.get(i).average())
        self.model = KMeansModel(priorDistribution, classMeans, parameters.getDistanceMetric())
