from MorphologicalAnalysis.MorphologicalParse cimport MorphologicalParse
from MorphologicalAnalysis.MorphologicalTag import MorphologicalTag


cdef class LastIGContainsTagAttribute(BinaryAttribute):

    def __init__(self, parse: MorphologicalParse, tag: MorphologicalTag):
        """
        Binary attribute for a given word. If the last inflectional group of the word contains tag,
        the attribute will be "true", otherwise "false".

        PARAMETERS
        ----------
        parse : MorphologicalParse
            Morphological parse of the word.
        tag : MorphologicalTag
            Tag that is checked in the last inflectional group.
        """
        super().__init__(parse.lastIGContainsTag(tag))
