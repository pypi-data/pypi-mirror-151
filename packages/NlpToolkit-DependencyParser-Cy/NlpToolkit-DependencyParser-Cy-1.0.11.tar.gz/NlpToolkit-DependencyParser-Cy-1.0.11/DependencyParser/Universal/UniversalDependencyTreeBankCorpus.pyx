from Corpus.Corpus cimport Corpus
from DataStructure.CounterHashMap cimport CounterHashMap

from DependencyParser.ParserEvaluationScore cimport ParserEvaluationScore
from DependencyParser.Universal.UniversalDependencyTreeBankSentence cimport UniversalDependencyTreeBankSentence

cdef class UniversalDependencyTreeBankCorpus(Corpus):

    def __init__(self, fileName: str):
        cdef list lines
        cdef str line, sentence
        self.sentences = []
        self.paragraphs = []
        self.wordList = CounterHashMap()
        sentence = ""
        file = open(fileName, "r")
        lines = file.readlines()
        file.close()
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                self.addSentence(UniversalDependencyTreeBankSentence(sentence))
                sentence = ""
            else:
                sentence = sentence + line + "\n"

    cpdef ParserEvaluationScore compareParses(self, UniversalDependencyTreeBankCorpus corpus):
        score = ParserEvaluationScore()
        for i in range(len(self.sentences)):
            score.add(self.sentences[i].compareParses(corpus.getSentence(i)))
        return score
