from Sampling.StratifiedKFoldCrossValidation cimport StratifiedKFoldCrossValidation
from Classification.Experiment.Experiment cimport Experiment
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Performance.Performance cimport Performance


cdef class StratifiedSingleRunWithK:

    cdef int __K

    def __init__(self, K: int):
        """
        Constructor for StratifiedSingleRunWithK class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        self.__K = K

    cpdef Performance execute(self, Experiment experiment):
        """
        Execute Stratified Single K-fold cross-validation with the given classifier on the given data set using the
        given parameters.

        PARAMETERS
        ----------
        experiment : Experiment
            Experiment to be run.

        RETURNS
        -------
        Performance
            A Performance instance.
        """
        cdef StratifiedKFoldCrossValidation crossValidation
        cdef InstanceList trainSet, testSet
        crossValidation = StratifiedKFoldCrossValidation(experiment.getDataSet().getClassInstances(), self.__K,
                                                         experiment.getParameter().getSeed())
        trainSet = InstanceList(crossValidation.getTrainFold(0))
        testSet = InstanceList(crossValidation.getTestFold(0))
        return experiment.getClassifier().singleRun(experiment.getParameter(), trainSet, testSet)
