from Sampling.StratifiedKFoldCrossValidation cimport StratifiedKFoldCrossValidation
from Classification.InstanceList.Partition cimport Partition
from Classification.InstanceList.InstanceList cimport InstanceList


cdef class StratifiedKFoldRunSeparateTest(KFoldRunSeparateTest):

    def __init__(self, K: int):
        """
        Constructor for StratifiedKFoldRunSeparateTest class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        super().__init__(K)

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        """
        Execute Stratified K-fold cross-validation with the given classifier on the given data set using the given
        parameters.

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
        cdef StratifiedKFoldCrossValidation crossValidation
        result = ExperimentPerformance()
        instanceList = experiment.getDataSet().getInstanceList()
        partition = Partition(instanceList, 0.25, experiment.getParameter().getSeed(), True)
        crossValidation = StratifiedKFoldCrossValidation(Partition(partition.get(1)).getLists(), self.K,
                                                         experiment.getParameter().getSeed())
        self.runExperimentSeparate(experiment.getClassifier(), experiment.getParameter(), result, crossValidation,
                           partition.get(0))
        return result
