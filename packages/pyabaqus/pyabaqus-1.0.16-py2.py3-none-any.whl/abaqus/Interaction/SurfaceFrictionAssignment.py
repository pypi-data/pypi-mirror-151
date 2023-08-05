import typing

from abaqusConstants import *


class SurfaceFrictionAssignment:
    """The SurfaceFrictionAssignment object stores the surface friction assignment definition
    for surfaces in ContactExp objects. The SurfaceFrictionAssignment object has no 
    constructor or members. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import interaction
        mdb.models[name].interactions[name].surfaceFrictionAssignments

    The corresponding analysis keywords are:

    - SURFACE PROPERTY ASSIGNMENT

    """

    def changeValuesInStep(self, stepName: str, index: int, value: float):
        """This method allows modification of surface friction assignments already defined on
        surfaces in a given step.
        
        Parameters
        ----------
        stepName
            A String specifying the name of the step in which the surface friction assignments are 
            to be modified. 
        index
            An Int specifying the position of the surface friction assignment whose value is to be 
            modified. 
        value
            A tuple specifying the value of the surface friction assignments for the surface whose 
            index is referenced. Each tuple contains: 
            - A Float specifying the overriding friction coefficient value to be used in the contact 
            definition. 
        """
        pass

    def appendInStep(self, stepName: str, assignments: typing.Union[SymbolicConstant, float]):
        """This method allows addition of surface friction assignments to new surfaces in a given
        step.
        
        Parameters
        ----------
        stepName
            A String specifying the name of the step in which new surface friction assignments are 
            to be defined. 
        assignments
            A sequence of tuples specifying the surface friction assignments. Each tuple contains 
            two entries: 
            - A region or a material object or the SymbolicConstant GLOBAL specifying the surface to 
            which the friction coefficient is assigned. 
            - A Float specifying the overriding friction coefficient to be used in the contact 
            definition. 
        """
        pass

    def delete(self, indices: tuple):
        """The delete method allows you to delete existing surface friction assignments.
        
        Parameters
        ----------
        indices
            A sequence of Ints specifying the index of each surface friction assignment to delete. 
        """
        pass
