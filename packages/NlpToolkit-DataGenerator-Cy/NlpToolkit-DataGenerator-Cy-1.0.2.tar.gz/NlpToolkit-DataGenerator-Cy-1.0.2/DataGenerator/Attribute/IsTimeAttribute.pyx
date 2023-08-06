from Classification.Attribute.BinaryAttribute cimport BinaryAttribute
from Dictionary.Word cimport Word


cdef class IsTimeAttribute(BinaryAttribute):

    def __init__(self, surfaceForm: str):
        """
        Binary attribute for a given word. If the word represents a time form, the attribute will have the
        value "true", otherwise "false".

        PARAMETERS
        ----------
        surfaceForm : str
            Surface form of the word.
        """
        super().__init__(Word.isTime(surfaceForm))
