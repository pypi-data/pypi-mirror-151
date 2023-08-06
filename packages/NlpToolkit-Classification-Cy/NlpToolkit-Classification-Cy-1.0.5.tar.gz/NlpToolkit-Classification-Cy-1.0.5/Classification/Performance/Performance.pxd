cdef class Performance(object):

    cdef double errorRate

    cpdef double getErrorRate(self)
