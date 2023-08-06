from Sampling.StratifiedKFoldCrossValidation cimport StratifiedKFoldCrossValidation
from Classification.Experiment.Experiment cimport Experiment
from Classification.Experiment.StratifiedKFoldRunSeparateTest cimport StratifiedKFoldRunSeparateTest
from Classification.InstanceList.Partition cimport Partition
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance


cdef class StratifiedMxKFoldRunSeparateTest(StratifiedKFoldRunSeparateTest):

    cdef int M

    def __init__(self, M: int, K: int):
        """
        Constructor for StratifiedMxKFoldRunSeparateTest class. Basically sets K parameter of the K-fold
        cross-validation and M for the number of times.

        PARAMETERS
        ----------
        M : int
            number of cross-validation times.
        K : int
            K of the K-fold cross-validation.
        """
        super().__init__(K)
        self.M = M

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        cdef ExperimentPerformance result
        cdef int j
        cdef InstanceList instanceList
        cdef Partition partition
        cdef StratifiedKFoldCrossValidation crossValidation
        result = ExperimentPerformance()
        for j in range(self.M):
            instanceList = experiment.getDataSet().getInstanceList()
            partition = Partition(instanceList, 0.25, experiment.getParameter().getSeed(), True)
            crossValidation = StratifiedKFoldCrossValidation(Partition(partition.get(1)).getLists(), self.K,
                                                             experiment.getParameter().getSeed())
            self.runExperimentSeparate(experiment.getClassifier(), experiment.getParameter(), result, crossValidation,
                               partition.get(0))
        return result
