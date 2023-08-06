cdef class SimpleWindowInstanceGenerator(InstanceGenerator):

    cpdef addAttributesForWords(self, Instance current, Sentence sentence, int wordIndex):
        pass

    cpdef addAttributesForEmptyWords(self, Instance current, str emptyWord):
        pass

    cpdef addAttributes(self, Instance current, Sentence sentence, int wordIndex):
        """
        addAttributes adds all attributes of the previous words, the current wordn, and next words of the given word
        to the given instance. If the previous or next words does not exists, the method calls
        addAttributesForEmptyWords method. If the word does not exists in the dictionary or the required annotation
        layer does not exists in the annotated word, the method throws InstanceNotGenerated. The window size determines
        the number of previous and next words.

        PARAMETERS
        ----------
        current : Instance
            Current classification instance to which attributes will be added.
        sentence : Sentence
            Input sentence.
        wordIndex : int
            The index of the word in the sentence.
        """
        cdef int i
        for i in range(self.windowSize):
            if wordIndex - self.windowSize + i >= 0:
                self.addAttributesForWords(current, sentence, wordIndex - self.windowSize + i)
            else:
                self.addAttributesForEmptyWords(current, "<s>")
            self.addAttributesForWords(current, sentence, wordIndex)
        for i in range(self.windowSize):
            if wordIndex + i + 1 < sentence.wordCount():
                self.addAttributesForWords(current, sentence, wordIndex + i + 1)
            else:
                self.addAttributesForEmptyWords(current, "</s>")
