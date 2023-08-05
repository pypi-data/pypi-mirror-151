from abaqusConstants import *
from .LoadState import LoadState


class GravityState(LoadState):
    """The GravityState object stores the propagating data for a gravity load in a step. One
    instance of this object is created internally by the Gravity object for each step. The 
    instance is also deleted internally by the Gravity object. 
    The GravityState object has no constructor or methods. 
    The GravityState object is derived from the LoadState object. 

    Attributes
    ----------
    comp1: float
        A Float or a Complex specifying the load component in the 1-direction.
    comp2: float
        A Float or a Complex specifying the load component in the 2-direction.
    comp3: float
        A Float or a Complex specifying the load component in the 3-direction.
    comp1State: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the load component in the
        1-direction. Possible values are UNSET, SET, UNCHANGED, and FREED.
    comp2State: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the load component in the
        2-direction. Possible values are UNSET, SET, UNCHANGED, and FREED.
    comp3State: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the load component in the
        3-direction. Possible values are UNSET, SET, UNCHANGED, and FREED.
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

    - DLOAD

    """

    # A Float or a Complex specifying the load component in the 1-direction. 
    comp1: float = None

    # A Float or a Complex specifying the load component in the 2-direction. 
    comp2: float = None

    # A Float or a Complex specifying the load component in the 3-direction. 
    comp3: float = None

    # A SymbolicConstant specifying the propagation state of the load component in the 
    # 1-direction. Possible values are UNSET, SET, UNCHANGED, and FREED. 
    comp1State: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the load component in the 
    # 2-direction. Possible values are UNSET, SET, UNCHANGED, and FREED. 
    comp2State: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the load component in the 
    # 3-direction. Possible values are UNSET, SET, UNCHANGED, and FREED. 
    comp3State: SymbolicConstant = None

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
