from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.LinearPerceptronModel cimport LinearPerceptronModel
from Classification.Parameter.Parameter cimport Parameter


cdef class LinearPerceptron(Classifier):

    cpdef train(self, InstanceList trainSet, Parameter parameters):
        """
        Training algorithm for the linear perceptron algorithm. 20 percent of the data is separated as cross-validation
        data used for selecting the best weights. 80 percent of the data is used for training the linear perceptron with
        gradient descent.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm
        parameters : LinearPerceptronParameter
            Parameters of the linear perceptron.
        """
        cdef Partition partition
        partition = Partition(trainSet, parameters.getCrossValidationRatio(), parameters.getSeed(), True)
        self.model = LinearPerceptronModel(partition.get(1), partition.get(0), parameters)
