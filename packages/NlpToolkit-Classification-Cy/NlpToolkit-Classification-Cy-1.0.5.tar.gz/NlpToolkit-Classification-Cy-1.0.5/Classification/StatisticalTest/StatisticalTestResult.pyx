from Classification.StatisticalTest.StatisticalTestNotApplicable import StatisticalTestNotApplicable
from Classification.StatisticalTest.StatisticalTestResultType import StatisticalTestResultType


cdef class StatisticalTestResult(object):

    def __init__(self, pValue: float, onlyTwoTailed: bool):
        self.__pValue = pValue
        self.__onlyTwoTailed = onlyTwoTailed

    cpdef object oneTailed(self, double alpha):
        if self.__onlyTwoTailed:
            raise StatisticalTestNotApplicable("One tailed option is not available for this test. The distribution is "
                                               "one tailed distribution.")
        if self.__pValue < alpha:
            return StatisticalTestResultType.REJECT
        else:
            return StatisticalTestResultType.FAILED_TO_REJECT

    cpdef object twoTailed(self, double alpha):
        if self.__onlyTwoTailed:
            if self.__pValue < alpha:
                return StatisticalTestResultType.REJECT
            else:
                return StatisticalTestResultType.FAILED_TO_REJECT
        else:
            if self.__pValue < alpha / 2 or self.__pValue > 1 - alpha / 2:
                return StatisticalTestResultType.REJECT

    cpdef double getPValue(self):
        return self.__pValue
