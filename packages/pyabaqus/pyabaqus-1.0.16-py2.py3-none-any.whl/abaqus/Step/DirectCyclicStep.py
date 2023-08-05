from abaqusConstants import *
from .AnalysisStep import AnalysisStep
from ..Adaptivity.AdaptiveMeshConstraintState import AdaptiveMeshConstraintState
from ..Adaptivity.AdaptiveMeshDomain import AdaptiveMeshDomain
from ..BoundaryCondition.BoundaryConditionState import BoundaryConditionState
from ..Load.LoadCase import LoadCase
from ..Load.LoadState import LoadState
from ..PredefinedField.PredefinedFieldState import PredefinedFieldState
from ..StepMiscellaneous.Control import Control
from ..StepMiscellaneous.SolverControl import SolverControl
from ..StepOutput.DiagnosticPrint import DiagnosticPrint
from ..StepOutput.FieldOutputRequestState import FieldOutputRequestState
from ..StepOutput.HistoryOutputRequestState import HistoryOutputRequestState
from ..StepOutput.Monitor import Monitor
from ..StepOutput.Restart import Restart


class DirectCyclicStep(AnalysisStep):
    """The DirectCyclicStep object is used to provide a direct cyclic procedure for nonlinear,
    non-isothermal quasi-static analysis. It can also be used to predict progressive damage 
    and failure for ductile bulk materials and/or to predict delamination/debonding growth 
    at the interfaces in laminated composites in a low-cycle fatigue analysis. 
    The DirectCyclicStep object is derived from the AnalysisStep object. 

    Attributes
    ----------
    name: str
        A String specifying the repository key.
    timePeriod: float
        A Float specifying the time of single loading cycle. The default value is 1.0.
    timeIncrementationMethod: SymbolicConstant
        A SymbolicConstant specifying the time incrementation method to be used. Possible values
        are FIXED and AUTOMATIC. The default value is AUTOMATIC.
    maxNumInc: int
        An Int specifying the maximum number of increments in a step. The default value is 100.
    initialInc: float
        A Float specifying the initial time increment. The default value is the total time
        period for the step.
    minInc: float
        A Float specifying the minimum time increment allowed. The default value is the smaller
        of the suggested initial time increment or 10−5 times the total time period.
    maxInc: float
        A Float specifying the maximum time increment allowed. The default value is the total
        time period for the step.
    maxNumIterations: int
        An Int specifying the maximum number of iterations in a step. The default value is 200.
    initialTerms: int
        An Int specifying the initial number of terms in the Fourier series. The default value
        is 11.
    maxTerms: int
        An Int specifying the maximum number of terms in the Fourier series. The default value
        is 25.
    termsIncrement: int
        An Int specifying the increment in number of terms in the Fourier series. The default
        value is 5.
    deltmx: float
        A Float specifying the maximum temperature change to be allowed in an increment. The
        default value is 0.0.
    cetol: float
        A Float specifying the maximum difference in the creep strain increment calculated from
        the creep strain rates at the beginning and end of the increment. The default value is
        0.0.
    fatigue: Boolean
        A Boolean specifying whether to include low-cycle fatigue analysis. The default value is
        OFF.
    continueAnalysis: Boolean
        A Boolean specifying whether the displacement solution in the Fourier series obtained in
        the previous direct cyclic step is used as the starting values for the current step. The
        default value is OFF.
    minCycleInc: int
        An Int specifying the minimum number of cycles over which the damage is extrapolated
        forward. The default value is 100.
    maxCycleInc: int
        An Int specifying the maximum number of cycles over which the damage is extrapolated
        forward. The default value is 1000.
    maxNumCycles: SymbolicConstant
        The SymbolicConstant DEFAULT or an Int specifying the maximum number of cycles allowed
        in a step or DEFAULT. A value of 1 plus half of the maximum number of cycles will be
        used if DEFAULT is specified. The default value is DEFAULT.
    damageExtrapolationTolerance: float
        A Float specifying the maximum extrapolated damage increment. The default value is 1.0.
    matrixStorage: SymbolicConstant
        A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC,
        UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT.
    extrapolation: SymbolicConstant
        A SymbolicConstant specifying the type of extrapolation to use in determining the
        incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, and
        PARABOLIC. The default value is LINEAR.
    convertSDI: SymbolicConstant
        A SymbolicConstant specifying whether to force a new iteration if severe discontinuities
        occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and
        CONVERT_SDI_ON. The default value is PROPAGATED.
    previous: str
        A String specifying the name of the previous step. The new step appears after this step
        in the list of analysis steps.
    description: str
        A String specifying a description of the new step. The default value is an empty string.
    timePoints: str
        None or a String specifying a String specifying the name of a time :py:class:`~.point` object used to
        determine at which times the response of the structure will be evaluated. The default
        value is NONE.
    explicit: SymbolicConstant
        A SymbolicConstant specifying whether the step has an explicit procedure type
        (**procedureType=ANNEAL**, DYNAMIC_EXPLICIT, or DYNAMIC_TEMP_DISPLACEMENT).
    perturbation: Boolean
        A Boolean specifying whether the step has a perturbation procedure type.
    nonmechanical: Boolean
        A Boolean specifying whether the step has a mechanical procedure type.
    procedureType: SymbolicConstant
        A SymbolicConstant specifying the Abaqus procedure. Possible values are:
            - ANNEAL
            - BUCKLE
            - COMPLEX_FREQUENCY
            - COUPLED_TEMP_DISPLACEMENT
            - COUPLED_THERMAL_ELECTRIC
            - DIRECT_CYCLIC
            - DYNAMIC_IMPLICIT
            - DYNAMIC_EXPLICIT
            - DYNAMIC_SUBSPACE
            - DYNAMIC_TEMP_DISPLACEMENT
            - COUPLED_THERMAL_ELECTRICAL_STRUCTURAL
            - FREQUENCY
            - GEOSTATIC
            - HEAT_TRANSFER
            - MASS_DIFFUSION
            - MODAL_DYNAMICS
            - RANDOM_RESPONSE
            - RESPONSE_SPECTRUM
            - SOILS
            - STATIC_GENERAL
            - STATIC_LINEAR_PERTURBATION
            - STATIC_RIKS
            - STEADY_STATE_DIRECT
            - STEADY_STATE_MODAL
            - STEADY_STATE_SUBSPACE
            - VISCO
    suppressed: Boolean
        A Boolean specifying whether the step is suppressed or not. The default value is OFF.
    fieldOutputRequestState: dict[str, FieldOutputRequestState]
        A repository of :py:class:`~abaqus.StepOutput.FieldOutputRequestState.FieldOutputRequestState` objects.
    historyOutputRequestState: dict[str, HistoryOutputRequestState]
        A repository of :py:class:`~abaqus.StepOutput.HistoryOutputRequestState.HistoryOutputRequestState` objects.
    diagnosticPrint: DiagnosticPrint
        A :py:class:`~abaqus.StepOutput.DiagnosticPrint.DiagnosticPrint` object.
    monitor: Monitor
        A :py:class:`~abaqus.StepOutput.Monitor.Monitor` object.
    restart: Restart
        A :py:class:`~abaqus.StepOutput.Restart.Restart` object.
    adaptiveMeshConstraintStates: dict[str, AdaptiveMeshConstraintState]
        A repository of :py:class:`~abaqus.Adaptivity.AdaptiveMeshConstraintState.AdaptiveMeshConstraintState` objects.
    adaptiveMeshDomains: dict[str, AdaptiveMeshDomain]
        A repository of :py:class:`~abaqus.Adaptivity.AdaptiveMeshDomain.AdaptiveMeshDomain` objects.
    control: Control
        A :py:class:`~abaqus.StepMiscellaneous.Control.Control` object.
    solverControl: SolverControl
        A :py:class:`~abaqus.StepMiscellaneous.SolverControl.SolverControl` object.
    boundaryConditionStates: dict[str, BoundaryConditionState]
        A repository of :py:class:`~abaqus.BoundaryCondition.BoundaryConditionState.BoundaryConditionState` objects.
    interactionStates: int
        A repository of :py:class:`~abaqus.Interaction.InteractionState.InteractionState` objects.
    loadStates: dict[str, LoadState]
        A repository of :py:class:`~abaqus.Load.LoadState.LoadState` objects.
    loadCases: dict[str, LoadCase]
        A repository of :py:class:`~abaqus.Load.LoadCase.LoadCase` objects.
    predefinedFieldStates: dict[str, PredefinedFieldState]
        A repository of :py:class:`~abaqus.PredefinedField.PredefinedFieldState.PredefinedFieldState` objects.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import step
        mdb.models[name].steps[name]

    The corresponding analysis keywords are:

    - DIRECT CYCLIC
            - STEP

    """

    # A String specifying the repository key. 
    name: str = ''

    # A Float specifying the time of single loading cycle. The default value is 1.0. 
    timePeriod: float = 1

    # A SymbolicConstant specifying the time incrementation method to be used. Possible values 
    # are FIXED and AUTOMATIC. The default value is AUTOMATIC. 
    timeIncrementationMethod: SymbolicConstant = AUTOMATIC

    # An Int specifying the maximum number of increments in a step. The default value is 100. 
    maxNumInc: int = 100

    # A Float specifying the initial time increment. The default value is the total time 
    # period for the step. 
    initialInc: float = None

    # A Float specifying the minimum time increment allowed. The default value is the smaller 
    # of the suggested initial time increment or 10−5 times the total time period. 
    minInc: float = None

    # A Float specifying the maximum time increment allowed. The default value is the total 
    # time period for the step. 
    maxInc: float = None

    # An Int specifying the maximum number of iterations in a step. The default value is 200. 
    maxNumIterations: int = 200

    # An Int specifying the initial number of terms in the Fourier series. The default value 
    # is 11. 
    initialTerms: int = 11

    # An Int specifying the maximum number of terms in the Fourier series. The default value 
    # is 25. 
    maxTerms: int = 25

    # An Int specifying the increment in number of terms in the Fourier series. The default 
    # value is 5. 
    termsIncrement: int = 5

    # A Float specifying the maximum temperature change to be allowed in an increment. The 
    # default value is 0.0. 
    deltmx: float = 0

    # A Float specifying the maximum difference in the creep strain increment calculated from 
    # the creep strain rates at the beginning and end of the increment. The default value is 
    # 0.0. 
    cetol: float = 0

    # A Boolean specifying whether to include low-cycle fatigue analysis. The default value is 
    # OFF. 
    fatigue: Boolean = OFF

    # A Boolean specifying whether the displacement solution in the Fourier series obtained in 
    # the previous direct cyclic step is used as the starting values for the current step. The 
    # default value is OFF. 
    continueAnalysis: Boolean = OFF

    # An Int specifying the minimum number of cycles over which the damage is extrapolated 
    # forward. The default value is 100. 
    minCycleInc: int = 100

    # An Int specifying the maximum number of cycles over which the damage is extrapolated 
    # forward. The default value is 1000. 
    maxCycleInc: int = 1000

    # The SymbolicConstant DEFAULT or an Int specifying the maximum number of cycles allowed 
    # in a step or DEFAULT. A value of 1 plus half of the maximum number of cycles will be 
    # used if DEFAULT is specified. The default value is DEFAULT. 
    maxNumCycles: SymbolicConstant = DEFAULT

    # A Float specifying the maximum extrapolated damage increment. The default value is 1.0. 
    damageExtrapolationTolerance: float = 1

    # A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
    # UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
    matrixStorage: SymbolicConstant = SOLVER_DEFAULT

    # A SymbolicConstant specifying the type of extrapolation to use in determining the 
    # incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, and 
    # PARABOLIC. The default value is LINEAR. 
    extrapolation: SymbolicConstant = LINEAR

    # A SymbolicConstant specifying whether to force a new iteration if severe discontinuities 
    # occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and 
    # CONVERT_SDI_ON. The default value is PROPAGATED. 
    convertSDI: SymbolicConstant = PROPAGATED

    # A String specifying the name of the previous step. The new step appears after this step 
    # in the list of analysis steps. 
    previous: str = ''

    # A String specifying a description of the new step. The default value is an empty string. 
    description: str = ''

    # None or a String specifying a String specifying the name of a time point object used to 
    # determine at which times the response of the structure will be evaluated. The default 
    # value is NONE. 
    timePoints: str = NONE

    # A SymbolicConstant specifying whether the step has an explicit procedure type 
    # (*procedureType*=ANNEAL, DYNAMIC_EXPLICIT, or DYNAMIC_TEMP_DISPLACEMENT). 
    explicit: SymbolicConstant = None

    # A Boolean specifying whether the step has a perturbation procedure type. 
    perturbation: Boolean = OFF

    # A Boolean specifying whether the step has a mechanical procedure type. 
    nonmechanical: Boolean = OFF

    # A SymbolicConstant specifying the Abaqus procedure. Possible values are: 
    # - ANNEAL 
    # - BUCKLE 
    # - COMPLEX_FREQUENCY 
    # - COUPLED_TEMP_DISPLACEMENT 
    # - COUPLED_THERMAL_ELECTRIC 
    # - DIRECT_CYCLIC 
    # - DYNAMIC_IMPLICIT 
    # - DYNAMIC_EXPLICIT 
    # - DYNAMIC_SUBSPACE 
    # - DYNAMIC_TEMP_DISPLACEMENT 
    # - COUPLED_THERMAL_ELECTRICAL_STRUCTURAL 
    # - FREQUENCY 
    # - GEOSTATIC 
    # - HEAT_TRANSFER 
    # - MASS_DIFFUSION 
    # - MODAL_DYNAMICS 
    # - RANDOM_RESPONSE 
    # - RESPONSE_SPECTRUM 
    # - SOILS 
    # - STATIC_GENERAL 
    # - STATIC_LINEAR_PERTURBATION 
    # - STATIC_RIKS 
    # - STEADY_STATE_DIRECT 
    # - STEADY_STATE_MODAL 
    # - STEADY_STATE_SUBSPACE 
    # - VISCO 
    procedureType: SymbolicConstant = None

    # A Boolean specifying whether the step is suppressed or not. The default value is OFF. 
    suppressed: Boolean = OFF

    # A repository of FieldOutputRequestState objects. 
    fieldOutputRequestState: dict[str, FieldOutputRequestState] = dict[str, FieldOutputRequestState]()

    # A repository of HistoryOutputRequestState objects. 
    historyOutputRequestState: dict[str, HistoryOutputRequestState] = dict[str, HistoryOutputRequestState]()

    # A DiagnosticPrint object. 
    diagnosticPrint: DiagnosticPrint = DiagnosticPrint()

    # A Monitor object. 
    monitor: Monitor = None

    # A Restart object. 
    restart: Restart = Restart()

    # A repository of AdaptiveMeshConstraintState objects. 
    adaptiveMeshConstraintStates: dict[str, AdaptiveMeshConstraintState] = dict[
        str, AdaptiveMeshConstraintState]()

    # A repository of AdaptiveMeshDomain objects. 
    adaptiveMeshDomains: dict[str, AdaptiveMeshDomain] = dict[str, AdaptiveMeshDomain]()

    # A Control object. 
    control: Control = Control()

    # A SolverControl object. 
    solverControl: SolverControl = SolverControl()

    # A repository of BoundaryConditionState objects. 
    boundaryConditionStates: dict[str, BoundaryConditionState] = dict[str, BoundaryConditionState]()

    # A repository of InteractionState objects. 
    interactionStates: int = None

    # A repository of LoadState objects. 
    loadStates: dict[str, LoadState] = dict[str, LoadState]()

    # A repository of LoadCase objects. 
    loadCases: dict[str, LoadCase] = dict[str, LoadCase]()

    # A repository of PredefinedFieldState objects. 
    predefinedFieldStates: dict[str, PredefinedFieldState] = dict[str, PredefinedFieldState]()

    def __init__(self, name: str, previous: str, description: str = '', timePeriod: float = 1,
                 timeIncrementationMethod: SymbolicConstant = AUTOMATIC, maxNumInc: int = 100,
                 initialInc: float = None, minInc: float = None, maxInc: float = None,
                 maxNumIterations: int = 200, initialTerms: int = 11, maxTerms: int = 25,
                 termsIncrement: int = 5, deltmx: float = 0, cetol: float = 0, timePoints: str = NONE,
                 fatigue: Boolean = OFF, continueAnalysis: Boolean = OFF, minCycleInc: int = 100,
                 maxCycleInc: int = 1000, maxNumCycles: SymbolicConstant = DEFAULT,
                 damageExtrapolationTolerance: float = 1,
                 matrixStorage: SymbolicConstant = SOLVER_DEFAULT,
                 extrapolation: SymbolicConstant = LINEAR, maintainAttributes: Boolean = False,
                 convertSDI: SymbolicConstant = PROPAGATED):
        """This method creates a DirectCyclicStep object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].DirectCyclicStep
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        previous
            A String specifying the name of the previous step. The new step appears after this step 
            in the list of analysis steps. 
        description
            A String specifying a description of the new step. The default value is an empty string. 
        timePeriod
            A Float specifying the time of single loading cycle. The default value is 1.0. 
        timeIncrementationMethod
            A SymbolicConstant specifying the time incrementation method to be used. Possible values 
            are FIXED and AUTOMATIC. The default value is AUTOMATIC. 
        maxNumInc
            An Int specifying the maximum number of increments in a step. The default value is 100. 
        initialInc
            A Float specifying the initial time increment. The default value is the total time 
            period for the step. 
        minInc
            A Float specifying the minimum time increment allowed. The default value is the smaller 
            of the suggested initial time increment or 10−5 times the total time period. 
        maxInc
            A Float specifying the maximum time increment allowed. The default value is the total 
            time period for the step. 
        maxNumIterations
            An Int specifying the maximum number of iterations in a step. The default value is 200. 
        initialTerms
            An Int specifying the initial number of terms in the Fourier series. The default value 
            is 11. 
        maxTerms
            An Int specifying the maximum number of terms in the Fourier series. The default value 
            is 25. 
        termsIncrement
            An Int specifying the increment in number of terms in the Fourier series. The default 
            value is 5. 
        deltmx
            A Float specifying the maximum temperature change to be allowed in an increment. The 
            default value is 0.0. 
        cetol
            A Float specifying the maximum difference in the creep strain increment calculated from 
            the creep strain rates at the beginning and end of the increment. The default value is 
            0.0. 
        timePoints
            None or a String specifying a String specifying the name of a time point object used to 
            determine at which times the response of the structure will be evaluated. The default 
            value is NONE. 
        fatigue
            A Boolean specifying whether to include low-cycle fatigue analysis. The default value is 
            OFF. 
        continueAnalysis
            A Boolean specifying whether the displacement solution in the Fourier series obtained in 
            the previous direct cyclic step is used as the starting values for the current step. The 
            default value is OFF. 
        minCycleInc
            An Int specifying the minimum number of cycles over which the damage is extrapolated 
            forward. The default value is 100. 
        maxCycleInc
            An Int specifying the maximum number of cycles over which the damage is extrapolated 
            forward. The default value is 1000. 
        maxNumCycles
            The SymbolicConstant DEFAULT or an Int specifying the maximum number of cycles allowed 
            in a step or DEFAULT. A value of 1 plus half of the maximum number of cycles will be 
            used if DEFAULT is specified. The default value is DEFAULT. 
        damageExtrapolationTolerance
            A Float specifying the maximum extrapolated damage increment. The default value is 1.0. 
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
        extrapolation
            A SymbolicConstant specifying the type of extrapolation to use in determining the 
            incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, and 
            PARABOLIC. The default value is LINEAR. 
        maintainAttributes
            A Boolean specifying whether to retain attributes from an existing step with the same 
            name. The default value is False. 
        convertSDI
            A SymbolicConstant specifying whether to force a new iteration if severe discontinuities 
            occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and 
            CONVERT_SDI_ON. The default value is PROPAGATED. 

        Returns
        -------
            A DirectCyclicStep object. 

        Raises
        ------
        RangeError
        """
        super().__init__()
        pass

    def setValues(self, description: str = '', timePeriod: float = 1,
                  timeIncrementationMethod: SymbolicConstant = AUTOMATIC, maxNumInc: int = 100,
                  initialInc: float = None, minInc: float = None, maxInc: float = None,
                  maxNumIterations: int = 200, initialTerms: int = 11, maxTerms: int = 25,
                  termsIncrement: int = 5, deltmx: float = 0, cetol: float = 0, timePoints: str = NONE,
                  fatigue: Boolean = OFF, continueAnalysis: Boolean = OFF, minCycleInc: int = 100,
                  maxCycleInc: int = 1000, maxNumCycles: SymbolicConstant = DEFAULT,
                  damageExtrapolationTolerance: float = 1,
                  matrixStorage: SymbolicConstant = SOLVER_DEFAULT,
                  extrapolation: SymbolicConstant = LINEAR, convertSDI: SymbolicConstant = PROPAGATED):
        """This method modifies the DirectCyclicStep object.
        
        Parameters
        ----------
        description
            A String specifying a description of the new step. The default value is an empty string. 
        timePeriod
            A Float specifying the time of single loading cycle. The default value is 1.0. 
        timeIncrementationMethod
            A SymbolicConstant specifying the time incrementation method to be used. Possible values 
            are FIXED and AUTOMATIC. The default value is AUTOMATIC. 
        maxNumInc
            An Int specifying the maximum number of increments in a step. The default value is 100. 
        initialInc
            A Float specifying the initial time increment. The default value is the total time 
            period for the step. 
        minInc
            A Float specifying the minimum time increment allowed. The default value is the smaller 
            of the suggested initial time increment or 10−5 times the total time period. 
        maxInc
            A Float specifying the maximum time increment allowed. The default value is the total 
            time period for the step. 
        maxNumIterations
            An Int specifying the maximum number of iterations in a step. The default value is 200. 
        initialTerms
            An Int specifying the initial number of terms in the Fourier series. The default value 
            is 11. 
        maxTerms
            An Int specifying the maximum number of terms in the Fourier series. The default value 
            is 25. 
        termsIncrement
            An Int specifying the increment in number of terms in the Fourier series. The default 
            value is 5. 
        deltmx
            A Float specifying the maximum temperature change to be allowed in an increment. The 
            default value is 0.0. 
        cetol
            A Float specifying the maximum difference in the creep strain increment calculated from 
            the creep strain rates at the beginning and end of the increment. The default value is 
            0.0. 
        timePoints
            None or a String specifying a String specifying the name of a time point object used to 
            determine at which times the response of the structure will be evaluated. The default 
            value is NONE. 
        fatigue
            A Boolean specifying whether to include low-cycle fatigue analysis. The default value is 
            OFF. 
        continueAnalysis
            A Boolean specifying whether the displacement solution in the Fourier series obtained in 
            the previous direct cyclic step is used as the starting values for the current step. The 
            default value is OFF. 
        minCycleInc
            An Int specifying the minimum number of cycles over which the damage is extrapolated 
            forward. The default value is 100. 
        maxCycleInc
            An Int specifying the maximum number of cycles over which the damage is extrapolated 
            forward. The default value is 1000. 
        maxNumCycles
            The SymbolicConstant DEFAULT or an Int specifying the maximum number of cycles allowed 
            in a step or DEFAULT. A value of 1 plus half of the maximum number of cycles will be 
            used if DEFAULT is specified. The default value is DEFAULT. 
        damageExtrapolationTolerance
            A Float specifying the maximum extrapolated damage increment. The default value is 1.0. 
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
        extrapolation
            A SymbolicConstant specifying the type of extrapolation to use in determining the 
            incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, and 
            PARABOLIC. The default value is LINEAR. 
        convertSDI
            A SymbolicConstant specifying whether to force a new iteration if severe discontinuities 
            occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and 
            CONVERT_SDI_ON. The default value is PROPAGATED.

        Raises
        ------
        RangeError
        """
        pass
