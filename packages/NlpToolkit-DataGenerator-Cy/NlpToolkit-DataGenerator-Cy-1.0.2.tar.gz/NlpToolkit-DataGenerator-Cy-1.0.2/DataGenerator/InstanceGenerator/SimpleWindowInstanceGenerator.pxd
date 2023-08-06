from Classification.Instance.Instance cimport Instance
from Corpus.Sentence cimport Sentence
from DataGenerator.InstanceGenerator.InstanceGenerator cimport InstanceGenerator


cdef class SimpleWindowInstanceGenerator(InstanceGenerator):

    cpdef addAttributesForWords(self, Instance current, Sentence sentence, int wordIndex)
    cpdef addAttributesForEmptyWords(self, Instance current, str emptyWord)
    cpdef addAttributes(self, Instance current, Sentence sentence, int wordIndex)
