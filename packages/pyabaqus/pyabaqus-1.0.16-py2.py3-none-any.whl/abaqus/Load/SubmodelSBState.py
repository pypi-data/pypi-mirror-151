from abaqusConstants import *
from .LoadState import LoadState


class SubmodelSBState(LoadState):
    """The SubmodelSBState object stores the propagating data for a Submodel load in a step.
    One instance of this object is created internally by the SubmodelSB object for each 
    step. The instance is also deleted internally by the SubmodelSB object. 
    The SubmodelSBState object has no constructor or methods. 
    The SubmodelSBState object is derived from the LoadState object. 

    Attributes
    ----------
    globalStepState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **globalStep** member. Possible
        values are SET and UNCHANGED.
    globalIncrement: int
        An Int specifying the increment number in the global model step at which the solution
        will be used to specify the values of the driven variables. This argument is applicable
        only for linear perturbation steps.
    globalIncrementState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **globalIncrement** member.
        Possible values are SET and UNCHANGED.
    globalStep: str
        A String specifying the step in the global model from which Abaqus reads the values of
        the variables that will drive the submodel analysis. The String indicates the position
        of the step in the sequence of analysis steps. For example, **globalStep**='1' indicates
        the first step.
    amplitudeState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **amplitude** member. Possible
        values are UNSET, SET, UNCHANGED, and FREED.
    status: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the :py:class:`~abaqus.Load.LoadState.LoadState` object. Possible
        values are:
            - NOT_YET_ACTIVE
            - CREATED
            - PROPAGATED
            - MODIFIED
            - DEACTIVATED
            - NO_LONGER_ACTIVE
            - TYPE_NOT_APPLICABLE
            - INSTANCE_NOT_APPLICABLE
            - BUILT_INTO_BASE_STATE
    amplitude: str
        A String specifying the name of the amplitude reference. The String is empty if the load
        has no amplitude reference.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import load
        mdb.models[name].steps[name].loadStates[name]

    The corresponding analysis keywords are:

    - SUBMODEL
            - DSLOAD

    """

    # A SymbolicConstant specifying the propagation state of the *globalStep* member. Possible 
    # values are SET and UNCHANGED. 
    globalStepState: SymbolicConstant = None

    # An Int specifying the increment number in the global model step at which the solution 
    # will be used to specify the values of the driven variables. This argument is applicable 
    # only for linear perturbation steps. 
    globalIncrement: int = None

    # A SymbolicConstant specifying the propagation state of the *globalIncrement* member. 
    # Possible values are SET and UNCHANGED. 
    globalIncrementState: SymbolicConstant = None

    # A String specifying the step in the global model from which Abaqus reads the values of 
    # the variables that will drive the submodel analysis. The String indicates the position 
    # of the step in the sequence of analysis steps. For example, *globalStep*='1' indicates 
    # the first step. 
    globalStep: str = ''

    # A SymbolicConstant specifying the propagation state of the *amplitude* member. Possible 
    # values are UNSET, SET, UNCHANGED, and FREED. 
    amplitudeState: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the LoadState object. Possible 
    # values are: 
    # - NOT_YET_ACTIVE 
    # - CREATED 
    # - PROPAGATED 
    # - MODIFIED 
    # - DEACTIVATED 
    # - NO_LONGER_ACTIVE 
    # - TYPE_NOT_APPLICABLE 
    # - INSTANCE_NOT_APPLICABLE 
    # - BUILT_INTO_BASE_STATE 
    status: SymbolicConstant = None

    # A String specifying the name of the amplitude reference. The String is empty if the load 
    # has no amplitude reference. 
    amplitude: str = ''
