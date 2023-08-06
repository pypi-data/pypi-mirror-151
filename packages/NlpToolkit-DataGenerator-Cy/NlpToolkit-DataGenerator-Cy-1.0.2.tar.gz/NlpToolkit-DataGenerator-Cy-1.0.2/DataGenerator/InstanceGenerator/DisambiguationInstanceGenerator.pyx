from AnnotatedSentence.AnnotatedWord cimport AnnotatedWord


cdef class DisambiguationInstanceGenerator(InstanceGenerator):

    cpdef addAttributesForPreviousWords(self, Instance current, Sentence sentence, int wordIndex):
        pass

    cpdef addAttributesForEmptyWords(self, Instance current, str emptyWord):
        pass

    cpdef Instance generateInstanceFromSentence(self, Sentence sentence, int wordIndex):
        """
        Generates a single classification instance of the morphological disambiguation problem for the given word of the
        given sentence. If the word does not have a morphological parse, the method throws InstanceNotGenerated.

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
        cdef Instance current
        cdef int i
        word = sentence.getWord(wordIndex)
        if isinstance(word, AnnotatedWord):
            current = Instance(word.getParse().getTransitionList())
            for i in range(self.windowSize):
                if wordIndex - self.windowSize + i >= 0:
                    self.addAttributesForPreviousWords(current, sentence, wordIndex - self.windowSize + i)
                else:
                    self.addAttributesForEmptyWords(current, "<s>")
            self.addAttributesForPreviousWords(current, sentence, wordIndex)
            return current
