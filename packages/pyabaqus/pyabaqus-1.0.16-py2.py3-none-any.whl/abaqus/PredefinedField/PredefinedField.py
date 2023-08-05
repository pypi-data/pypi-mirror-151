from .IMAField import IMAField
from ..Region.Region import Region


class PredefinedField:
    """The PredefinedField object is the base object for the objects in the predefined field
    repository. The methods and members of the PredefinedField object are common to all 
    objects derived from PredefinedField. 
    An instance of any PredefinedField object can be obtained through the predefined field 
    repository of the Model object. An instance of any PredefinedFieldState object can be 
    obtained through the predefined field repository of the Step object. 

    Attributes
    ----------
    name: str
        A String specifying the repository key.
    region: Region
        A :py:class:`~abaqus.Region.Region.Region` object specifying the region to which the predefined field is applied. **:py:class:`~abaqus.Region.Region.Region`**
        is ignored if the predefined field has an **instances** member available. **:py:class:`~abaqus.Region.Region.Region`** is also
        ignored if the predefined field has a **distributionType** member available, and
        **distributionType=FROM_FILE** or FROM_FILE_AND_USER_DEFINED.
    fieldList: IMAField
        An IMAField for MaterialAssignment predefined field。

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import load
        mdb.models[name].predefinedFields[name]

    """

    # A String specifying the repository key. 
    name: str = ''

    # A Region object specifying the region to which the predefined field is applied. *Region* 
    # is ignored if the predefined field has an *instances* member available. *Region* is also 
    # ignored if the predefined field has a *distributionType* member available, and 
    # *distributionType*=FROM_FILE or FROM_FILE_AND_USER_DEFINED. 
    region: Region = Region()

    # An IMAField for MaterialAssignment predefined field。
    fieldList: IMAField = IMAField()

    def move(self, fromStepName: str, toStepName: str):
        """This method moves a specific PredefinedFieldState object from one step to a different
        step.
        
        Parameters
        ----------
        fromStepName
            A String specifying the name of the step from which the PredefinedFieldState object is 
            moved. 
        toStepName
            A String specifying the name of the step to which the PredefinedFieldState object is 
            moved.

        Raises
        ------
            TextError. 
        """
        pass

    def resume(self):
        """This method resumes the predefined field that was previously suppressed.
        """
        pass

    def suppress(self):
        """This method suppresses the predefined field.
        """
        pass

    def delete(self, indices: tuple):
        """This method allows you to delete existing fields.
        
        Parameters
        ----------
        indices
            A sequence of Ints specifying the index of each field to delete. 
        """
        pass
