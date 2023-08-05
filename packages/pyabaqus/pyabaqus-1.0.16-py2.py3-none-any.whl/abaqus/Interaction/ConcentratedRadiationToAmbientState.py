from abaqusConstants import *
from .InteractionState import InteractionState


class ConcentratedRadiationToAmbientState(InteractionState):
    """The ConcentratedRadiationToAmbientState object stores the propagating data for a
    ConcentratedRadiationToAmbient object. One instance of this object is created internally 
    by the ConcentratedRadiationToAmbient object for each step. The instance is also deleted 
    internally by the ConcentratedRadiationToAmbient object. 
    The ConcentratedRadiationToAmbientState object has no constructor or methods. 
    The ConcentratedRadiationToAmbientState object is derived from the InteractionState 
    object. 

    Attributes
    ----------
    ambientTemperature: float
        A Float specifying the ambient temperature.
    ambientTemperatureState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **ambientTemperature** member.
        Possible values are UNSET, SET, UNCHANGED, and FREED.
    ambientTemperatureAmpState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **ambientTemperatureAmp**
        member. Possible values are UNSET, SET, UNCHANGED, and FREED.
    emissivity: float
        A Float specifying the emissivity.
    emissivityState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **emissivity** member. Possible
        values are UNSET, SET, UNCHANGED, and FREED.
    nodalArea: float
        A Float specifying the area associated with the node where the concentrated radiation is
        applied.
    nodalAreaState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **nodalArea** member. Possible
        values are UNSET, SET, UNCHANGED, and FREED.
    ambientTemperatureAmp: str
        A String specifying the name of the :py:class:`~abaqus.Amplitude.Amplitude.Amplitude` object that gives the variation of the
        ambient temperature with time.
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

    - CRADIATE

    """

    # A Float specifying the ambient temperature. 
    ambientTemperature: float = None

    # A SymbolicConstant specifying the propagation state of the *ambientTemperature* member. 
    # Possible values are UNSET, SET, UNCHANGED, and FREED. 
    ambientTemperatureState: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the *ambientTemperatureAmp* 
    # member. Possible values are UNSET, SET, UNCHANGED, and FREED. 
    ambientTemperatureAmpState: SymbolicConstant = None

    # A Float specifying the emissivity. 
    emissivity: float = None

    # A SymbolicConstant specifying the propagation state of the *emissivity* member. Possible 
    # values are UNSET, SET, UNCHANGED, and FREED. 
    emissivityState: SymbolicConstant = None

    # A Float specifying the area associated with the node where the concentrated radiation is 
    # applied. 
    nodalArea: float = None

    # A SymbolicConstant specifying the propagation state of the *nodalArea* member. Possible 
    # values are UNSET, SET, UNCHANGED, and FREED. 
    nodalAreaState: SymbolicConstant = None

    # A String specifying the name of the Amplitude object that gives the variation of the 
    # ambient temperature with time. 
    ambientTemperatureAmp: str = ''

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
