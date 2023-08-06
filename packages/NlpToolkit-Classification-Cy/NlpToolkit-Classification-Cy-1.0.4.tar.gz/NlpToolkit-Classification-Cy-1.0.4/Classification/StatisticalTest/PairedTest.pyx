from Classification.StatisticalTest.StatisticalTestResultType import StatisticalTestResultType


cdef class PairedTest(object):

    cpdef StatisticalTestResult compare(self, ExperimentPerformance classifier1, ExperimentPerformance classifier2):
        pass

    cpdef int compareWithAlpha(self, ExperimentPerformance classifier1, ExperimentPerformance classifier2, double alpha):
        cdef StatisticalTestResult testResult1, testResult2
        testResult1 = self.compare(classifier1, classifier2)
        testResult2 = self.compare(classifier2, classifier1)
        testResultType1 = testResult1.oneTailed(alpha)
        testResultType2 = testResult2.oneTailed(alpha)
        if testResultType1 is StatisticalTestResultType.REJECT:
            return 1
        else:
            if testResultType2 is StatisticalTestResultType.REJECT:
                return -1
            else:
                return 0
