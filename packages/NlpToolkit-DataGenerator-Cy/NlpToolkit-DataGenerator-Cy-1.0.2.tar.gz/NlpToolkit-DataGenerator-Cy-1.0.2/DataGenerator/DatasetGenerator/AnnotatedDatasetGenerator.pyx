from AnnotatedSentence.AnnotatedCorpus cimport AnnotatedCorpus
from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence
from Classification.DataSet.DataSet cimport DataSet
from DataGenerator.InstanceGenerator.InstanceGenerator cimport InstanceGenerator


cdef class AnnotatedDatasetGenerator:

    cdef AnnotatedCorpus __corpus
    cdef InstanceGenerator instanceGenerator

    def __init__(self, folder: str, pattern: str, instanceGenerator: InstanceGenerator):
        """
        Constructor for the AnnotatedDataSetGenerator which takes input the data directory, the pattern for the
        training files included, and an instanceGenerator. The constructor loads the sentence corpus from the given
        directory including the given files having the given pattern.

        PARAMETERS
        ----------
        folder : str
            Directory where the corpus files reside.
        pattern : str
            Pattern of the tree files to be included in the treebank. Use "." for all files.
        instanceGenerator : InstanceGenerator
            The instance generator used to generate the dataset.
        """
        self.__corpus = AnnotatedCorpus(folder, pattern)
        self.instanceGenerator = instanceGenerator

    cpdef setInstanceGenerator(self, InstanceGenerator instanceGenerator):
        """
        Mutator for the instanceGenerator attribute.

        PARAMETERS
        ----------
        instanceGenerator : InstanceGenerator
            Input instanceGenerator
        """
        self.instanceGenerator = instanceGenerator

    cpdef DataSet generate(self):
        """
        Creates a dataset from the corpus. Calls generateInstanceFromSentence for each parse sentence in the corpus.

        RETURNS
        -------
        DataSet
            Created dataset.
        """
        cdef DataSet dataSet
        cdef AnnotatedSentence sentence, generatedInstance
        cdef int j
        dataSet = DataSet()
        for sentence in self.__corpus.sentences:
            for j in range(sentence.wordCount()):
                generatedInstance = self.instanceGenerator.generateInstanceFromSentence(sentence, j)
                if generatedInstance is not None:
                    dataSet.addInstance(generatedInstance)
        return dataSet
