from abaqusConstants import *
from .InteractionState import InteractionState


class IncidentWaveState(InteractionState):
    """The IncidentWaveState object stores the propagating data of an IncidentWave object in a
    step. One instance of this object is created internally by the IncidentWave object for 
    each step. The instance is also deleted internally by the IncidentWave object. 
    The IncidentWaveState object has no constructor or methods. 
    The IncidentWaveState object is derived from the InteractionState object. 

    Attributes
    ----------
    status: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the :py:class:`~abaqus.Interaction.InteractionState.InteractionState` object.
        Possible values
        are:NOT_YET_ACTIVECREATEDPROPAGATEDMODIFIEDDEACTIVATEDNO_LONGER_ACTIVETYPE_NOT_APPLICABLEINSTANCE_NOT_APPLICABLEBUILT_INTO_BASE_STATE

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import interaction
        mdb.models[name].steps[name].interactionStates[name]

    The corresponding analysis keywords are:

    - INCIDENT WAVE INTERACTION

    """

    # A SymbolicConstant specifying the propagation state of the InteractionState object. 
    # Possible values 
    # are:NOT_YET_ACTIVECREATEDPROPAGATEDMODIFIEDDEACTIVATEDNO_LONGER_ACTIVETYPE_NOT_APPLICABLEINSTANCE_NOT_APPLICABLEBUILT_INTO_BASE_STATE 
    status: SymbolicConstant = None
