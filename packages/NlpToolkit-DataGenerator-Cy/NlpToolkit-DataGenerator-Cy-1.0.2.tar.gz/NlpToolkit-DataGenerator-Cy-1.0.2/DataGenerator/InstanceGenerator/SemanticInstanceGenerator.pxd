from Classification.Instance.Instance cimport Instance
from Corpus.Sentence cimport Sentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer cimport FsmMorphologicalAnalyzer
from WordNet.WordNet cimport WordNet
from DataGenerator.InstanceGenerator.SimpleWindowInstanceGenerator cimport SimpleWindowInstanceGenerator


cdef class SemanticInstanceGenerator(SimpleWindowInstanceGenerator):

    cdef FsmMorphologicalAnalyzer __fsm
    cdef WordNet __wordNet

    cpdef addAttributesForWords(self, Instance current, Sentence sentence, int wordIndex)
    cpdef addAttributesForEmptyWords(self, Instance current, str emptyWord)
    cpdef Instance generateInstanceFromSentence(self, Sentence sentence, int wordIndex)
