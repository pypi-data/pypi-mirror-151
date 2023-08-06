from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence
from AnnotatedSentence.AnnotatedWord cimport AnnotatedWord
from Classification.Instance.CompositeInstance cimport CompositeInstance
from WordNet.SynSet cimport SynSet


cdef class SemanticInstanceGenerator(SimpleWindowInstanceGenerator):

    def __init__(self, fsm: FsmMorphologicalAnalyzer, wordNet: WordNet):
        """
        Constructor for the semantic instance generator. Takes morphological analyzer and wordnet as input to set the
        corresponding variables.

        PARAMETERS
        ----------
        fsm : FsmMorphologicalAnalyzer
            Morphological analyzer to be used.
        wordNet : WordNet
            Wordnet to be used.
        """
        self.__fsm = fsm
        self.__wordNet = wordNet

    cpdef addAttributesForWords(self, Instance current, Sentence sentence, int wordIndex):
        """
        Generates a single classification instance of the WSD problem for the given word of the given sentence. If the
        word has not been labeled with sense tag yet, the method returns null. In the WSD problem, the system also
        generates and stores all possible sense labels for the current instance. In this case, a classification
        instance will not have all labels in the dataset, but some subset of it.

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
        pass

    cpdef addAttributesForEmptyWords(self, Instance current, str emptyWord):
        pass

    cpdef Instance generateInstanceFromSentence(self, Sentence sentence, int wordIndex):
        cdef list possibleSynSets, possibleClassLabels
        cdef AnnotatedWord word
        cdef str classLabel
        cdef CompositeInstance current
        cdef SynSet synSet
        if isinstance(sentence, AnnotatedSentence):
            possibleSynSets = sentence.constructSynSets(self.__wordNet, self.__fsm, wordIndex)
            word = sentence.getWord(wordIndex)
            if isinstance(word, AnnotatedWord):
                classLabel = word.getSemantic()
                current = CompositeInstance(classLabel)
                possibleClassLabels = []
                for synSet in possibleSynSets:
                    possibleClassLabels.append(synSet.getId())
                current.setPossibleClassLabels(possibleClassLabels)
                self.addAttributes(current, sentence, wordIndex)
                return current
