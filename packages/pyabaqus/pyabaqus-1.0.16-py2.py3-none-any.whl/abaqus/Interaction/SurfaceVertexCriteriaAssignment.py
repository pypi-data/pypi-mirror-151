import typing

from abaqusConstants import *


class SurfaceVertexCriteriaAssignment:
    """The SurfaceVertexCriteriaAssignment object stores the surface vertex criteria assignment
    definition for surfaces in ContactStd objects. The SurfaceVertexCriteriaAssignment 
    object has no constructor or members. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import interaction
        mdb.models[name].interactions[name].surfacevertexCriteriaAssignments

    The corresponding analysis keywords are:

    - SURFACE PROPERTY ASSIGNMENT

    """

    def changeValuesInStep(self, stepName: str, index: int, value: typing.Union[SymbolicConstant, float]):
        """This method allows modification of surface vertex criteria assignments already defined
        on surfaces in a given step.
        
        Parameters
        ----------
        stepName
            A String specifying the name of the step in which the surface vertex criteria 
            assignments are to be modified. 
        index
            An Int specifying the position of the surface vertex criteria assignment whose value is 
            to be modified. 
        value
            A tuple specifying the value of the surface vertex criteria assignments for the surface 
            whose index is referenced. Each tuple contains: 
            - A Float or a SymbolicConstant specifying the vertex criteria value to be used for the 
            surface. Possible values of the SymbolicConstant are ALL_VERTICES or NO_VERTICES. 
        """
        pass

    def appendInStep(self, stepName: str, assignments: typing.Union[SymbolicConstant, float]):
        """This method allows addition of surface vertex criteria assignments to new surfaces in a
        given step.
        
        Parameters
        ----------
        stepName
            A String specifying the name of the step in which new surface vertex criteria 
            assignments are to be defined. 
        assignments
            A sequence of tuples specifying the surface vertex criteria assignments. Each tuple 
            contains two entries: 
            - A region or a material object or the SymbolicConstant GLOBAL specifying the surface to 
            which the vertex criteria is assigned. 
            - A Float or a SymbolicConstant specifying the vertex criteria value to be used for the 
            surface. Possible values of the SymbolicConstant are ALL_VERTICES or NO_VERTICES. 
        """
        pass

    def delete(self, indices: tuple):
        """The delete method allows you to delete existing surface vertex criteria assignments from
        a ContactStd object.
        
        Parameters
        ----------
        indices
            A sequence of Ints specifying the index of each surface vertex criteria assignment to 
            delete. 
        """
        pass
