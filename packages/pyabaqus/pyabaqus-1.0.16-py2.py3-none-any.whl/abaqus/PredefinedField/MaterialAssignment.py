from abaqusConstants import *
from .PredefinedField import PredefinedField
from ..Assembly.PartInstanceArray import PartInstanceArray
from ..Region.Region import Region


class MaterialAssignment(PredefinedField):
    """The MaterialAssignment object stores the data for an initial material assignment
    predefined field, for use with an Eulerian analysis. 
    The MaterialAssignment object is derived from the PredefinedField object. 

    Attributes
    ----------
    region: Region
        A :py:class:`~abaqus.Region.Region.Region` object specifying the region to which the predefined field is applied.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import load
        mdb.models[name].predefinedFields[name]

    The corresponding analysis keywords are:

    - INITIAL CONDITIONS

    """

    # A Region object specifying the region to which the predefined field is applied. 
    region: Region = Region()

    def __init__(self, name: str, instanceList: PartInstanceArray, useFields: Boolean = OFF,
                 assignmentList: tuple = (), fieldList: tuple = (), colorList: tuple = ()):
        """This method creates a MaterialAssignment predefined field object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].MaterialAssignment
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        instanceList
            A PartInstanceArray object specifying the part instances to which the predefined field 
            is applied. All instances must be assigned the same Eulerian section. 
        useFields
            A Boolean specifying whether the volume fraction data will be uniform or defined by 
            discrete fields. The default value is OFF. 
        assignmentList
            A sequence of tuples specifying the uniform volume fractions to be assigned. This 
            argument is valid only when *useFields*=FALSE. Each tuple contains two entries:A Region 
            object.A tuple of Floats specifying the uniform volume fraction values. The length of 
            the tuple must match the number of material instance names specified in the Eulerain 
            section assigned to part instances specified by *instanceList*. 
        fieldList
            A sequence of tuples specifying the discrete volume fractions to be assigned. This 
            argument is valid only when *useFields*=TRUE. Each tuple contains two entries:A Region 
            object.A tuple of Strings specifying Discrete Field names. The length of the tuple must 
            match the number of material instance names specified in the Eulerain section assigned 
            to part instances specified by *instanceList*. 
        colorList
            A sequence of three Ints specifying colors used to display the material instance 
            assignments. This is a sequence of R,G,B colors, where the values are represented by 
            integers between 0 and 255. The default value is an empty sequence. 

        Returns
        -------
            A MaterialAssignment object.
        """
        super().__init__()
        pass

    def setValues(self, useFields: Boolean = OFF, assignmentList: tuple = (), fieldList: tuple = (),
                  colorList: tuple = ()):
        """This method modifies the MaterialAssignment object.
        
        Parameters
        ----------
        useFields
            A Boolean specifying whether the volume fraction data will be uniform or defined by 
            discrete fields. The default value is OFF. 
        assignmentList
            A sequence of tuples specifying the uniform volume fractions to be assigned. This 
            argument is valid only when *useFields*=FALSE. Each tuple contains two entries:A Region 
            object.A tuple of Floats specifying the uniform volume fraction values. The length of 
            the tuple must match the number of material instance names specified in the Eulerain 
            section assigned to part instances specified by *instanceList*. 
        fieldList
            A sequence of tuples specifying the discrete volume fractions to be assigned. This 
            argument is valid only when *useFields*=TRUE. Each tuple contains two entries:A Region 
            object.A tuple of Strings specifying Discrete Field names. The length of the tuple must 
            match the number of material instance names specified in the Eulerain section assigned 
            to part instances specified by *instanceList*. 
        colorList
            A sequence of three Ints specifying colors used to display the material instance 
            assignments. This is a sequence of R,G,B colors, where the values are represented by 
            integers between 0 and 255. The default value is an empty sequence. 
        """
        pass
