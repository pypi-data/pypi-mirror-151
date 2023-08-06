from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence
from AnnotatedSentence.AnnotatedWord cimport AnnotatedWord
from AnnotatedSentence.AnnotatedCorpus cimport AnnotatedCorpus
from DisambiguationCorpus.DisambiguatedWord cimport DisambiguatedWord
from DisambiguationCorpus.DisambiguationCorpus cimport DisambiguationCorpus

cdef class SentenceDisambiguationCorpusGenerator:

    cdef AnnotatedCorpus __annotatedCorpus

    def __init__(self, folder: str, pattern: str):
        """
        Constructor for the DisambiguationCorpusGenerator which takes input the data directory and the pattern for the
        training files included. The constructor loads the corpus from the given directory including the given files
        the given pattern.

        PARAMETERS
        ----------
        folder : str
            Directory where the sentence files reside.
        pattern : str
            Pattern of the tree files to be included in the corpus. Use "." for all files.
        """
        self.__annotatedCorpus = AnnotatedCorpus(folder, pattern)

    cpdef DisambiguationCorpus generate(self):
        """
        Creates a morphological disambiguation corpus from the corpus.

        RETURNS
        -------
        DisambiguationCorpus
            Created disambiguation corpus.
        """
        cdef DisambiguationCorpus corpus
        cdef int i
        cdef AnnotatedSentence disambiguationSentence
        cdef AnnotatedWord annotatedWord
        corpus = DisambiguationCorpus()
        for i in range(self.__annotatedCorpus.sentenceCount()):
            sentence = self.__annotatedCorpus.getSentence(i)
            disambiguationSentence = AnnotatedSentence()
            for j in range(sentence.wordCount()):
                annotatedWord = sentence.getWord(j)
                if isinstance(annotatedWord, AnnotatedWord):
                    disambiguationSentence.addWord(DisambiguatedWord(annotatedWord.getName(),
                                                                     annotatedWord.getParse()))
            corpus.addSentence(disambiguationSentence)
        return corpus
