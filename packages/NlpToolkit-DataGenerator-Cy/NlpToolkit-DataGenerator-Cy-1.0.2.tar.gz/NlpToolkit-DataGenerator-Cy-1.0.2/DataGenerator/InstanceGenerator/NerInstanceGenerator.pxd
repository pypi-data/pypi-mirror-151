from Classification.Instance.Instance cimport Instance
from Corpus.Sentence cimport Sentence
from DataGenerator.InstanceGenerator.SimpleWindowInstanceGenerator cimport SimpleWindowInstanceGenerator


cdef class NerInstanceGenerator(SimpleWindowInstanceGenerator):

    cpdef addAttributesForWords(self, Instance current, Sentence sentence, int wordIndex)
    cpdef addAttributesForEmptyWords(self, Instance current, str emptyWord)
    cpdef Instance generateInstanceFromSentence(self, Sentence sentence, int wordIndex)
