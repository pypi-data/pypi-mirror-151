from abaqusConstants import *
from .LoadState import LoadState


class BodyForceState(LoadState):
    """The BodyForceState object stores the propagating data of a body force in a step. One
    instance of this object is created internally by the BodyForce object for each step. The 
    instance is also deleted internally by the BodyForce object. 
    The BodyForceState object has no constructor or methods. 
    The BodyForceState object is derived from the LoadState object. 

    Attributes
    ----------
    comp1: float
        A Float or a Complex specifying the body force component in the 1-direction.
    comp2: float
        A Float or a Complex specifying the body force component in the 2-direction.
    comp3: float
        A Float or a Complex specifying the body force component in the 3-direction.
    comp1State: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the body force component in the
        1-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED.
    comp2State: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the body force component in the
        2-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED.
    comp3State: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the body force component in the
        3-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED.
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

    # A Float or a Complex specifying the body force component in the 1-direction. 
    comp1: float = None

    # A Float or a Complex specifying the body force component in the 2-direction. 
    comp2: float = None

    # A Float or a Complex specifying the body force component in the 3-direction. 
    comp3: float = None

    # A SymbolicConstant specifying the propagation state of the body force component in the 
    # 1-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED. 
    comp1State: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the body force component in the 
    # 2-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED. 
    comp2State: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the body force component in the 
    # 3-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED. 
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
