from Math.DiscreteDistribution cimport DiscreteDistribution
from Math.Vector cimport Vector

from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.NaiveBayesModel cimport NaiveBayesModel
from Classification.Parameter.Parameter cimport Parameter


cdef class NaiveBayes(Classifier):

    cpdef trainContinuousVersion(self, DiscreteDistribution priorDistribution, Partition classLists):
        """
        Training algorithm for Naive Bayes algorithm with a continuous data set.

        PARAMETERS
        ----------
        priorDistribution : DiscreteDistribution
            Probability distribution of classes P(C_i)
        classLists : Partition
            Instances are divided into K lists, where each list contains only instances from a single class
        """
        cdef dict classMeans, classDeviations
        cdef int i
        cdef str classLabel
        cdef Vector averageVector, standardDeviationVector
        classMeans = {}
        classDeviations = {}
        for i in range(classLists.size()):
            classLabel = classLists.get(i).getClassLabel()
            averageVector = classLists.get(i).average().toVector()
            classMeans[classLabel] = averageVector
            standardDeviationVector = classLists.get(i).standardDeviation().toVector()
            classDeviations[classLabel] = standardDeviationVector
        self.model = NaiveBayesModel(priorDistribution)
        if isinstance(self.model, NaiveBayesModel):
            self.model.initForContinuous(classMeans, classDeviations)

    cpdef trainDiscreteVersion(self, DiscreteDistribution priorDistribution, Partition classLists):
        """
        Training algorithm for Naive Bayes algorithm with a discrete data set.

        PARAMETERS
        ----------
        priorDistribution : DiscreteDistribution
            Probability distribution of classes P(C_i)
        classLists : Partition
            Instances are divided into K lists, where each list contains only instances from a single class
        """
        cdef dict classAttributeDistributions
        cdef int i
        classAttributeDistributions = {}
        for i in range(classLists.size()):
            classAttributeDistributions[classLists.get(i).getClassLabel()] = \
                classLists.get(i).allAttributesDistribution()
        self.model = NaiveBayesModel(priorDistribution)
        if isinstance(self.model, NaiveBayesModel):
            self.model.initForDiscrete(classAttributeDistributions)

    cpdef train(self, InstanceList trainSet, Parameter parameters):
        """
        Training algorithm for Naive Bayes algorithm. It basically calls trainContinuousVersion for continuous data
        sets, trainDiscreteVersion for discrete data sets.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm
        """
        cdef DiscreteDistribution priorDistribution
        cdef Partition classLists
        priorDistribution = trainSet.classDistribution()
        classLists = Partition(trainSet)
        if isinstance(classLists.get(0).get(0).getAttribute(0), DiscreteAttribute):
            self.trainDiscreteVersion(priorDistribution, classLists)
        else:
            self.trainContinuousVersion(priorDistribution, classLists)
