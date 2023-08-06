from DependencyParser.DependencyRelation cimport DependencyRelation
from DependencyParser.ParserEvaluationScore cimport ParserEvaluationScore

cdef class UniversalDependencyRelation(DependencyRelation):

    cdef object __universalDependencyType
    cpdef ParserEvaluationScore compareRelations(self, UniversalDependencyRelation relation)
