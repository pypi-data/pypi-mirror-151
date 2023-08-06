from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.AutoEncoderModel cimport AutoEncoderModel
from Classification.Parameter.Parameter cimport Parameter
from Classification.Performance.Performance cimport Performance


cdef class AutoEncoder(Classifier):

    cpdef train(self, InstanceList trainSet, Parameter parameters):
        """
        Training algorithm for auto encoders. An auto encoder is a neural network which attempts to replicate its input
        at its output.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        parameters : MultiLayerPerceptronParameter
            Parameters of the auto encoder.
        """
        cdef Partition partition
        partition = Partition(trainSet, 0.2, parameters.getSeed(), True)
        self.model = AutoEncoderModel(partition.get(1), partition.get(0), parameters)

    cpdef Performance test(self, InstanceList testSet):
        """
        A performance test for an auto encoder with the given test set.

        PARAMETERS
        ----------
        testSet : InstanceList
            Test data (list of instances) to be tested.

        RETURNS
        -------
        Performance
            Error rate.
        """
        if isinstance(self.model, AutoEncoderModel):
            return self.model.testAutoEncoder(testSet)
