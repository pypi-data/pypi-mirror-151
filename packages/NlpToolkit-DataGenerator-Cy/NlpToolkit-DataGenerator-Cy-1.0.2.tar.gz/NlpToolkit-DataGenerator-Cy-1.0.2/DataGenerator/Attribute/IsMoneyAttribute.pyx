from Classification.Attribute.BinaryAttribute cimport BinaryAttribute
from Dictionary.Word cimport Word


cdef class IsMoneyAttribute(BinaryAttribute):

    def __init__(self, surfaceForm: str):
        """
        Binary attribute for a given word. If the word is "dolar", "euro", "sterlin", etc., the attribute will have the
        value "true", otherwise "false".

        PARAMETERS
        ----------
        surfaceForm : str
            Surface form of the word.
        """
        super().__init__(Word.isMoney(surfaceForm))
