from AnnotatedSentence.ViewLayerType import ViewLayerType
from AnnotatedTree.TreeBankDrawable cimport TreeBankDrawable
from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable
from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence
from AnnotatedSentence.AnnotatedWord cimport AnnotatedWord
from DisambiguationCorpus.DisambiguatedWord cimport DisambiguatedWord
from DisambiguationCorpus.DisambiguationCorpus cimport DisambiguationCorpus


cdef class TreeDisambiguationCorpusGenerator:

    cdef TreeBankDrawable __treeBank

    def __init__(self, folder: str, pattern: str):
        """
        Constructor for the DisambiguationCorpusGenerator which takes input the data directory and the pattern for the
        training files included. The constructor loads the treebank from the given directory including the given files
        the given pattern.

        PARAMETERS
        ----------
        folder : str
            Directory where the treebank files reside.
        pattern : str
            Pattern of the tree files to be included in the treebank. Use "." for all files.
        """
        self.__treeBank = TreeBankDrawable(folder, pattern)

    cpdef DisambiguationCorpus generate(self):
        """
        Creates a morphological disambiguation corpus from the treeBank. Calls generateAnnotatedSentence for each parse
        tree in the treebank.

        RETURNS
        -------
        DisambiguationCorpus
            Created disambiguation corpus.
        """
        cdef DisambiguationCorpus corpus
        cdef int i
        cdef ParseTreeDrawable parseTree
        cdef AnnotatedSentence sentence, disambiguationSentence
        cdef AnnotatedWord annotatedWord
        corpus = DisambiguationCorpus()
        for i in range(self.__treeBank.size()):
            parseTree = self.__treeBank.get(i)
            if parseTree.layerAll(ViewLayerType.INFLECTIONAL_GROUP):
                sentence = parseTree.generateAnnotatedSentence()
                disambiguationSentence = AnnotatedSentence()
                for j in range(sentence.wordCount()):
                    annotatedWord = sentence.getWord(j)
                    if isinstance(annotatedWord, AnnotatedWord):
                        disambiguationSentence.addWord(DisambiguatedWord(annotatedWord.getName(),
                                                                         annotatedWord.getParse()))
                corpus.addSentence(disambiguationSentence)
        return corpus
