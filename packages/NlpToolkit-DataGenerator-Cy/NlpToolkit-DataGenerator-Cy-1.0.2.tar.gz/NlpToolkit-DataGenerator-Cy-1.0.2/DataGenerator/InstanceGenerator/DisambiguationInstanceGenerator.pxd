from Classification.Instance.Instance cimport Instance
from Corpus.Sentence cimport Sentence
from DataGenerator.InstanceGenerator.InstanceGenerator cimport InstanceGenerator


cdef class DisambiguationInstanceGenerator(InstanceGenerator):

    cpdef addAttributesForPreviousWords(self, Instance current, Sentence sentence, int wordIndex)
    cpdef addAttributesForEmptyWords(self, Instance current, str emptyWord)
    cpdef Instance generateInstanceFromSentence(self, Sentence sentence, int wordIndex)
