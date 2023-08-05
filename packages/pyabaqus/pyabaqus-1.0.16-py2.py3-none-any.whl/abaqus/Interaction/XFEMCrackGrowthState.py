from abaqusConstants import *
from .InteractionState import InteractionState


class XFEMCrackGrowthState(InteractionState):
    """The XFEMCrackGrowthState object stores the propagating data of an XFEMCrackGrowth object
    in a step. One instance of this object is created internally by the XFEMCrackGrowth 
    object for each step. The instance is also deleted internally by the XFEMCrackGrowth 
    object. 
    The XFEMCrackGrowthState object has no constructor or methods. 
    The XFEMCrackGrowthState object is derived from the InteractionState object. 

    Attributes
    ----------
    allowGrowth: Boolean
        A Boolean specifying whether the crack is allowed to grow (propagate) during this
        analysis step. The default value is ON.
    allowGrowthState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **allowGrowth** member.
        Possible values are UNSET, SET, UNCHANGED, and FREED.
    status: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the :py:class:`~abaqus.Interaction.InteractionState.InteractionState` object.
        Possible values are:
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
        
        import interaction
        mdb.models[name].steps[name].interactionStates[name]

    The corresponding analysis keywords are:

    - ENRICHMENT ACTIVATION

    """

    # A Boolean specifying whether the crack is allowed to grow (propagate) during this 
    # analysis step. The default value is ON. 
    allowGrowth: Boolean = ON

    # A SymbolicConstant specifying the propagation state of the *allowGrowth* member. 
    # Possible values are UNSET, SET, UNCHANGED, and FREED. 
    allowGrowthState: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the InteractionState object. 
    # Possible values are: 
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
