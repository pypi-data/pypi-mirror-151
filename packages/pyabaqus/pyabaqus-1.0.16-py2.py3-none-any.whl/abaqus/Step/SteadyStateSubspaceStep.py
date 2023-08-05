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
from ..StepMiscellaneous.SteadyStateSubspaceFrequencyArray import SteadyStateSubspaceFrequencyArray
from ..StepOutput.DiagnosticPrint import DiagnosticPrint
from ..StepOutput.FieldOutputRequestState import FieldOutputRequestState
from ..StepOutput.HistoryOutputRequestState import HistoryOutputRequestState
from ..StepOutput.Monitor import Monitor
from ..StepOutput.Restart import Restart


class SteadyStateSubspaceStep(AnalysisStep):
    """The SteadyStateSubspaceStep object is used to calculate the linearized steady-state
    response of the system to harmonic excitation on the basis of the subspace projection 
    method. 
    The SteadyStateSubspaceStep object is derived from the AnalysisStep object. 

    Attributes
    ----------
    name: str
        A String specifying the repository key.
    factorization: SymbolicConstant
        A SymbolicConstant specifying whether damping terms are to be ignored so that a real,
        rather than a complex, system matrix is factored. Possible values are REAL_ONLY and
        COMPLEX. The default value is COMPLEX.
    scale: SymbolicConstant
        A SymbolicConstant specifying whether a logarithmic or linear scale is used for output.
        Possible values are LOGARITHMIC and LINEAR. The default value is LOGARITHMIC.
    matrixStorage: SymbolicConstant
        A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC,
        UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT.
    subdivideUsingEigenfrequencies: Boolean
        A Boolean specifying whether to subdivide each frequency range using the
        eigenfrequencies of the system. The default value is ON.
    projection: SymbolicConstant
        A SymbolicConstant specifying how often to perform subspace projections onto the modal
        subspace. Possible values are ALL_FREQUENCIES, CONSTANT, EIGENFREQUENCY,
        PROPERTY_CHANGE, and RANGE. The default value is ALL_FREQUENCIES.
    maxDampingChange: float
        A Float specifying the maximum relative change in damping material properties before a
        new projection is to be performed. The default value is 0.1.
    maxStiffnessChange: float
        A Float specifying the maximum relative change in stiffness material properties before a
        new projection is to be performed. The default value is 0.1.
    frictionDamping: Boolean
        A Boolean specifying whether to add to the damping matrix contributions due to friction
        effects. The default value is OFF.
    previous: str
        A String specifying the name of the previous step. The new step appears after this step
        in the list of analysis steps.
    description: str
        A String specifying a description of the new step. The default value is an empty string.
    frequencyRange: SteadyStateSubspaceFrequencyArray
        A :py:class:`~abaqus.StepMiscellaneous.SteadyStateSubspaceFrequencyArray.SteadyStateSubspaceFrequencyArray` object.
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

    - STEADY STATE DYNAMICS
            - STEP

    """

    # A String specifying the repository key. 
    name: str = ''

    # A SymbolicConstant specifying whether damping terms are to be ignored so that a real, 
    # rather than a complex, system matrix is factored. Possible values are REAL_ONLY and 
    # COMPLEX. The default value is COMPLEX. 
    factorization: SymbolicConstant = COMPLEX

    # A SymbolicConstant specifying whether a logarithmic or linear scale is used for output. 
    # Possible values are LOGARITHMIC and LINEAR. The default value is LOGARITHMIC. 
    scale: SymbolicConstant = LOGARITHMIC

    # A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
    # UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
    matrixStorage: SymbolicConstant = SOLVER_DEFAULT

    # A Boolean specifying whether to subdivide each frequency range using the 
    # eigenfrequencies of the system. The default value is ON. 
    subdivideUsingEigenfrequencies: Boolean = ON

    # A SymbolicConstant specifying how often to perform subspace projections onto the modal 
    # subspace. Possible values are ALL_FREQUENCIES, CONSTANT, EIGENFREQUENCY, 
    # PROPERTY_CHANGE, and RANGE. The default value is ALL_FREQUENCIES. 
    projection: SymbolicConstant = ALL_FREQUENCIES

    # A Float specifying the maximum relative change in damping material properties before a 
    # new projection is to be performed. The default value is 0.1. 
    maxDampingChange: float = 0

    # A Float specifying the maximum relative change in stiffness material properties before a 
    # new projection is to be performed. The default value is 0.1. 
    maxStiffnessChange: float = 0

    # A Boolean specifying whether to add to the damping matrix contributions due to friction 
    # effects. The default value is OFF. 
    frictionDamping: Boolean = OFF

    # A String specifying the name of the previous step. The new step appears after this step 
    # in the list of analysis steps. 
    previous: str = ''

    # A String specifying a description of the new step. The default value is an empty string. 
    description: str = ''

    # A SteadyStateSubspaceFrequencyArray object. 
    frequencyRange: SteadyStateSubspaceFrequencyArray = SteadyStateSubspaceFrequencyArray()

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

    def __init__(self, name: str, previous: str, frequencyRange: SteadyStateSubspaceFrequencyArray,
                 description: str = '', factorization: SymbolicConstant = COMPLEX,
                 scale: SymbolicConstant = LOGARITHMIC, matrixStorage: SymbolicConstant = SOLVER_DEFAULT,
                 maintainAttributes: Boolean = False, subdivideUsingEigenfrequencies: Boolean = ON,
                 projection: SymbolicConstant = ALL_FREQUENCIES, maxDampingChange: float = 0,
                 maxStiffnessChange: float = 0, frictionDamping: Boolean = OFF):
        """This method creates a SteadyStateSubspaceStep object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].SteadyStateSubspaceStep
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        previous
            A String specifying the name of the previous step. The new step appears after this step 
            in the list of analysis steps. 
        frequencyRange
            A SteadyStateSubspaceFrequencyArray object. 
        description
            A String specifying a description of the new step. The default value is an empty string. 
        factorization
            A SymbolicConstant specifying whether damping terms are to be ignored so that a real, 
            rather than a complex, system matrix is factored. Possible values are REAL_ONLY and 
            COMPLEX. The default value is COMPLEX. 
        scale
            A SymbolicConstant specifying whether a logarithmic or linear scale is used for output. 
            Possible values are LOGARITHMIC and LINEAR. The default value is LOGARITHMIC. 
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
        maintainAttributes
            A Boolean specifying whether to retain attributes from an existing step with the same 
            name. The default value is False. 
        subdivideUsingEigenfrequencies
            A Boolean specifying whether to subdivide each frequency range using the 
            eigenfrequencies of the system. The default value is ON. 
        projection
            A SymbolicConstant specifying how often to perform subspace projections onto the modal 
            subspace. Possible values are ALL_FREQUENCIES, CONSTANT, EIGENFREQUENCY, 
            PROPERTY_CHANGE, and RANGE. The default value is ALL_FREQUENCIES. 
        maxDampingChange
            A Float specifying the maximum relative change in damping material properties before a 
            new projection is to be performed. The default value is 0.1. 
        maxStiffnessChange
            A Float specifying the maximum relative change in stiffness material properties before a 
            new projection is to be performed. The default value is 0.1. 
        frictionDamping
            A Boolean specifying whether to add to the damping matrix contributions due to friction 
            effects. The default value is OFF. 

        Returns
        -------
            A SteadyStateSubspaceStep object. 

        Raises
        ------
        RangeError
        """
        super().__init__()
        pass

    def setValues(self, description: str = '', factorization: SymbolicConstant = COMPLEX,
                  scale: SymbolicConstant = LOGARITHMIC, matrixStorage: SymbolicConstant = SOLVER_DEFAULT,
                  subdivideUsingEigenfrequencies: Boolean = ON,
                  projection: SymbolicConstant = ALL_FREQUENCIES, maxDampingChange: float = 0,
                  maxStiffnessChange: float = 0, frictionDamping: Boolean = OFF):
        """This method modifies the SteadyStateSubspaceStep object.
        
        Parameters
        ----------
        description
            A String specifying a description of the new step. The default value is an empty string. 
        factorization
            A SymbolicConstant specifying whether damping terms are to be ignored so that a real, 
            rather than a complex, system matrix is factored. Possible values are REAL_ONLY and 
            COMPLEX. The default value is COMPLEX. 
        scale
            A SymbolicConstant specifying whether a logarithmic or linear scale is used for output. 
            Possible values are LOGARITHMIC and LINEAR. The default value is LOGARITHMIC. 
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
        subdivideUsingEigenfrequencies
            A Boolean specifying whether to subdivide each frequency range using the 
            eigenfrequencies of the system. The default value is ON. 
        projection
            A SymbolicConstant specifying how often to perform subspace projections onto the modal 
            subspace. Possible values are ALL_FREQUENCIES, CONSTANT, EIGENFREQUENCY, 
            PROPERTY_CHANGE, and RANGE. The default value is ALL_FREQUENCIES. 
        maxDampingChange
            A Float specifying the maximum relative change in damping material properties before a 
            new projection is to be performed. The default value is 0.1. 
        maxStiffnessChange
            A Float specifying the maximum relative change in stiffness material properties before a 
            new projection is to be performed. The default value is 0.1. 
        frictionDamping
            A Boolean specifying whether to add to the damping matrix contributions due to friction 
            effects. The default value is OFF.

        Raises
        ------
        RangeError
        """
        pass
