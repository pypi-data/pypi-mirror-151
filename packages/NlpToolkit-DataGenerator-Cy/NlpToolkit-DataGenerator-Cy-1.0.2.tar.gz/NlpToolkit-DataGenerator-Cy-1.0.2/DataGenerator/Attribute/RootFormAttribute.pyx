from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from MorphologicalAnalysis.MorphologicalParse cimport MorphologicalParse


cdef class RootFormAttribute(DiscreteAttribute):

    def __init__(self, parse: MorphologicalParse):
        """
        Discrete attribute for a given word. Returns the the root word

        PARAMETERS
        ----------
        parse : MorphologicalParse
            Morphological parse of the word.
        """
        super().__init__(parse.getWord().getName())
