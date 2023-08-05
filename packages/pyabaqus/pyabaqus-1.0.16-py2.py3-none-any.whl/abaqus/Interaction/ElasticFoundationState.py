from abaqusConstants import *
from .InteractionState import InteractionState


class ElasticFoundationState(InteractionState):
    """The ElasticFoundationState object stores the propagating data for an ElasticFoundation
    object. One instance of this object is created internally by the ElasticFoundation 
    object for each step. The instance is also deleted internally by the ElasticFoundation 
    object. 
    The ElasticFoundationState object has no constructor or methods. 
    The ElasticFoundationState object is derived from the InteractionState object. 

    Attributes
    ----------
    stiffness: float
        A Float specifying the foundation stiffness per area.
    stiffnessState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the stiffness member. Possible
        values are UNSET, SET, UNCHANGED, and FREED.
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

    """

    # A Float specifying the foundation stiffness per area. 
    stiffness: float = None

    # A SymbolicConstant specifying the propagation state of the stiffness member. Possible 
    # values are UNSET, SET, UNCHANGED, and FREED. 
    stiffnessState: SymbolicConstant = None

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
