from abaqusConstants import *
from .Constraint import Constraint
from ..Region.Region import Region


class ShellSolidCoupling(Constraint):
    """The ShellSolidCoupling object defines two surfaces to be tied together for the duration
    of a simulation. 
    The ShellSolidCoupling object is derived from the ConstrainedSketchConstraint object.

    Attributes
    ----------
    suppressed: Boolean
        A Boolean specifying whether the constraint is suppressed or not. The default value is
        OFF.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import interaction
        mdb.models[name].constraints[name]

    The corresponding analysis keywords are:

    - SHELL TO SOLID COUPLING

    """

    # A Boolean specifying whether the constraint is suppressed or not. The default value is 
    # OFF. 
    suppressed: Boolean = OFF

    def __init__(self, name: str, shellEdge: Region, solidFace: Region,
                 positionToleranceMethod: SymbolicConstant = COMPUTED, positionTolerance: float = 0,
                 influenceDistanceMethod: SymbolicConstant = DEFAULT, influenceDistance: float = 0):
        """This method creates a ShellSolidCoupling object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].ShellSolidCoupling
        
        Parameters
        ----------
        name
            A String specifying the constraint repository key. 
        shellEdge
            A Region object specifying the name of the shell edge surface. 
        solidFace
            A Region object specifying the name of the solid surface. 
        positionToleranceMethod
            A SymbolicConstant specifying the method used to determine the position tolerance. 
            Possible values are COMPUTED and SPECIFIED. The default value is COMPUTED. 
        positionTolerance
            A Float specifying the position tolerance. The default value is 0.0.The 
            *positionTolerance* argument applies only when 
            *positionToleranceMethod*=SPECIFIED.Note:Abaqus will not constrain nodes on the solid 
            face region outside the position tolerance. 
        influenceDistanceMethod
            A SymbolicConstant specifying the method used to determine the influence distance. 
            Possible values are DEFAULT and SPECIFIED. The default value is DEFAULT. 
        influenceDistance
            A Float specifying the influence distance. The *influenceDistance* argument applies only 
            when *influenceDistanceMethod*=SPECIFIED. The default value is 0.0. 

        Returns
        -------
            A ShellSolidCoupling object.
        """
        super().__init__()
        pass

    def setValues(self, positionToleranceMethod: SymbolicConstant = COMPUTED, positionTolerance: float = 0,
                  influenceDistanceMethod: SymbolicConstant = DEFAULT, influenceDistance: float = 0):
        """This method modifies the ShellSolidCoupling object.
        
        Parameters
        ----------
        positionToleranceMethod
            A SymbolicConstant specifying the method used to determine the position tolerance. 
            Possible values are COMPUTED and SPECIFIED. The default value is COMPUTED. 
        positionTolerance
            A Float specifying the position tolerance. The default value is 0.0.The 
            *positionTolerance* argument applies only when 
            *positionToleranceMethod*=SPECIFIED.Note:Abaqus will not constrain nodes on the solid 
            face region outside the position tolerance. 
        influenceDistanceMethod
            A SymbolicConstant specifying the method used to determine the influence distance. 
            Possible values are DEFAULT and SPECIFIED. The default value is DEFAULT. 
        influenceDistance
            A Float specifying the influence distance. The *influenceDistance* argument applies only 
            when *influenceDistanceMethod*=SPECIFIED. The default value is 0.0. 
        """
        pass
