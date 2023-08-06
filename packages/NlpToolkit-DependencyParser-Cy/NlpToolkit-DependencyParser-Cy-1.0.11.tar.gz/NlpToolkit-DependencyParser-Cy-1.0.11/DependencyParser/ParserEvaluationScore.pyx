cdef class ParserEvaluationScore:

    def __init__(self, float LAS = 0.0, float UAS = 0.0, float LS = 0.0, int wordCount = 0):
        self.LAS = LAS
        self.UAS = UAS
        self.LS = LS
        self.wordCount = wordCount

    cpdef float getLS(self):
        return self.LS

    cpdef float getLAS(self):
        return self.LAS

    cpdef float getUAS(self):
        return self.UAS

    cpdef int getWordCount(self):
        return self.wordCount

    cpdef add(self, ParserEvaluationScore parserEvaluationScore):
        self.LAS = (self.LAS * self.wordCount + parserEvaluationScore.LAS * parserEvaluationScore.wordCount) / \
                   (self.wordCount + parserEvaluationScore.wordCount)
        self.UAS = (self.UAS * self.wordCount + parserEvaluationScore.UAS * parserEvaluationScore.wordCount) / \
                   (self.wordCount + parserEvaluationScore.wordCount)
        self.LS = (self.LS * self.wordCount + parserEvaluationScore.LS * parserEvaluationScore.wordCount) / \
                  (self.wordCount + parserEvaluationScore.wordCount)
        self.wordCount += parserEvaluationScore.wordCount
