from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from MorphologicalAnalysis.MorphologicalParse cimport MorphologicalParse


cdef class RootPosAttribute(DiscreteAttribute):

    def __init__(self, parse: MorphologicalParse):
        """
        Discrete attribute for a given word. Returns the part of speech of the root word

        PARAMETERS
        ----------
        parse : MorphologicalParse
            Morphological parse of the word.
        """
        super().__init__(parse.getRootPos())
