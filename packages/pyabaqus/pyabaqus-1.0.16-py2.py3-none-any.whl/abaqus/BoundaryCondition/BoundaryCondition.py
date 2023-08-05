from abaqusConstants import *
from ..Region.Region import Region


class BoundaryCondition:
    """The BoundaryCondition object is the abstract base type for other BoundaryCondition
    objects. The BoundaryCondition object has no explicit constructor. The methods and 
    members of the BoundaryCondition object are common to all objects derived from the 
    BoundaryCondition. 

    Attributes
    ----------
    name: str
        A String specifying the boundary condition repository key.
    category: SymbolicConstant
        A SymbolicConstant specifying the category of the boundary condition. Possible values
        are MECHANICAL and THERMAL.
    region: Region
        A :py:class:`~abaqus.Region.Region.Region` object specifying the region to which the boundary condition is applied.
    localCsys: str
        None or a :py:class:`~abaqus.Datum.DatumCsys.DatumCsys` object specifying the local coordinate system of the boundary
        condition's degrees of freedom. If **localCsys=None**, the degrees of freedom are defined
        in the global coordinate system. The default value is None.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import load
        mdb.models[name].boundaryConditions[name]

    """

    # A String specifying the boundary condition repository key. 
    name: str = ''

    # A SymbolicConstant specifying the category of the boundary condition. Possible values 
    # are MECHANICAL and THERMAL. 
    category: SymbolicConstant = None

    # A Region object specifying the region to which the boundary condition is applied. 
    region: Region = Region()

    # None or a DatumCsys object specifying the local coordinate system of the boundary 
    # condition's degrees of freedom. If *localCsys*=None, the degrees of freedom are defined 
    # in the global coordinate system. The default value is None. 
    localCsys: str = None

    def deactivate(self, stepName: str):
        """This method deactivates the boundary condition in the specified step and all subsequent
        steps.
        
        Parameters
        ----------
        stepName
            A String specifying the name of the step in which the boundary condition is deactivated.
        """
        pass

    def move(self, fromStepName: str, toStepName: str):
        """This method moves the boundary condition state from one step to a different step.
        
        Parameters
        ----------
        fromStepName
            A String specifying the name of the step from which the boundary condition state is 
            moved. 
        toStepName
            A String specifying the name of the step to which the boundary condition state is moved.
        """
        pass

    def reset(self, stepName: str):
        """This method resets the boundary condition state of the specified step to the state of
        the previous analysis step.
        
        Parameters
        ----------
        stepName
            A String specifying the name of the step in which the boundary condition state is reset.
        """
        pass

    def resume(self):
        """This method resumes the boundary condition that was previously suppressed.
        """
        pass

    def suppress(self):
        """This method suppresses the boundary condition.
        """
        pass

    def delete(self, indices: tuple):
        """This method allows you to delete existing boundary conditions.
        
        Parameters
        ----------
        indices
            A sequence of Ints specifying the index of each boundary condition to delete. 
        """
        pass

    def setValues(self, *args, **kwargs):
        pass

    def setValuesInStep(self, *args, **kwargs):
        pass
