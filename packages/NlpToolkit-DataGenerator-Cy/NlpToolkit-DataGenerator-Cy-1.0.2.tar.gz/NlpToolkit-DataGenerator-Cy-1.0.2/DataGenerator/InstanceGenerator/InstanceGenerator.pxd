from Classification.Instance.Instance cimport Instance
from Corpus.Sentence cimport Sentence


cdef class InstanceGenerator:

    cdef int windowSize

    cpdef Instance generateInstanceFromSentence(self, Sentence sentence, int wordIndex)
