from Sampling.KFoldCrossValidation cimport KFoldCrossValidation
from Classification.InstanceList.InstanceList cimport InstanceList


cdef class KFoldRun(MultipleRun):

    def __init__(self, K: int):
        """
        Constructor for KFoldRun class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        self.K = K

    cpdef runExperiment(self, Classifier classifier, Parameter parameter, ExperimentPerformance experimentPerformance,
                      CrossValidation crossValidation):
        cdef int i
        cdef InstanceList trainSet, testSet
        for i in range(self.K):
            trainSet = InstanceList(crossValidation.getTrainFold(i))
            testSet = InstanceList(crossValidation.getTestFold(i))
            classifier.train(trainSet, parameter)
            experimentPerformance.add(classifier.test(testSet))

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        """
        Execute K-fold cross-validation with the given classifier on the given data set using the given parameters.

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
        cdef KFoldCrossValidation crossValidation
        result = ExperimentPerformance()
        crossValidation = KFoldCrossValidation(experiment.getDataSet().getInstances(), self.K, experiment.getParameter()
                                               .getSeed())
        self.runExperiment(experiment.getClassifier(), experiment.getParameter(), result, crossValidation)
        return result
