from abaqusConstants import *
from .PredefinedFieldState import PredefinedFieldState


class TemperatureState(PredefinedFieldState):
    """The TemperatureState object stores the propagating data of a temperature in a step. One
    instance of this object is created internally by the Temperature object for each step. 
    The TemperatureState object has no constructor or methods. 
    The TemperatureState object is derived from the PredefinedFieldState object. 

    Attributes
    ----------
    fileNameState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **fileName** member. Possible
        values are UNSET, SET, and UNCHANGED.
    beginStep: SymbolicConstant
        A SymbolicConstant or an Int specifying the first step from which temperature values are
        to be read. This argument is valid only when **distribution=FROM_FILE** or
        **distribution=FROM_FILE_AND_USER_DEFINED**. Possible values are FIRST_STEP, LAST_STEP,
        and NONE. The default value is NONE.
    beginStepState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **beginStep** member. Possible
        values are UNSET, SET, and UNCHANGED.
    beginIncrement: SymbolicConstant
        None or an Int specifying the first increment of the step set in **beginStep** or the
        SymbolicConstants STEP_START or STEP_END. This argument is valid only when
        **distributionType=FROM_FILE** or **distributionType=FROM_FILE_AND_USER_DEFINED**. The
        default value is None.
    beginIncrementState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **beginIncrement** member.
        Possible values are UNSET, SET, and UNCHANGED.
    endStep: SymbolicConstant
        None or an Int specifying the last step from which temperature values are to be read or
        the SymbolicConstants FIRST_STEP and LAST_STEP. This argument is valid only when
        **distributionType=FROM_FILE** or **distributionType=FROM_FILE_AND_USER_DEFINED**. The
        default value is None.
    endStepState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **endStep** member. Possible
        values are UNSET, SET, and UNCHANGED.
    endIncrement: SymbolicConstant
        None or an Int specifying the last increment of the step set in **endStep** or the
        SymbolicConstants STEP_START and STEP_END. This argument is valid only when
        **distributionType=FROM_FILE** or **distributionType=FROM_FILE_AND_USER_DEFINED**. The
        default value is None.
    endIncrementState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **endIncrement** member.
        Possible values are UNSET, SET, and UNCHANGED.
    midside: Boolean
        A Boolean specifying that temperatures in second-order elements are to be interpolated
        from corner node temperatures. This argument is valid only when
        **distributionType=FROM_FILE** or **distributionType=FROM_FILE_AND_USER_DEFINED**.
    midsideState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **midside** member. Possible
        values are UNSET, SET, and UNCHANGED.
    amplitudeState: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the **amplitudeState** member.
        Possible values are UNSET, SET, and UNCHANGED.
    fileName: str
        A String specifying the name of the file from which the temperature values are to be
        read when **distributionType=FROM_FILE** or **distributionType=FROM_FILE_AND_USER_DEFINED**.
    amplitude: SymbolicConstant
        The SymbolicConstant UNSET or a String specifying the name of the amplitude reference.
        The SymbolicConstant UNSET should be used if the predefined field has no amplitude
        reference. The default value is UNSET.Note:**amplitude** should be given only if it is
        valid for the specified step.
    magnitudesState: SymbolicConstant
        A tuple of SymbolicConstants specifying the propagation state of each item of the
        **magnitudes** member. Possible values are UNSET, SET, and UNCHANGED.
    magnitudes: tuple
        A tuple of Floats specifying the temperature values when **distributionType=UNIFORM** or
        **distributionType=FIELD**. The value of the **magnitudes** argument is a function of the
        **crossSectionDistribution** argument, as shown in the following list:
            - If **crossSectionDistribution=CONSTANT_THROUGH_THICKNESS** then **magnitudes** is a Double
        specifying the temperature.
            - If **crossSectionDistribution=GRADIENTS_THROUGH_SHELL_CS** then **magnitudes** is a
        sequence of Doubles specifying the mean value and the gradient in the thickness
        direction.
            - If **crossSectionDistribution=GRADIENTS_THROUGH_BEAM_CS** then **magnitudes** is a
        sequence of Doubles specifying the mean value, the gradient in the N1 direction, and the
        gradient in the N2 direction.
            - If **crossSectionDistribution=POINTS_THROUGH_SECTION** then **magnitudes** is a sequence
        of Doubles specifying the temperature at each point.
    status: SymbolicConstant
        A SymbolicConstant specifying the propagation state of the :py:class:`~abaqus.PredefinedField.:py:class:`~abaqus.PredefinedField.PredefinedFieldState.PredefinedFieldState`.:py:class:`~abaqus.PredefinedField.PredefinedFieldState.PredefinedFieldState`` object.
        Possible values are:
            - NOT_YET_ACTIVE
            - CREATED
            - PROPAGATED
            - MODIFIED
            - DEACTIVATED
            - DEACTIVATED_TO_INITIAL
            - NO_LONGER_ACTIVE
            - RESET_TO_INITIAL
            - TO_BE_COMPUTED
            - PROPAGATED_FROM_COMPUTED
            - BUILT_INTO_BASE_STATE
            - TYPE_NOT_APPLICABLE
            - INSTANCE_NOT_APPLICABLE
        This member exists in all :py:class:`~abaqus.PredefinedField.:py:class:`~abaqus.PredefinedField.PredefinedFieldState.PredefinedFieldState`.:py:class:`~abaqus.PredefinedField.PredefinedFieldState.PredefinedFieldState`` objects, but different predefined fields
        use different subsets of the entire list of possible values depending on propagation
        rules.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import load
        mdb.models[name].steps[name].predefinedFieldStates[name]

    """

    # A SymbolicConstant specifying the propagation state of the *fileName* member. Possible 
    # values are UNSET, SET, and UNCHANGED. 
    fileNameState: SymbolicConstant = None

    # A SymbolicConstant or an Int specifying the first step from which temperature values are 
    # to be read. This argument is valid only when *distribution*=FROM_FILE or 
    # *distribution*=FROM_FILE_AND_USER_DEFINED. Possible values are FIRST_STEP, LAST_STEP, 
    # and NONE. The default value is NONE. 
    beginStep: SymbolicConstant = NONE

    # A SymbolicConstant specifying the propagation state of the *beginStep* member. Possible 
    # values are UNSET, SET, and UNCHANGED. 
    beginStepState: SymbolicConstant = None

    # None or an Int specifying the first increment of the step set in *beginStep* or the 
    # SymbolicConstants STEP_START or STEP_END. This argument is valid only when 
    # *distributionType*=FROM_FILE or *distributionType*=FROM_FILE_AND_USER_DEFINED. The 
    # default value is None. 
    beginIncrement: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the *beginIncrement* member. 
    # Possible values are UNSET, SET, and UNCHANGED. 
    beginIncrementState: SymbolicConstant = None

    # None or an Int specifying the last step from which temperature values are to be read or 
    # the SymbolicConstants FIRST_STEP and LAST_STEP. This argument is valid only when 
    # *distributionType*=FROM_FILE or *distributionType*=FROM_FILE_AND_USER_DEFINED. The 
    # default value is None. 
    endStep: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the *endStep* member. Possible 
    # values are UNSET, SET, and UNCHANGED. 
    endStepState: SymbolicConstant = None

    # None or an Int specifying the last increment of the step set in *endStep* or the 
    # SymbolicConstants STEP_START and STEP_END. This argument is valid only when 
    # *distributionType*=FROM_FILE or *distributionType*=FROM_FILE_AND_USER_DEFINED. The 
    # default value is None. 
    endIncrement: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the *endIncrement* member. 
    # Possible values are UNSET, SET, and UNCHANGED. 
    endIncrementState: SymbolicConstant = None

    # A Boolean specifying that temperatures in second-order elements are to be interpolated 
    # from corner node temperatures. This argument is valid only when 
    # *distributionType*=FROM_FILE or *distributionType*=FROM_FILE_AND_USER_DEFINED. 
    midside: Boolean = OFF

    # A SymbolicConstant specifying the propagation state of the *midside* member. Possible 
    # values are UNSET, SET, and UNCHANGED. 
    midsideState: SymbolicConstant = None

    # A SymbolicConstant specifying the propagation state of the *amplitudeState* member. 
    # Possible values are UNSET, SET, and UNCHANGED. 
    amplitudeState: SymbolicConstant = None

    # A String specifying the name of the file from which the temperature values are to be 
    # read when *distributionType*=FROM_FILE or *distributionType*=FROM_FILE_AND_USER_DEFINED. 
    fileName: str = ''

    # The SymbolicConstant UNSET or a String specifying the name of the amplitude reference. 
    # The SymbolicConstant UNSET should be used if the predefined field has no amplitude 
    # reference. The default value is UNSET.Note:*amplitude* should be given only if it is 
    # valid for the specified step. 
    amplitude: SymbolicConstant = UNSET

    # A tuple of SymbolicConstants specifying the propagation state of each item of the 
    # *magnitudes* member. Possible values are UNSET, SET, and UNCHANGED. 
    magnitudesState: SymbolicConstant = None

    # A tuple of Floats specifying the temperature values when *distributionType*=UNIFORM or 
    # *distributionType*=FIELD. The value of the *magnitudes* argument is a function of the 
    # *crossSectionDistribution* argument, as shown in the following list: 
    # - If *crossSectionDistribution*=CONSTANT_THROUGH_THICKNESS then *magnitudes* is a Double 
    # specifying the temperature. 
    # - If *crossSectionDistribution*=GRADIENTS_THROUGH_SHELL_CS then *magnitudes* is a 
    # sequence of Doubles specifying the mean value and the gradient in the thickness 
    # direction. 
    # - If *crossSectionDistribution*=GRADIENTS_THROUGH_BEAM_CS then *magnitudes* is a 
    # sequence of Doubles specifying the mean value, the gradient in the N1 direction, and the 
    # gradient in the N2 direction. 
    # - If *crossSectionDistribution*=POINTS_THROUGH_SECTION then *magnitudes* is a sequence 
    # of Doubles specifying the temperature at each point. 
    magnitudes: tuple = ()

    # A SymbolicConstant specifying the propagation state of the PredefinedFieldState object. 
    # Possible values are: 
    # - NOT_YET_ACTIVE 
    # - CREATED 
    # - PROPAGATED 
    # - MODIFIED 
    # - DEACTIVATED 
    # - DEACTIVATED_TO_INITIAL 
    # - NO_LONGER_ACTIVE 
    # - RESET_TO_INITIAL 
    # - TO_BE_COMPUTED 
    # - PROPAGATED_FROM_COMPUTED 
    # - BUILT_INTO_BASE_STATE 
    # - TYPE_NOT_APPLICABLE 
    # - INSTANCE_NOT_APPLICABLE 
    # This member exists in all PredefinedFieldState objects, but different predefined fields 
    # use different subsets of the entire list of possible values depending on propagation 
    # rules. 
    status: SymbolicConstant = None
