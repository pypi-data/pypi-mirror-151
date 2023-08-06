cdef class UniversalDependencyTreeBankFeatures:

    cdef dict featureList

    cpdef str getFeatureValue(self, str feature)

    cpdef bint featureExists(self, str feature)
