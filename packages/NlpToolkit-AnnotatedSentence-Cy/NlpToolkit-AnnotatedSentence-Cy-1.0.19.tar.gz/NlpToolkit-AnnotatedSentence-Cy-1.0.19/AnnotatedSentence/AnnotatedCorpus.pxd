from Corpus.Corpus cimport Corpus
from DependencyParser.ParserEvaluationScore cimport ParserEvaluationScore

cdef class AnnotatedCorpus(Corpus):

    cpdef ParserEvaluationScore compareParses(self, AnnotatedCorpus corpus)
    cpdef exportUniversalDependencyFormat(self, str outputFileName, str path=*)
    cpdef checkMorphologicalAnalysis(self)
    cpdef checkNer(self)
    cpdef checkShallowParse(self)
    cpdef checkSemantic(self)
