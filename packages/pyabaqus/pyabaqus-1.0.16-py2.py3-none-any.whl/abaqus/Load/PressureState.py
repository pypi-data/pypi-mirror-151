from abaqusConstants import *
from .LoadState import LoadState


class PressureState(LoadState):
    """The PressureState object stores the propagating data for a pressure in a step. One
    instance of this object is created internally by the Pressure object for each step. The 
    instance is also deleted internally by the Pressure object. 
    The PressureState object has no constructor or methods. 
    The PressureState object is derived from the LoadState object. 

    Attributes
    ----------
    magnitude: float
        A Float or a Complex specifying the pressure magnitude.
    magnitudeState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the pressure magnitude. Possible
        values are UNSET, SET, UNCHANGED, and MODIFIED.
    hZero: float
        A Float specifying the height of the zero pressure level when the pressure
        **distributionType=HYDROSTATIC**.
    hZeroState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of **hZero**. Possible values are
        UNSET, SET, UNCHANGED, and FREED.
    hReference: float
        A Float specifying the height of the reference pressure level when the pressure
        **distributionType=HYDROSTATIC**.
    hReferenceState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of **hReference**. Possible values are
        UNSET, SET, UNCHANGED, and FREED.
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

    - DSLOAD
            - DLOAD

    """

    # A Float or a Complex specifying the pressure magnitude. 
    magnitude: float = None

    # A SymbolicConstant specifying the propagation state of the pressure magnitude. Possible 
    # values are UNSET, SET, UNCHANGED, and MODIFIED. 
    magnitudeState: SymbolicConstant = None

    # A Float specifying the height of the zero pressure level when the pressure 
    # *distributionType*=HYDROSTATIC. 
    hZero: float = None

    # A SymbolicConstant specifying the propagation state of *hZero*. Possible values are 
    # UNSET, SET, UNCHANGED, and FREED. 
    hZeroState: SymbolicConstant = None

    # A Float specifying the height of the reference pressure level when the pressure 
    # *distributionType*=HYDROSTATIC. 
    hReference: float = None

    # A SymbolicConstant specifying the propagation state of *hReference*. Possible values are 
    # UNSET, SET, UNCHANGED, and FREED. 
    hReferenceState: SymbolicConstant = None

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
