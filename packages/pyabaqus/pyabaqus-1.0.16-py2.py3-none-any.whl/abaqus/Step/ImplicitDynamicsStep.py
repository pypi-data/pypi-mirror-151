import typing

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


class ImplicitDynamicsStep(AnalysisStep):
    """The ImplicitDynamicsStep object is used to provide direct integration of a dynamic
    stress/displacement response in Abaqus/Standard analyses and is generally used for 
    nonlinear cases. 
    The ImplicitDynamicsStep object is derived from the AnalysisStep object. 

    Attributes
    ----------
    name: str
        A String specifying the repository key.
    timePeriod: float
        A Float specifying the total time period of the step. The default value is 1.0.
    nlgeom: Boolean
        A Boolean specifying whether geometric nonlinearities should be accounted for during the
        step. The default value is based on the previous step.
    matrixStorage: SymbolicConstant
        A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC,
        UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT.
    application: SymbolicConstant
        A SymbolicConstant specifying the application type of the step. Possible values are
        ANALYSIS_PRODUCT_DEFAULT, TRANSIENT_FIDELITY, MODERATE_DISSIPATION, and QUASI_STATIC.
        The default value is ANALYSIS_PRODUCT_DEFAULT.
    adiabatic: Boolean
        A Boolean specifying whether an adiabatic stress analysis is to be performed. The
        default value is OFF.
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
    maxInc: typing.Union[SymbolicConstant, float]
        The SymbolicConstant DEFAULT or a Float specifying the maximum time increment allowed.
    hafTolMethod: SymbolicConstant
        A SymbolicConstant specifying the way of specifying half-increment residual tolerance
        with the automatic time incrementation scheme. Possible values are
        ANALYSIS_PRODUCT_DEFAULT, VALUE, and SCALE. The default value is VALUE.
    haftol: float
        None or a Float specifying the half-increment residual tolerance to be used with the
        automatic time incrementation scheme. The default value is None.
    halfIncScaleFactor: float
        None or a Float specifying the half-increment residual tolerance scale factor to be used
        with the automatic time incrementation scheme. The default value is None.
    nohaf: Boolean
        A Boolean specifying whether to suppress calculation of the half-increment residual. The
        default value is OFF.
    amplitude: SymbolicConstant
        A SymbolicConstant specifying the amplitude variation for loading magnitudes during the
        step. Possible values are STEP and RAMP. The default value is STEP.
    alpha: typing.Union[SymbolicConstant, float]
        The SymbolicConstant DEFAULT or a Float specifying the nondefault value of the numerical
        (artificial) damping control parameter, αα, in the implicit operator. Possible values
        are −.333 <α<<α< 0. The default value is DEFAULT.
    initialConditions: SymbolicConstant
        A SymbolicConstant specifying whether accelerations should be calculated or recalculated
        at the beginning of the step. Possible values are DEFAULT, BYPASS, and ALLOW. The
        default value is DEFAULT.
    extrapolation: SymbolicConstant
        A SymbolicConstant specifying the type of extrapolation to use in determining the
        incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR,
        PARABOLIC, VELOCITY_PARABOLIC, and ANALYSIS_PRODUCT_DEFAULT. The default value is
        ANALYSIS_PRODUCT_DEFAULT.
    noStop: Boolean
        A Boolean specifying whether to accept the solution to an increment after the maximum
        number of iterations allowed have been completed, even if the equilibrium tolerances are
        not satisfied. The default value is OFF.Warning:You should set **noStop=OFF** only in
        special cases when you have a thorough understanding of how to interpret the results.
    solutionTechnique: SymbolicConstant
        A SymbolicConstant specifying the technique used to for solving nonlinear equations.
        Possible values are FULL_NEWTON and QUASI_NEWTON. The default value is FULL_NEWTON.
    reformKernel: int
        An Int specifying the number of quasi-Newton iterations allowed before the kernel matrix
        is reformed.. The default value is 8.
    convertSDI: SymbolicConstant
        A SymbolicConstant specifying whether to force a new iteration if severe discontinuities
        occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and
        CONVERT_SDI_ON. The default value is PROPAGATED.
    previous: str
        A String specifying the name of the previous step. The new step appears after this step
        in the list of analysis steps.
    description: str
        A String specifying a description of the new step. The default value is an empty string.
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

    - DYNAMIC
            - STEP

    """

    # A String specifying the repository key. 
    name: str = ''

    # A Float specifying the total time period of the step. The default value is 1.0. 
    timePeriod: float = 1

    # A Boolean specifying whether geometric nonlinearities should be accounted for during the 
    # step. The default value is based on the previous step. 
    nlgeom: Boolean = OFF

    # A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
    # UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
    matrixStorage: SymbolicConstant = SOLVER_DEFAULT

    # A SymbolicConstant specifying the application type of the step. Possible values are 
    # ANALYSIS_PRODUCT_DEFAULT, TRANSIENT_FIDELITY, MODERATE_DISSIPATION, and QUASI_STATIC. 
    # The default value is ANALYSIS_PRODUCT_DEFAULT. 
    application: SymbolicConstant = ANALYSIS_PRODUCT_DEFAULT

    # A Boolean specifying whether an adiabatic stress analysis is to be performed. The 
    # default value is OFF. 
    adiabatic: Boolean = OFF

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

    # The SymbolicConstant DEFAULT or a Float specifying the maximum time increment allowed. 
    maxInc: typing.Union[SymbolicConstant, float] = None

    # A SymbolicConstant specifying the way of specifying half-increment residual tolerance 
    # with the automatic time incrementation scheme. Possible values are 
    # ANALYSIS_PRODUCT_DEFAULT, VALUE, and SCALE. The default value is VALUE. 
    hafTolMethod: SymbolicConstant = VALUE

    # None or a Float specifying the half-increment residual tolerance to be used with the 
    # automatic time incrementation scheme. The default value is None. 
    haftol: float = None

    # None or a Float specifying the half-increment residual tolerance scale factor to be used 
    # with the automatic time incrementation scheme. The default value is None. 
    halfIncScaleFactor: float = None

    # A Boolean specifying whether to suppress calculation of the half-increment residual. The 
    # default value is OFF. 
    nohaf: Boolean = OFF

    # A SymbolicConstant specifying the amplitude variation for loading magnitudes during the 
    # step. Possible values are STEP and RAMP. The default value is STEP. 
    amplitude: SymbolicConstant = STEP

    # The SymbolicConstant DEFAULT or a Float specifying the nondefault value of the numerical 
    # (artificial) damping control parameter, αα, in the implicit operator. Possible values 
    # are −.333 <α<<α< 0. The default value is DEFAULT. 
    alpha: typing.Union[SymbolicConstant, float] = DEFAULT

    # A SymbolicConstant specifying whether accelerations should be calculated or recalculated 
    # at the beginning of the step. Possible values are DEFAULT, BYPASS, and ALLOW. The 
    # default value is DEFAULT. 
    initialConditions: SymbolicConstant = DEFAULT

    # A SymbolicConstant specifying the type of extrapolation to use in determining the 
    # incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, 
    # PARABOLIC, VELOCITY_PARABOLIC, and ANALYSIS_PRODUCT_DEFAULT. The default value is 
    # ANALYSIS_PRODUCT_DEFAULT. 
    extrapolation: SymbolicConstant = ANALYSIS_PRODUCT_DEFAULT

    # A Boolean specifying whether to accept the solution to an increment after the maximum 
    # number of iterations allowed have been completed, even if the equilibrium tolerances are 
    # not satisfied. The default value is OFF.Warning:You should set *noStop*=OFF only in 
    # special cases when you have a thorough understanding of how to interpret the results. 
    noStop: Boolean = OFF

    # A SymbolicConstant specifying the technique used to for solving nonlinear equations. 
    # Possible values are FULL_NEWTON and QUASI_NEWTON. The default value is FULL_NEWTON. 
    solutionTechnique: SymbolicConstant = FULL_NEWTON

    # An Int specifying the number of quasi-Newton iterations allowed before the kernel matrix 
    # is reformed.. The default value is 8. 
    reformKernel: int = 8

    # A SymbolicConstant specifying whether to force a new iteration if severe discontinuities 
    # occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and 
    # CONVERT_SDI_ON. The default value is PROPAGATED. 
    convertSDI: SymbolicConstant = PROPAGATED

    # A String specifying the name of the previous step. The new step appears after this step 
    # in the list of analysis steps. 
    previous: str = ''

    # A String specifying a description of the new step. The default value is an empty string. 
    description: str = ''

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
                 nlgeom: Boolean = OFF, matrixStorage: SymbolicConstant = SOLVER_DEFAULT,
                 application: SymbolicConstant = ANALYSIS_PRODUCT_DEFAULT, adiabatic: Boolean = OFF,
                 timeIncrementationMethod: SymbolicConstant = AUTOMATIC, maxNumInc: int = 100,
                 initialInc: float = None, minInc: float = None,
                 maxInc: typing.Union[SymbolicConstant, float] = DEFAULT,
                 hafTolMethod: SymbolicConstant = VALUE, haftol: float = None,
                 halfIncScaleFactor: float = None, nohaf: Boolean = OFF,
                 amplitude: SymbolicConstant = STEP,
                 alpha: typing.Union[SymbolicConstant, float] = DEFAULT,
                 initialConditions: SymbolicConstant = DEFAULT,
                 extrapolation: SymbolicConstant = ANALYSIS_PRODUCT_DEFAULT, noStop: Boolean = OFF,
                 maintainAttributes: Boolean = False, solutionTechnique: SymbolicConstant = FULL_NEWTON,
                 reformKernel: int = 8, convertSDI: SymbolicConstant = PROPAGATED):
        """This method creates an ImplicitDynamicsStep object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].ImplicitDynamicsStep
        
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
            A Float specifying the total time period of the step. The default value is 1.0. 
        nlgeom
            A Boolean specifying whether geometric nonlinearities should be accounted for during the 
            step. The default value is based on the previous step. 
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
        application
            A SymbolicConstant specifying the application type of the step. Possible values are 
            ANALYSIS_PRODUCT_DEFAULT, TRANSIENT_FIDELITY, MODERATE_DISSIPATION, and QUASI_STATIC. 
            The default value is ANALYSIS_PRODUCT_DEFAULT. 
        adiabatic
            A Boolean specifying whether an adiabatic stress analysis is to be performed. The 
            default value is OFF. 
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
            The SymbolicConstant DEFAULT or a Float specifying the maximum time increment allowed. 
        hafTolMethod
            A SymbolicConstant specifying the way of specifying half-increment residual tolerance 
            with the automatic time incrementation scheme. Possible values are 
            ANALYSIS_PRODUCT_DEFAULT, VALUE, and SCALE. The default value is VALUE. 
        haftol
            None or a Float specifying the half-increment residual tolerance to be used with the 
            automatic time incrementation scheme. The default value is None. 
        halfIncScaleFactor
            None or a Float specifying the half-increment residual tolerance scale factor to be used 
            with the automatic time incrementation scheme. The default value is None. 
        nohaf
            A Boolean specifying whether to suppress calculation of the half-increment residual. The 
            default value is OFF. 
        amplitude
            A SymbolicConstant specifying the amplitude variation for loading magnitudes during the 
            step. Possible values are STEP and RAMP. The default value is STEP. 
        alpha
            The SymbolicConstant DEFAULT or a Float specifying the nondefault value of the numerical 
            (artificial) damping control parameter, αα, in the implicit operator. Possible values 
            are −.333 <α<<α< 0. The default value is DEFAULT. 
        initialConditions
            A SymbolicConstant specifying whether accelerations should be calculated or recalculated 
            at the beginning of the step. Possible values are DEFAULT, BYPASS, and ALLOW. The 
            default value is DEFAULT. 
        extrapolation
            A SymbolicConstant specifying the type of extrapolation to use in determining the 
            incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, 
            PARABOLIC, VELOCITY_PARABOLIC, and ANALYSIS_PRODUCT_DEFAULT. The default value is 
            ANALYSIS_PRODUCT_DEFAULT. 
        noStop
            A Boolean specifying whether to accept the solution to an increment after the maximum 
            number of iterations allowed have been completed, even if the equilibrium tolerances are 
            not satisfied. The default value is OFF.Warning:You should set *noStop*=OFF only in 
            special cases when you have a thorough understanding of how to interpret the results. 
        maintainAttributes
            A Boolean specifying whether to retain attributes from an existing step with the same 
            name. The default value is False. 
        solutionTechnique
            A SymbolicConstant specifying the technique used to for solving nonlinear equations. 
            Possible values are FULL_NEWTON and QUASI_NEWTON. The default value is FULL_NEWTON. 
        reformKernel
            An Int specifying the number of quasi-Newton iterations allowed before the kernel matrix 
            is reformed.. The default value is 8. 
        convertSDI
            A SymbolicConstant specifying whether to force a new iteration if severe discontinuities 
            occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and 
            CONVERT_SDI_ON. The default value is PROPAGATED. 

        Returns
        -------
            An ImplicitDynamicsStep object. 

        Raises
        ------
        RangeError
        """
        super().__init__()
        pass

    def setValues(self, description: str = '', timePeriod: float = 1, nlgeom: Boolean = OFF,
                  matrixStorage: SymbolicConstant = SOLVER_DEFAULT,
                  application: SymbolicConstant = ANALYSIS_PRODUCT_DEFAULT, adiabatic: Boolean = OFF,
                  timeIncrementationMethod: SymbolicConstant = AUTOMATIC, maxNumInc: int = 100,
                  initialInc: float = None, minInc: float = None,
                  maxInc: typing.Union[SymbolicConstant, float] = DEFAULT,
                  hafTolMethod: SymbolicConstant = VALUE, haftol: float = None,
                  halfIncScaleFactor: float = None, nohaf: Boolean = OFF,
                  amplitude: SymbolicConstant = STEP,
                  alpha: typing.Union[SymbolicConstant, float] = DEFAULT,
                  initialConditions: SymbolicConstant = DEFAULT,
                  extrapolation: SymbolicConstant = ANALYSIS_PRODUCT_DEFAULT, noStop: Boolean = OFF,
                  solutionTechnique: SymbolicConstant = FULL_NEWTON, reformKernel: int = 8,
                  convertSDI: SymbolicConstant = PROPAGATED):
        """This method modifies the ImplicitDynamicsStep object.
        
        Parameters
        ----------
        description
            A String specifying a description of the new step. The default value is an empty string. 
        timePeriod
            A Float specifying the total time period of the step. The default value is 1.0. 
        nlgeom
            A Boolean specifying whether geometric nonlinearities should be accounted for during the 
            step. The default value is based on the previous step. 
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
        application
            A SymbolicConstant specifying the application type of the step. Possible values are 
            ANALYSIS_PRODUCT_DEFAULT, TRANSIENT_FIDELITY, MODERATE_DISSIPATION, and QUASI_STATIC. 
            The default value is ANALYSIS_PRODUCT_DEFAULT. 
        adiabatic
            A Boolean specifying whether an adiabatic stress analysis is to be performed. The 
            default value is OFF. 
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
            The SymbolicConstant DEFAULT or a Float specifying the maximum time increment allowed. 
        hafTolMethod
            A SymbolicConstant specifying the way of specifying half-increment residual tolerance 
            with the automatic time incrementation scheme. Possible values are 
            ANALYSIS_PRODUCT_DEFAULT, VALUE, and SCALE. The default value is VALUE. 
        haftol
            None or a Float specifying the half-increment residual tolerance to be used with the 
            automatic time incrementation scheme. The default value is None. 
        halfIncScaleFactor
            None or a Float specifying the half-increment residual tolerance scale factor to be used 
            with the automatic time incrementation scheme. The default value is None. 
        nohaf
            A Boolean specifying whether to suppress calculation of the half-increment residual. The 
            default value is OFF. 
        amplitude
            A SymbolicConstant specifying the amplitude variation for loading magnitudes during the 
            step. Possible values are STEP and RAMP. The default value is STEP. 
        alpha
            The SymbolicConstant DEFAULT or a Float specifying the nondefault value of the numerical 
            (artificial) damping control parameter, αα, in the implicit operator. Possible values 
            are −.333 <α<<α< 0. The default value is DEFAULT. 
        initialConditions
            A SymbolicConstant specifying whether accelerations should be calculated or recalculated 
            at the beginning of the step. Possible values are DEFAULT, BYPASS, and ALLOW. The 
            default value is DEFAULT. 
        extrapolation
            A SymbolicConstant specifying the type of extrapolation to use in determining the 
            incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, 
            PARABOLIC, VELOCITY_PARABOLIC, and ANALYSIS_PRODUCT_DEFAULT. The default value is 
            ANALYSIS_PRODUCT_DEFAULT. 
        noStop
            A Boolean specifying whether to accept the solution to an increment after the maximum 
            number of iterations allowed have been completed, even if the equilibrium tolerances are 
            not satisfied. The default value is OFF.Warning:You should set *noStop*=OFF only in 
            special cases when you have a thorough understanding of how to interpret the results. 
        solutionTechnique
            A SymbolicConstant specifying the technique used to for solving nonlinear equations. 
            Possible values are FULL_NEWTON and QUASI_NEWTON. The default value is FULL_NEWTON. 
        reformKernel
            An Int specifying the number of quasi-Newton iterations allowed before the kernel matrix 
            is reformed.. The default value is 8. 
        convertSDI
            A SymbolicConstant specifying whether to force a new iteration if severe discontinuities 
            occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and 
            CONVERT_SDI_ON. The default value is PROPAGATED.

        Raises
        ------
        RangeError
        """
        pass
