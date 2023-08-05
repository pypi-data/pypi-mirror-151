from abaqusConstants import *
from .LoadState import LoadState


class ConcentratedForceState(LoadState):
    """The ConcentratedForceState object stores the propagating data for a concentrated force
    in a step. One instance of this object is created internally by the ConcentratedForce 
    object for each step. The instance is also deleted internally by the ConcentratedForce 
    object. 
    The ConcentratedForceState object has no constructor or methods. 
    The ConcentratedForceState object is derived from the LoadState object. 

    Attributes
    ----------
    cf1: float
        A Float or a Complex specifying the concentrated force component in the 1-direction.
        Although **cf1**, **cf2**, and **cf3** are optional arguments, at least one of them must be
        nonzero.
    cf2: float
        A Float or a Complex specifying the concentrated force component in the 2-direction.
    cf3: float
        A Float or a Complex specifying the concentrated force component in the 3-direction.
    cf1State: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the concentrated force component
        in the 1-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED.
    cf2State: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the concentrated force component
        in the 2-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED.
    cf3State: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the concentrated force component
        in the 3-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED.
    amplitudeState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **amplitude** member. Possible
        values are UNSET, SET, UNCHANGED, and FREED.
    status: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the :py:class:`~abaqus.Load.LoadState.LoadState` object. Possible
        values are:
    amplitude: str
        A String specifying the name of the amplitude reference. The String is empty if the load
        has no amplitude reference.
            - NOT_YET_ACTIVE
            - CREATED
            - PROPAGATED
            - MODIFIED
            - DEACTIVATED
            - NO_LONGER_ACTIVE
            - TYPE_NOT_APPLICABLE
            - INSTANCE_NOT_APPLICABLE
            - BUILT_INTO_BASE_STATE

    Notes
    -----
    This object can be accessed by:
        
    .. code-block:: python
        
        import load
        mdb.models[name].steps[name].loadStates[name]

    The corresponding analysis keywords are:

    - CLOAD

    """

    # A Float or a Complex specifying the concentrated force component in the 1-direction. 
    # Although *cf1*, *cf2*, and *cf3* are optional arguments, at least one of them must be 
    # nonzero. 
    cf1: float = None

    # A Float or a Complex specifying the concentrated force component in the 2-direction. 
    cf2: float = None

    # A Float or a Complex specifying the concentrated force component in the 3-direction. 
    cf3: float = None

    # A SymbolicConstant specifying the propagation state of the concentrated force component 
    # in the 1-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED. 
    cf1State: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the concentrated force component 
    # in the 2-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED. 
    cf2State: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the concentrated force component 
    # in the 3-direction. Possible values are UNSET, SET, UNCHANGED, and MODIFIED. 
    cf3State: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the *amplitude* member. Possible 
    # values are UNSET, SET, UNCHANGED, and FREED. 
    amplitudeState: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the LoadState object. Possible 
    # values are: 
    status: SymbolicConstant = None

    # A String specifying the name of the amplitude reference. The String is empty if the load 
    # has no amplitude reference. 
    # - NOT_YET_ACTIVE 
    # - CREATED 
    # - PROPAGATED 
    # - MODIFIED 
    # - DEACTIVATED 
    # - NO_LONGER_ACTIVE 
    # - TYPE_NOT_APPLICABLE 
    # - INSTANCE_NOT_APPLICABLE 
    # - BUILT_INTO_BASE_STATE 
    amplitude: str = ''
