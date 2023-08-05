from abaqusConstants import *


class Constraint:
    """The ConstrainedSketchConstraint object is the abstract base type for other ConstrainedSketchConstraint objects. The
    ConstrainedSketchConstraint object has no explicit constructor. The members of the ConstrainedSketchConstraint object are
    common to all objects derived from the ConstrainedSketchConstraint.

    Attributes
    ----------
    name: str
        A String specifying the constraint repository key.
    suppressed: Boolean
        A Boolean specifying whether the constraint is suppressed or not. The default value is
        OFF.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import interaction
        mdb.models[name].constraints[name]

    """

    # A String specifying the constraint repository key. 
    name: str = ''

    # A Boolean specifying whether the constraint is suppressed or not. The default value is 
    # OFF. 
    suppressed: Boolean = OFF

    def resume(self):
        """This method resumes the constraint that was previously suppressed.
        """
        pass

    def suppress(self):
        """This method suppresses the constraint.
        """
        pass

    def delete(self, indices: tuple):
        """This method allows you to delete existing constraints.
        
        Parameters
        ----------
        indices
            A sequence of Ints specifying the index of each constraint to delete. 
        """
        pass
