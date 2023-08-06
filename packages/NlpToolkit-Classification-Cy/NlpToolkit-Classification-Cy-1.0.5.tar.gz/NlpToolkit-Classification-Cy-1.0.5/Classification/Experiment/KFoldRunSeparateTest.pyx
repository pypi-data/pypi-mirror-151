from Sampling.KFoldCrossValidation cimport KFoldCrossValidation
from Classification.InstanceList.Partition cimport Partition


cdef class KFoldRunSeparateTest(KFoldRun):

    def __init__(self, K: int):
        """
        Constructor for KFoldRunSeparateTest class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        super().__init__(K)

    cpdef runExperimentSeparate(self, Classifier classifier, Parameter parameter, ExperimentPerformance experimentPerformance,
                      CrossValidation crossValidation, InstanceList testSet):
        cdef int i
        cdef InstanceList trainSet
        for i in range(self.K):
            trainSet = InstanceList(crossValidation.getTrainFold(i))
            classifier.train(trainSet, parameter)
            experimentPerformance.add(classifier.test(testSet))

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        """
        Execute K-fold cross-validation with separate test set with the given classifier on the given data set using the
        given parameters.

        PARAMETERS
        ----------
        experiment : Experiment
            Experiment to be run.

        RETURNS
        -------
        ExperimentPerformance
            An ExperimentPerformance instance.
        """
        cdef ExperimentPerformance result
        cdef InstanceList instanceList
        cdef Partition partition
        cdef KFoldCrossValidation crossValidation
        result = ExperimentPerformance()
        instanceList = experiment.getDataSet().getInstanceList()
        partition = Partition(instanceList, 0.25, experiment.getParameter().getSeed(), True)
        crossValidation = KFoldCrossValidation(partition.get(1).getInstances(), self.K, experiment.getParameter().
                                               getSeed())
        self.runExperimentSeparate(experiment.getClassifier(), experiment.getParameter(), result, crossValidation,
                           partition.get(0))
        return result
