from abaqusConstants import *
from .AnalysisStep import AnalysisStep
from ..Adaptivity.AdaptiveMeshConstraintState import AdaptiveMeshConstraintState
from ..Adaptivity.AdaptiveMeshDomain import AdaptiveMeshDomain
from ..BoundaryCondition.BoundaryConditionState import BoundaryConditionState
from ..Load.LoadCase import LoadCase
from ..Load.LoadState import LoadState
from ..PredefinedField.PredefinedFieldState import PredefinedFieldState
from ..Region.Region import Region
from ..StepMiscellaneous.Control import Control
from ..StepMiscellaneous.SolverControl import SolverControl
from ..StepOutput.DiagnosticPrint import DiagnosticPrint
from ..StepOutput.FieldOutputRequestState import FieldOutputRequestState
from ..StepOutput.HistoryOutputRequestState import HistoryOutputRequestState
from ..StepOutput.Monitor import Monitor
from ..StepOutput.Restart import Restart


class StaticRiksStep(AnalysisStep):
    """The StaticRiksStep object is used to indicate that the step should be analyzed as a
    static load step using the modified Riks method for proportional loading cases. 
    The StaticRiksStep object is derived from the AnalysisStep object. 

    Attributes
    ----------
    name: str
        A String specifying the repository key.
    nlgeom: Boolean
        A Boolean specifying whether to allow for geometric nonlinearity. The default value is
        OFF.
    adiabatic: Boolean
        A Boolean specifying whether to perform an adiabatic stress analysis. The default value
        is OFF.
    maxLPF: float
        None or a Float specifying the maximum value of the load proportionality factor. The
        default value is None.
    nodeOn: Boolean
        A Boolean specifying whether to monitor the finishing displacement value at a node. The
        default value is OFF.
    maximumDisplacement: float
        A Float specifying the value of the total displacement (or rotation) at the node and
        degree of freedom that, if crossed during an increment, ends the step at the current
        increment. This argument is required when **nodeOn=ON**. The default value is 0.0.
    dof: int
        An Int specifying the degree of freedom being monitored. This argument is required when
        **nodeOn=ON**. The default value is 0.
    timeIncrementationMethod: SymbolicConstant
        A SymbolicConstant specifying the time incrementation method to be used. Possible values
        are FIXED and AUTOMATIC. The default value is AUTOMATIC.
    maxNumInc: int
        An Int specifying the maximum number of increments in a step. The default value is 100.
    totalArcLength: float
        A Float specifying the total load proportionality factor associated with the load in
        this step. The default value is 1.0.
    initialArcInc: float
        A Float specifying the initial load proportionality factor. The default value is the
        total load proportionality factor for the step.
    minArcInc: float
        A Float specifying the minimum arc length increment allowed. The default value is the
        smaller of the suggested initial load proportionality factor or 10−5 times the total
        load proportionality factor for the step.
    maxArcInc: float
        A Float specifying the maximum arc length increment allowed. The default value is the
        total load proportionality factor for the step.
    matrixStorage: SymbolicConstant
        A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC,
        UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT.
    extrapolation: SymbolicConstant
        A SymbolicConstant specifying the type of extrapolation to use in determining the
        incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, and
        PARABOLIC. The default value is LINEAR.
    noStop: Boolean
        A Boolean specifying whether to accept the solution to an increment after the maximum
        number of iterations allowed have been completed, even if the equilibrium tolerances are
        not satisfied. The default value is OFF.Warning:You should set **noStop=ON** only in
        special cases when you have a thorough understanding of how to interpret the results.
    useLongTermSolution: Boolean
        A Boolean specifying wether to obtain the fully relaxed long-term elastic solution with
        time-domain viscoelasticity or the long-term elastic-Plastic solution for two-layer
        viscoplasticity. The default value is OFF.
    convertSDI: SymbolicConstant
        A SymbolicConstant specifying whether to force a new iteration if severe discontinuities
        occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and
        CONVERT_SDI_ON. The default value is PROPAGATED.
    previous: str
        A String specifying the name of the previous step. The new step appears after this step
        in the list of analysis steps.
    description: str
        A String specifying a description of the new step. The default value is an empty string.
    fullyPlastic: str
        A String specifying the name of the region being monitored for fully Plastic behavior.
        The default value is an empty string.
    region: Region
        A :py:class:`~abaqus.Region.Region.Region` object specifying the vertex at which the finishing displacement value is being
        monitored. This argument is required when **nodeOn=ON**.
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

    - STATIC
            - STEP

    """

    # A String specifying the repository key. 
    name: str = ''

    # A Boolean specifying whether to allow for geometric nonlinearity. The default value is 
    # OFF. 
    nlgeom: Boolean = OFF

    # A Boolean specifying whether to perform an adiabatic stress analysis. The default value 
    # is OFF. 
    adiabatic: Boolean = OFF

    # None or a Float specifying the maximum value of the load proportionality factor. The 
    # default value is None. 
    maxLPF: float = None

    # A Boolean specifying whether to monitor the finishing displacement value at a node. The 
    # default value is OFF. 
    nodeOn: Boolean = OFF

    # A Float specifying the value of the total displacement (or rotation) at the node and 
    # degree of freedom that, if crossed during an increment, ends the step at the current 
    # increment. This argument is required when *nodeOn*=ON. The default value is 0.0. 
    maximumDisplacement: float = 0

    # An Int specifying the degree of freedom being monitored. This argument is required when 
    # *nodeOn*=ON. The default value is 0. 
    dof: int = 0

    # A SymbolicConstant specifying the time incrementation method to be used. Possible values 
    # are FIXED and AUTOMATIC. The default value is AUTOMATIC. 
    timeIncrementationMethod: SymbolicConstant = AUTOMATIC

    # An Int specifying the maximum number of increments in a step. The default value is 100. 
    maxNumInc: int = 100

    # A Float specifying the total load proportionality factor associated with the load in 
    # this step. The default value is 1.0. 
    totalArcLength: float = 1

    # A Float specifying the initial load proportionality factor. The default value is the 
    # total load proportionality factor for the step. 
    initialArcInc: float = None

    # A Float specifying the minimum arc length increment allowed. The default value is the 
    # smaller of the suggested initial load proportionality factor or 10−5 times the total 
    # load proportionality factor for the step. 
    minArcInc: float = None

    # A Float specifying the maximum arc length increment allowed. The default value is the 
    # total load proportionality factor for the step. 
    maxArcInc: float = None

    # A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
    # UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
    matrixStorage: SymbolicConstant = SOLVER_DEFAULT

    # A SymbolicConstant specifying the type of extrapolation to use in determining the 
    # incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, and 
    # PARABOLIC. The default value is LINEAR. 
    extrapolation: SymbolicConstant = LINEAR

    # A Boolean specifying whether to accept the solution to an increment after the maximum 
    # number of iterations allowed have been completed, even if the equilibrium tolerances are 
    # not satisfied. The default value is OFF.Warning:You should set *noStop*=ON only in 
    # special cases when you have a thorough understanding of how to interpret the results. 
    noStop: Boolean = OFF

    # A Boolean specifying wether to obtain the fully relaxed long-term elastic solution with 
    # time-domain viscoelasticity or the long-term elastic-Plastic solution for two-layer
    # viscoplasticity. The default value is OFF. 
    useLongTermSolution: Boolean = OFF

    # A SymbolicConstant specifying whether to force a new iteration if severe discontinuities 
    # occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and 
    # CONVERT_SDI_ON. The default value is PROPAGATED. 
    convertSDI: SymbolicConstant = PROPAGATED

    # A String specifying the name of the previous step. The new step appears after this step 
    # in the list of analysis steps. 
    previous: str = ''

    # A String specifying a description of the new step. The default value is an empty string. 
    description: str = ''

    # A String specifying the name of the region being monitored for fully Plastic behavior.
    # The default value is an empty string. 
    fullyPlastic: str = ''

    # A Region object specifying the vertex at which the finishing displacement value is being 
    # monitored. This argument is required when *nodeOn*=ON. 
    region: Region = Region()

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

    def __init__(self, name: str, previous: str, description: str = '', nlgeom: Boolean = OFF,
                 adiabatic: Boolean = OFF, maxLPF: float = None, nodeOn: Boolean = OFF,
                 maximumDisplacement: float = 0, dof: int = 0, region: Region = Region(),
                 timeIncrementationMethod: SymbolicConstant = AUTOMATIC, maxNumInc: int = 100,
                 totalArcLength: float = 1, initialArcInc: float = None, minArcInc: float = None,
                 maxArcInc: float = None, matrixStorage: SymbolicConstant = SOLVER_DEFAULT,
                 extrapolation: SymbolicConstant = LINEAR, fullyPlastic: str = '', noStop: Boolean = OFF,
                 maintainAttributes: Boolean = False, useLongTermSolution: Boolean = OFF,
                 convertSDI: SymbolicConstant = PROPAGATED):
        """This method creates a StaticRiksStep object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].StaticRiksStep
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        previous
            A String specifying the name of the previous step. The new step appears after this step 
            in the list of analysis steps. 
        description
            A String specifying a description of the new step. The default value is an empty string. 
        nlgeom
            A Boolean specifying whether to allow for geometric nonlinearity. The default value is 
            OFF. 
        adiabatic
            A Boolean specifying whether to perform an adiabatic stress analysis. The default value 
            is OFF. 
        maxLPF
            None or a Float specifying the maximum value of the load proportionality factor. The 
            default value is None. 
        nodeOn
            A Boolean specifying whether to monitor the finishing displacement value at a node. The 
            default value is OFF. 
        maximumDisplacement
            A Float specifying the value of the total displacement (or rotation) at the node and 
            degree of freedom that, if crossed during an increment, ends the step at the current 
            increment. This argument is required when *nodeOn*=ON. The default value is 0.0. 
        dof
            An Int specifying the degree of freedom being monitored. This argument is required when 
            *nodeOn*=ON. The default value is 0. 
        region
            A Region object specifying the vertex at which the finishing displacement value is being 
            monitored. This argument is required when *nodeOn*=ON. 
        timeIncrementationMethod
            A SymbolicConstant specifying the time incrementation method to be used. Possible values 
            are FIXED and AUTOMATIC. The default value is AUTOMATIC. 
        maxNumInc
            An Int specifying the maximum number of increments in a step. The default value is 100. 
        totalArcLength
            A Float specifying the total load proportionality factor associated with the load in 
            this step. The default value is 1.0. 
        initialArcInc
            A Float specifying the initial load proportionality factor. The default value is the 
            total load proportionality factor for the step. 
        minArcInc
            A Float specifying the minimum arc length increment allowed. The default value is the 
            smaller of the suggested initial load proportionality factor or 10−5 times the total 
            load proportionality factor for the step. 
        maxArcInc
            A Float specifying the maximum arc length increment allowed. The default value is the 
            total load proportionality factor for the step. 
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
        extrapolation
            A SymbolicConstant specifying the type of extrapolation to use in determining the 
            incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, and 
            PARABOLIC. The default value is LINEAR. 
        fullyPlastic
            A String specifying the name of the region being monitored for fully Plastic behavior.
            The default value is an empty string. 
        noStop
            A Boolean specifying whether to accept the solution to an increment after the maximum 
            number of iterations allowed have been completed, even if the equilibrium tolerances are 
            not satisfied. The default value is OFF.Warning:You should set *noStop*=ON only in 
            special cases when you have a thorough understanding of how to interpret the results. 
        maintainAttributes
            A Boolean specifying whether to retain attributes from an existing step with the same 
            name. The default value is False. 
        useLongTermSolution
            A Boolean specifying wether to obtain the fully relaxed long-term elastic solution with 
            time-domain viscoelasticity or the long-term elastic-Plastic solution for two-layer
            viscoplasticity. The default value is OFF. 
        convertSDI
            A SymbolicConstant specifying whether to force a new iteration if severe discontinuities 
            occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and 
            CONVERT_SDI_ON. The default value is PROPAGATED. 

        Returns
        -------
            A StaticRiksStep object. 

        Raises
        ------
        RangeError
        """
        super().__init__()
        pass

    def setValues(self, description: str = '', nlgeom: Boolean = OFF, adiabatic: Boolean = OFF,
                  maxLPF: float = None, nodeOn: Boolean = OFF, maximumDisplacement: float = 0,
                  dof: int = 0, region: Region = Region(),
                  timeIncrementationMethod: SymbolicConstant = AUTOMATIC, maxNumInc: int = 100,
                  totalArcLength: float = 1, initialArcInc: float = None, minArcInc: float = None,
                  maxArcInc: float = None, matrixStorage: SymbolicConstant = SOLVER_DEFAULT,
                  extrapolation: SymbolicConstant = LINEAR, fullyPlastic: str = '', noStop: Boolean = OFF,
                  useLongTermSolution: Boolean = OFF, convertSDI: SymbolicConstant = PROPAGATED):
        """This method modifies the StaticRiksStep object.
        
        Parameters
        ----------
        description
            A String specifying a description of the new step. The default value is an empty string. 
        nlgeom
            A Boolean specifying whether to allow for geometric nonlinearity. The default value is 
            OFF. 
        adiabatic
            A Boolean specifying whether to perform an adiabatic stress analysis. The default value 
            is OFF. 
        maxLPF
            None or a Float specifying the maximum value of the load proportionality factor. The 
            default value is None. 
        nodeOn
            A Boolean specifying whether to monitor the finishing displacement value at a node. The 
            default value is OFF. 
        maximumDisplacement
            A Float specifying the value of the total displacement (or rotation) at the node and 
            degree of freedom that, if crossed during an increment, ends the step at the current 
            increment. This argument is required when *nodeOn*=ON. The default value is 0.0. 
        dof
            An Int specifying the degree of freedom being monitored. This argument is required when 
            *nodeOn*=ON. The default value is 0. 
        region
            A Region object specifying the vertex at which the finishing displacement value is being 
            monitored. This argument is required when *nodeOn*=ON. 
        timeIncrementationMethod
            A SymbolicConstant specifying the time incrementation method to be used. Possible values 
            are FIXED and AUTOMATIC. The default value is AUTOMATIC. 
        maxNumInc
            An Int specifying the maximum number of increments in a step. The default value is 100. 
        totalArcLength
            A Float specifying the total load proportionality factor associated with the load in 
            this step. The default value is 1.0. 
        initialArcInc
            A Float specifying the initial load proportionality factor. The default value is the 
            total load proportionality factor for the step. 
        minArcInc
            A Float specifying the minimum arc length increment allowed. The default value is the 
            smaller of the suggested initial load proportionality factor or 10−5 times the total 
            load proportionality factor for the step. 
        maxArcInc
            A Float specifying the maximum arc length increment allowed. The default value is the 
            total load proportionality factor for the step. 
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
        extrapolation
            A SymbolicConstant specifying the type of extrapolation to use in determining the 
            incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, and 
            PARABOLIC. The default value is LINEAR. 
        fullyPlastic
            A String specifying the name of the region being monitored for fully Plastic behavior.
            The default value is an empty string. 
        noStop
            A Boolean specifying whether to accept the solution to an increment after the maximum 
            number of iterations allowed have been completed, even if the equilibrium tolerances are 
            not satisfied. The default value is OFF.Warning:You should set *noStop*=ON only in 
            special cases when you have a thorough understanding of how to interpret the results. 
        useLongTermSolution
            A Boolean specifying wether to obtain the fully relaxed long-term elastic solution with 
            time-domain viscoelasticity or the long-term elastic-Plastic solution for two-layer
            viscoplasticity. The default value is OFF. 
        convertSDI
            A SymbolicConstant specifying whether to force a new iteration if severe discontinuities 
            occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and 
            CONVERT_SDI_ON. The default value is PROPAGATED.

        Raises
        ------
        RangeError
        """
        pass
