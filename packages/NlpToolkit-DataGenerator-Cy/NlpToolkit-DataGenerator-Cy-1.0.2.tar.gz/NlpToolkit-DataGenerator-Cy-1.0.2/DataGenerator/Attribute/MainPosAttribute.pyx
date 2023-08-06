from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from MorphologicalAnalysis.MorphologicalParse cimport MorphologicalParse


cdef class MainPosAttribute(DiscreteAttribute):

    def __init__(self, parse: MorphologicalParse):
        """
        Discrete attribute for a given word. Returns the last part of speech (main part of speech) of the word

        PARAMETERS
        ----------
        parse : MorphologicalParse
            Morphological parse of the word.
        """
        super().__init__(parse.getPos())
