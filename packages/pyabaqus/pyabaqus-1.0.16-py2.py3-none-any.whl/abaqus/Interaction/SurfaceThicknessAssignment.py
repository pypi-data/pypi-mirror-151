import typing

from abaqusConstants import *


class SurfaceThicknessAssignment:
    """The SurfaceThicknessAssignment object stores the surface thickness assignment definition
    for surfaces in ContactExp and ContactStd objects. The SurfaceThicknessAssignment object 
    has no constructor or members. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import interaction
        mdb.models[name].interactions[name].surfaceThicknessAssignments

    The corresponding analysis keywords are:

    - SURFACE PROPERTY ASSIGNMENT

    """

    def changeValuesInStep(self, stepName: str, index: int, value: typing.Union[SymbolicConstant, float]):
        """This method allows modification of surface thickness assignments already defined on
        surfaces in a given step.
        
        Parameters
        ----------
        stepName
            A String specifying the name of the step in which the surface thickness assignments are 
            to be modified. 
        index
            An Int specifying the position of the surface thickness assignment whose value is to be 
            modified. 
        value
            A tuple specifying the value of the surface thickness assignments for the surface whose 
            index is referenced. Each tuple contains two entries: 
            - A Float or a SymbolicConstant specifying the overriding thickness value to be used in 
            the contact definition. Possible values of the SymbolicConstant are ORIGINAL and 
            THINNING. The SymbolicConstant THINNING can be specified only in an Abaqus/Explicit 
            analysis. 
            - A Float specifying a scale factor that multiplies the thickness value specified in the 
            second entry. 
        """
        pass

    def appendInStep(self, stepName: str, assignments: typing.Union[SymbolicConstant, float]):
        """This method allows addition of surface thickness assignments to new surfaces in a given
        step.
        
        Parameters
        ----------
        stepName
            A String specifying the name of the step in which new surface thickness assignments are 
            to be defined. 
        assignments
            A sequence of tuples specifying the surface thickness assignments. Each tuple contains 
            three entries: 
            - A region or a material object or the SymbolicConstant GLOBAL specifying the surface to 
            which the thickness is assigned. 
            - A Float or a SymbolicConstant specifying the overriding thickness value to be used in 
            the contact definition. Possible values of the SymbolicConstant are ORIGINAL and 
            THINNING. The SymbolicConstant THINNING can be specified only in an Abaqus/Explicit 
            analysis. 
            - A Float specifying a scale factor that multiplies the thickness value specified in the 
            second entry. 
        """
        pass

    def delete(self, indices: tuple):
        """The delete method allows you to delete existing surface thickness assignments.
        
        Parameters
        ----------
        indices
            A sequence of Ints specifying the index of each surface thickness assignment to delete. 
        """
        pass
