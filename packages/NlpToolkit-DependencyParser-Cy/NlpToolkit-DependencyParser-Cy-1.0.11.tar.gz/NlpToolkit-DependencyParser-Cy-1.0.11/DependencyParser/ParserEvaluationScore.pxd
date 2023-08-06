cdef class ParserEvaluationScore:

    cdef float LAS
    cdef float UAS
    cdef float LS
    cdef int wordCount

    cpdef float getLS(self)
    cpdef float getLAS(self)
    cpdef float getUAS(self)
    cpdef int getWordCount(self)
    cpdef add(self, ParserEvaluationScore parserEvaluationScore)
