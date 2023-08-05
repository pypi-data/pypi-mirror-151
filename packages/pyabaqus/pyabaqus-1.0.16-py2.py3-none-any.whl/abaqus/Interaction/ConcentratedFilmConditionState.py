from abaqusConstants import *
from .InteractionState import InteractionState


class ConcentratedFilmConditionState(InteractionState):
    """The ConcentratedFilmConditionState object stores the propagating data for a
    ConcentratedFilmCondition object. One instance of this object is created internally by 
    the ConcentratedFilmCondition object for each step. The instance is also deleted 
    internally by the ConcentratedFilmCondition object. 
    The ConcentratedFilmConditionState object has no constructor or methods. 
    The ConcentratedFilmConditionState object is derived from the InteractionState object. 

    Attributes
    ----------
    interactionPropertyState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **interactionProperty** member.
        Possible values are UNSET, SET, UNCHANGED, and FREED.
    sinkTemperature: float
        A Float specifying the sink temperature.
    sinkTemperatureState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **sinkTemperature** member.
        Possible values are UNSET, SET, UNCHANGED, and FREED.
    sinkAmplitudeState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **sinkAmplitude** member.
        Possible values are UNSET, SET, UNCHANGED, and FREED.
    filmCoeff: float
        A Float specifying the film coefficient.
    filmCoeffState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **filmCoeff** member. Possible
        values are UNSET, SET, UNCHANGED, and FREED.
    filmCoeffAmplitudeState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **filmCoeffAmplitude** member.
        Possible values are UNSET, SET, UNCHANGED, and FREED.
    nodalArea: float
        A Float specifying the area associated with the node where the concentrated film
        condition is applied.
    nodalAreaState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **nodalArea** member. Possible
        values are UNSET, SET, UNCHANGED, and FREED.
    interactionProperty: str
        A String specifying the :py:class:`~abaqus.Interaction.FilmConditionProp.FilmConditionProp` object associated with this interaction.
    sinkAmplitude: str
        A String specifying the name of the :py:class:`~abaqus.Amplitude.Amplitude.Amplitude` object that gives the variation of the
        sink temperature.
    filmCoeffAmplitude: str
        A String specifying the name of the :py:class:`~abaqus.Amplitude.Amplitude.Amplitude` object that gives the variation of the
        film coefficient.
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

    - CFILM

    """

    # A SymbolicConstant specifying the propagation state of the *interactionProperty* member. 
    # Possible values are UNSET, SET, UNCHANGED, and FREED. 
    interactionPropertyState: SymbolicConstant = None

    # A Float specifying the sink temperature. 
    sinkTemperature: float = None

    # A SymbolicConstant specifying the propagation state of the *sinkTemperature* member. 
    # Possible values are UNSET, SET, UNCHANGED, and FREED. 
    sinkTemperatureState: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the *sinkAmplitude* member. 
    # Possible values are UNSET, SET, UNCHANGED, and FREED. 
    sinkAmplitudeState: SymbolicConstant = None

    # A Float specifying the film coefficient. 
    filmCoeff: float = None

    # A SymbolicConstant specifying the propagation state of the *filmCoeff* member. Possible 
    # values are UNSET, SET, UNCHANGED, and FREED. 
    filmCoeffState: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the *filmCoeffAmplitude* member. 
    # Possible values are UNSET, SET, UNCHANGED, and FREED. 
    filmCoeffAmplitudeState: SymbolicConstant = None

    # A Float specifying the area associated with the node where the concentrated film 
    # condition is applied. 
    nodalArea: float = None

    # A SymbolicConstant specifying the propagation state of the *nodalArea* member. Possible 
    # values are UNSET, SET, UNCHANGED, and FREED. 
    nodalAreaState: SymbolicConstant = None

    # A String specifying the FilmConditionProp object associated with this interaction. 
    interactionProperty: str = ''

    # A String specifying the name of the Amplitude object that gives the variation of the 
    # sink temperature. 
    sinkAmplitude: str = ''

    # A String specifying the name of the Amplitude object that gives the variation of the 
    # film coefficient. 
    filmCoeffAmplitude: str = ''

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
