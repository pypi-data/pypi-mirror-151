from AnnotatedSentence.AnnotatedWord cimport AnnotatedWord
from Classification.Instance.Instance cimport Instance
from Corpus.Sentence cimport Sentence
from DataGenerator.InstanceGenerator.SimpleWindowInstanceGenerator cimport SimpleWindowInstanceGenerator


cdef class ShallowParseInstanceGenerator(SimpleWindowInstanceGenerator):

    cpdef addAttributesForWords(self, Instance current, Sentence sentence, int wordIndex):
        pass

    cpdef addAttributesForEmptyWords(self, Instance current, str emptyWord):
        pass

    cpdef Instance generateInstanceFromSentence(self, Sentence sentence, int wordIndex):
        """
        Generates a single classification instance of the Shallow Parse problem for the given word of the given
        sentence. If the  word has not been labeled with shallow parse tag yet, the method returns null.

        PARAMETERS
        ----------
        sentence : Sentence
            Input sentence.
        wordIndex : int
            The index of the word in the sentence.

        RETURNS
        -------
        Instance
            Classification instance.
        """
        cdef AnnotatedWord word
        cdef str classLabel
        cdef Instance current
        word = sentence.getWord(wordIndex)
        if isinstance(word, AnnotatedWord):
            classLabel = word.getShallowParse()
            current = Instance(classLabel)
            self.addAttributes(current, sentence, wordIndex)
            return current
