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


class FrequencyStep(AnalysisStep):
    """The FrequencyStep object is used to perform eigenvalue extraction to calculate the
    natural frequencies and corresponding mode shapes of a system. 
    The FrequencyStep object is derived from the AnalysisStep object. 

    Attributes
    ----------
    name: str
        A String specifying the repository key.
    eigensolver: SymbolicConstant
        A SymbolicConstant specifying the eigensolver. Possible values are LANCZOS, SUBSPACE,
        and AMS.The following optional arguments are ignored unless **eigensolver=LANCZOS**:
        **blockSize**, **maxBlocks**, **normalization**, **propertyEvaluationFrequency**.The following
        optional arguments are ignored unless **eigensolver=LANCZOS** or AMS: **minEigen**,
        **maxEigen**, and **acousticCoupling**.The following optional arguments are ignored unless
        **eigensolver=AMS**: **projectDamping**, **acousticRangeFactor**,
        **substructureCutoffMultiplier**, **firstCutoffMultiplier**, **secondCutoffMultiplier**,
        **residualModeRegion**, **regionalModeDof**, and **limitSavedEigenvectorRegion**.
    numEigen: SymbolicConstant
        The SymbolicConstant ALL or an Int specifying the number of eigenvalues to be calculated
        or ALL. The default value is ALL.
    shift: float
        A Float specifying the shift point in cycles per time. The default value is 0.0.
    minEigen: float
        None or a Float specifying the minimum frequency of interest in cycles per time. The
        default value is None.
    maxEigen: float
        None or a Float specifying the maximum frequency of interest in cycles per time. The
        default value is None.
    vectors: int
        None or an Int specifying the number of vectors used in the iteration. The default is
        the minimum of (2**n**, **n** + 8), where **n** is the number of eigenvalues requested. The
        default value is None.
    maxIterations: int
        An Int specifying the maximum number of iterations. The default value is 30.
    blockSize: SymbolicConstant
        A SymbolicConstant specifying the size of the Lanczos block steps. The default value is
        DEFAULT.
    maxBlocks: SymbolicConstant
        A SymbolicConstant specifying the maximum number of Lanczos block steps within each
        Lanczos run. The default value is DEFAULT.
    normalization: SymbolicConstant
        A SymbolicConstant specifying the method for normalizing eigenvectors. Possible values
        are DISPLACEMENT and MASS. The default value is DISPLACEMENT.A value of DISPLACEMENT
        indicates normalizing the eigenvectors so that the largest displacement entry in each
        vector is unity. A value of MASS indicates normalizing the eigenvectors with respect to
        the structure's mass matrix, which results in scaling the eigenvectors so that the
        generalized mass for each vector is unity.
    propertyEvaluationFrequency: float
        None or a Float specifying the frequency at which to evaluate frequency-dependent
        properties for viscoelasticity, springs, and dashpots during the eigenvalue extraction.
        If the value is None, the analysis product will evaluate the stiffness associated with
        frequency-dependent springs and dashpots at zero frequency and will not consider the
        stiffness contributions from frequency-domain viscoelasticity in the step. The default
        value is None.
    projectDamping: Boolean
        A Boolean specifying whether to include projection of viscous and structural damping
        operators during **AMS** eigenvalue extraction. Valid only when **eigenSolver=AMS**. The
        default value is ON.
    acousticCoupling: SymbolicConstant
        A SymbolicConstant specifying the type of acoustic-structural coupling in models with
        acoustic and structural elements coupled using the TIE option or in models with ASI-type
        elements. Possible values are AC_ON, AC_OFF, and AC_PROJECTION. The default value is
        AC_ON.
    acousticRangeFactor: float
        A Float specifying the ratio of the maximum acoustic frequency to the maximum structural
        frequency. The default value is 1.0.
    frictionDamping: Boolean
        A Boolean specifying whether to add to the damping matrix contributions due to friction
        effects. The default value is OFF.
    matrixStorage: SymbolicConstant
        A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC,
        UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT.
    simLinearDynamics: Boolean
        A Boolean specifying whether to activate the SIM-based linear dynamics procedures. The
        default value is OFF.
    residualModes: Boolean
        A Boolean specifying whether to include residual modes from an immediately preceding
        Static, Linear Perturbation step. The default value is OFF.
    substructureCutoffMultiplier: float
        A Float specifying the cutoff frequency for substructure eigenproblems, defined as a
        multiplier of the maximum frequency of interest. The default value is 5.0.
    firstCutoffMultiplier: float
        A Float specifying the first cutoff frequency for a reduced eigenproblem, defined as a
        multiplier of the maximum frequency of interest. The default value is 1.7.
    secondCutoffMultiplier: float
        A Float specifying the second cutoff frequency for a reduced eigenproblem defined as a
        multiplier of the maximum frequency of interest. The default value is 1.1.
    previous: str
        A String specifying the name of the previous step. The new step appears after this step
        in the list of analysis steps.
    description: str
        A String specifying a description of the new step. The default value is an empty string.
    residualModeRegion: tuple
        None or a tuple of Strings specifying the name of a region for which residual modes are
        requested. The default value is None.
    residualModeDof: int
        None or a tuple of Ints specifying the degree of freedom for which residual modes are
        requested. The default value is None.
    limitSavedEigenvectorRegion: SymbolicConstant
        None or a :py:class:`~abaqus.Region.Region.Region` object specifying a region for which eigenvectors should be saved or
        the SymbolicConstant None representing the whole model. The default value is None.
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

    - FREQUENCY
            - STEP

    """

    # A String specifying the repository key. 
    name: str = ''

    # A SymbolicConstant specifying the eigensolver. Possible values are LANCZOS, SUBSPACE, 
    # and AMS.The following optional arguments are ignored unless *eigensolver*=LANCZOS: 
    # *blockSize*, *maxBlocks*, *normalization*, *propertyEvaluationFrequency*.The following 
    # optional arguments are ignored unless *eigensolver*=LANCZOS or AMS: *minEigen*, 
    # *maxEigen*, and *acousticCoupling*.The following optional arguments are ignored unless 
    # *eigensolver*=AMS: *projectDamping*, *acousticRangeFactor*, 
    # *substructureCutoffMultiplier*, *firstCutoffMultiplier*, *secondCutoffMultiplier*, 
    # *residualModeRegion*, *regionalModeDof*, and *limitSavedEigenvectorRegion*. 
    eigensolver: SymbolicConstant = None

    # The SymbolicConstant ALL or an Int specifying the number of eigenvalues to be calculated 
    # or ALL. The default value is ALL. 
    numEigen: SymbolicConstant = ALL

    # A Float specifying the shift point in cycles per time. The default value is 0.0. 
    shift: float = 0

    # None or a Float specifying the minimum frequency of interest in cycles per time. The 
    # default value is None. 
    minEigen: float = None

    # None or a Float specifying the maximum frequency of interest in cycles per time. The 
    # default value is None. 
    maxEigen: float = None

    # None or an Int specifying the number of vectors used in the iteration. The default is 
    # the minimum of (2*n*, *n* + 8), where *n* is the number of eigenvalues requested. The 
    # default value is None. 
    vectors: int = None

    # An Int specifying the maximum number of iterations. The default value is 30. 
    maxIterations: int = 30

    # A SymbolicConstant specifying the size of the Lanczos block steps. The default value is 
    # DEFAULT. 
    blockSize: SymbolicConstant = DEFAULT

    # A SymbolicConstant specifying the maximum number of Lanczos block steps within each 
    # Lanczos run. The default value is DEFAULT. 
    maxBlocks: SymbolicConstant = DEFAULT

    # A SymbolicConstant specifying the method for normalizing eigenvectors. Possible values 
    # are DISPLACEMENT and MASS. The default value is DISPLACEMENT.A value of DISPLACEMENT 
    # indicates normalizing the eigenvectors so that the largest displacement entry in each 
    # vector is unity. A value of MASS indicates normalizing the eigenvectors with respect to 
    # the structure's mass matrix, which results in scaling the eigenvectors so that the 
    # generalized mass for each vector is unity. 
    normalization: SymbolicConstant = DISPLACEMENT

    # None or a Float specifying the frequency at which to evaluate frequency-dependent 
    # properties for viscoelasticity, springs, and dashpots during the eigenvalue extraction. 
    # If the value is None, the analysis product will evaluate the stiffness associated with 
    # frequency-dependent springs and dashpots at zero frequency and will not consider the 
    # stiffness contributions from frequency-domain viscoelasticity in the step. The default 
    # value is None. 
    propertyEvaluationFrequency: float = None

    # A Boolean specifying whether to include projection of viscous and structural damping 
    # operators during *AMS* eigenvalue extraction. Valid only when *eigenSolver*=AMS. The 
    # default value is ON. 
    projectDamping: Boolean = ON

    # A SymbolicConstant specifying the type of acoustic-structural coupling in models with 
    # acoustic and structural elements coupled using the TIE option or in models with ASI-type 
    # elements. Possible values are AC_ON, AC_OFF, and AC_PROJECTION. The default value is 
    # AC_ON. 
    acousticCoupling: SymbolicConstant = AC_ON

    # A Float specifying the ratio of the maximum acoustic frequency to the maximum structural 
    # frequency. The default value is 1.0. 
    acousticRangeFactor: float = 1

    # A Boolean specifying whether to add to the damping matrix contributions due to friction 
    # effects. The default value is OFF. 
    frictionDamping: Boolean = OFF

    # A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
    # UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
    matrixStorage: SymbolicConstant = SOLVER_DEFAULT

    # A Boolean specifying whether to activate the SIM-based linear dynamics procedures. The 
    # default value is OFF. 
    simLinearDynamics: Boolean = OFF

    # A Boolean specifying whether to include residual modes from an immediately preceding 
    # Static, Linear Perturbation step. The default value is OFF. 
    residualModes: Boolean = OFF

    # A Float specifying the cutoff frequency for substructure eigenproblems, defined as a 
    # multiplier of the maximum frequency of interest. The default value is 5.0. 
    substructureCutoffMultiplier: float = 5

    # A Float specifying the first cutoff frequency for a reduced eigenproblem, defined as a 
    # multiplier of the maximum frequency of interest. The default value is 1.7. 
    firstCutoffMultiplier: float = 1

    # A Float specifying the second cutoff frequency for a reduced eigenproblem defined as a 
    # multiplier of the maximum frequency of interest. The default value is 1.1. 
    secondCutoffMultiplier: float = 1

    # A String specifying the name of the previous step. The new step appears after this step 
    # in the list of analysis steps. 
    previous: str = ''

    # A String specifying a description of the new step. The default value is an empty string. 
    description: str = ''

    # None or a tuple of Strings specifying the name of a region for which residual modes are 
    # requested. The default value is None. 
    residualModeRegion: tuple = None

    # None or a tuple of Ints specifying the degree of freedom for which residual modes are 
    # requested. The default value is None. 
    residualModeDof: int = None

    # None or a Region object specifying a region for which eigenvectors should be saved or 
    # the SymbolicConstant None representing the whole model. The default value is None. 
    limitSavedEigenvectorRegion: SymbolicConstant = None

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

    def __init__(self, name: str, previous: str, eigensolver: SymbolicConstant,
                 numEigen: SymbolicConstant = ALL, description: str = '', shift: float = 0,
                 minEigen: float = None, maxEigen: float = None, vectors: int = None,
                 maxIterations: int = 30, blockSize: SymbolicConstant = DEFAULT,
                 maxBlocks: SymbolicConstant = DEFAULT, normalization: SymbolicConstant = DISPLACEMENT,
                 propertyEvaluationFrequency: float = None, projectDamping: Boolean = ON,
                 acousticCoupling: SymbolicConstant = AC_ON, acousticRangeFactor: float = 1,
                 frictionDamping: Boolean = OFF, matrixStorage: SymbolicConstant = SOLVER_DEFAULT,
                 maintainAttributes: Boolean = False, simLinearDynamics: Boolean = OFF,
                 residualModes: Boolean = OFF, substructureCutoffMultiplier: float = 5,
                 firstCutoffMultiplier: float = 1, secondCutoffMultiplier: float = 1,
                 residualModeRegion: str = None, residualModeDof: str = None,
                 limitSavedEigenvectorRegion: SymbolicConstant = None):
        """This method creates a FrequencyStep object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].FrequencyStep
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        previous
            A String specifying the name of the previous step. The new step appears after this step 
            in the list of analysis steps. 
        eigensolver
            A SymbolicConstant specifying the eigensolver. Possible values are LANCZOS, SUBSPACE, 
            and AMS.The following optional arguments are ignored unless *eigensolver*=LANCZOS: 
            *blockSize*, *maxBlocks*, *normalization*, *propertyEvaluationFrequency*.The following 
            optional arguments are ignored unless *eigensolver*=LANCZOS or AMS: *minEigen*, 
            *maxEigen*, and *acousticCoupling*.The following optional arguments are ignored unless 
            *eigensolver*=AMS: *projectDamping*, *acousticRangeFactor*, 
            *substructureCutoffMultiplier*, *firstCutoffMultiplier*, *secondCutoffMultiplier*, 
            *residualModeRegion*, *regionalModeDof*, and *limitSavedEigenvectorRegion*. 
        numEigen
            The SymbolicConstant ALL or an Int specifying the number of eigenvalues to be calculated 
            or ALL. The default value is ALL. 
        description
            A String specifying a description of the new step. The default value is an empty string. 
        shift
            A Float specifying the shift point in cycles per time. The default value is 0.0. 
        minEigen
            None or a Float specifying the minimum frequency of interest in cycles per time. The 
            default value is None. 
        maxEigen
            None or a Float specifying the maximum frequency of interest in cycles per time. The 
            default value is None. 
        vectors
            None or an Int specifying the number of vectors used in the iteration. The default is 
            the minimum of (2*n*, *n* + 8), where *n* is the number of eigenvalues requested. The 
            default value is None. 
        maxIterations
            An Int specifying the maximum number of iterations. The default value is 30. 
        blockSize
            A SymbolicConstant specifying the size of the Lanczos block steps. The default value is 
            DEFAULT. 
        maxBlocks
            A SymbolicConstant specifying the maximum number of Lanczos block steps within each 
            Lanczos run. The default value is DEFAULT. 
        normalization
            A SymbolicConstant specifying the method for normalizing eigenvectors. Possible values 
            are DISPLACEMENT and MASS. The default value is DISPLACEMENT.A value of DISPLACEMENT 
            indicates normalizing the eigenvectors so that the largest displacement entry in each 
            vector is unity. A value of MASS indicates normalizing the eigenvectors with respect to 
            the structure's mass matrix, which results in scaling the eigenvectors so that the 
            generalized mass for each vector is unity. 
        propertyEvaluationFrequency
            None or a Float specifying the frequency at which to evaluate frequency-dependent 
            properties for viscoelasticity, springs, and dashpots during the eigenvalue extraction. 
            If the value is None, the analysis product will evaluate the stiffness associated with 
            frequency-dependent springs and dashpots at zero frequency and will not consider the 
            stiffness contributions from frequency-domain viscoelasticity in the step. The default 
            value is None. 
        projectDamping
            A Boolean specifying whether to include projection of viscous and structural damping 
            operators during *AMS* eigenvalue extraction. Valid only when *eigenSolver*=AMS. The 
            default value is ON. 
        acousticCoupling
            A SymbolicConstant specifying the type of acoustic-structural coupling in models with 
            acoustic and structural elements coupled using the TIE option or in models with ASI-type 
            elements. Possible values are AC_ON, AC_OFF, and AC_PROJECTION. The default value is 
            AC_ON. 
        acousticRangeFactor
            A Float specifying the ratio of the maximum acoustic frequency to the maximum structural 
            frequency. The default value is 1.0. 
        frictionDamping
            A Boolean specifying whether to add to the damping matrix contributions due to friction 
            effects. The default value is OFF. 
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
        maintainAttributes
            A Boolean specifying whether to retain attributes from an existing step with the same 
            name. The default value is False. 
        simLinearDynamics
            A Boolean specifying whether to activate the SIM-based linear dynamics procedures. The 
            default value is OFF. 
        residualModes
            A Boolean specifying whether to include residual modes from an immediately preceding 
            Static, Linear Perturbation step. The default value is OFF. 
        substructureCutoffMultiplier
            A Float specifying the cutoff frequency for substructure eigenproblems, defined as a 
            multiplier of the maximum frequency of interest. The default value is 5.0. 
        firstCutoffMultiplier
            A Float specifying the first cutoff frequency for a reduced eigenproblem, defined as a 
            multiplier of the maximum frequency of interest. The default value is 1.7. 
        secondCutoffMultiplier
            A Float specifying the second cutoff frequency for a reduced eigenproblem defined as a 
            multiplier of the maximum frequency of interest. The default value is 1.1. 
        residualModeRegion
            None or a sequence of Strings specifying the name of a region for which residual modes 
            are requested. The default value is None. 
        residualModeDof
            None or a sequence of Ints specifying the degree of freedom for which residual modes are 
            requested. The default value is None. 
        limitSavedEigenvectorRegion
            None or a Region object specifying a region for which eigenvectors should be saved or 
            the SymbolicConstant None representing the whole model. The default value is None. 

        Returns
        -------
            A FrequencyStep object. 

        Raises
        ------
        RangeError
        """
        super().__init__()
        pass

    def setValues(self, numEigen: SymbolicConstant = ALL, description: str = '', shift: float = 0,
                  minEigen: float = None, maxEigen: float = None, vectors: int = None,
                  maxIterations: int = 30, blockSize: SymbolicConstant = DEFAULT,
                  maxBlocks: SymbolicConstant = DEFAULT, normalization: SymbolicConstant = DISPLACEMENT,
                  propertyEvaluationFrequency: float = None, projectDamping: Boolean = ON,
                  acousticCoupling: SymbolicConstant = AC_ON, acousticRangeFactor: float = 1,
                  frictionDamping: Boolean = OFF, matrixStorage: SymbolicConstant = SOLVER_DEFAULT,
                  simLinearDynamics: Boolean = OFF, residualModes: Boolean = OFF,
                  substructureCutoffMultiplier: float = 5, firstCutoffMultiplier: float = 1,
                  secondCutoffMultiplier: float = 1, residualModeRegion: str = None,
                  residualModeDof: str = None, limitSavedEigenvectorRegion: SymbolicConstant = None):
        """This method modifies the FrequencyStep object.
        
        Parameters
        ----------
        numEigen
            The SymbolicConstant ALL or an Int specifying the number of eigenvalues to be calculated 
            or ALL. The default value is ALL. 
        description
            A String specifying a description of the new step. The default value is an empty string. 
        shift
            A Float specifying the shift point in cycles per time. The default value is 0.0. 
        minEigen
            None or a Float specifying the minimum frequency of interest in cycles per time. The 
            default value is None. 
        maxEigen
            None or a Float specifying the maximum frequency of interest in cycles per time. The 
            default value is None. 
        vectors
            None or an Int specifying the number of vectors used in the iteration. The default is 
            the minimum of (2*n*, *n* + 8), where *n* is the number of eigenvalues requested. The 
            default value is None. 
        maxIterations
            An Int specifying the maximum number of iterations. The default value is 30. 
        blockSize
            A SymbolicConstant specifying the size of the Lanczos block steps. The default value is 
            DEFAULT. 
        maxBlocks
            A SymbolicConstant specifying the maximum number of Lanczos block steps within each 
            Lanczos run. The default value is DEFAULT. 
        normalization
            A SymbolicConstant specifying the method for normalizing eigenvectors. Possible values 
            are DISPLACEMENT and MASS. The default value is DISPLACEMENT.A value of DISPLACEMENT 
            indicates normalizing the eigenvectors so that the largest displacement entry in each 
            vector is unity. A value of MASS indicates normalizing the eigenvectors with respect to 
            the structure's mass matrix, which results in scaling the eigenvectors so that the 
            generalized mass for each vector is unity. 
        propertyEvaluationFrequency
            None or a Float specifying the frequency at which to evaluate frequency-dependent 
            properties for viscoelasticity, springs, and dashpots during the eigenvalue extraction. 
            If the value is None, the analysis product will evaluate the stiffness associated with 
            frequency-dependent springs and dashpots at zero frequency and will not consider the 
            stiffness contributions from frequency-domain viscoelasticity in the step. The default 
            value is None. 
        projectDamping
            A Boolean specifying whether to include projection of viscous and structural damping 
            operators during *AMS* eigenvalue extraction. Valid only when *eigenSolver*=AMS. The 
            default value is ON. 
        acousticCoupling
            A SymbolicConstant specifying the type of acoustic-structural coupling in models with 
            acoustic and structural elements coupled using the TIE option or in models with ASI-type 
            elements. Possible values are AC_ON, AC_OFF, and AC_PROJECTION. The default value is 
            AC_ON. 
        acousticRangeFactor
            A Float specifying the ratio of the maximum acoustic frequency to the maximum structural 
            frequency. The default value is 1.0. 
        frictionDamping
            A Boolean specifying whether to add to the damping matrix contributions due to friction 
            effects. The default value is OFF. 
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC, 
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT. 
        simLinearDynamics
            A Boolean specifying whether to activate the SIM-based linear dynamics procedures. The 
            default value is OFF. 
        residualModes
            A Boolean specifying whether to include residual modes from an immediately preceding 
            Static, Linear Perturbation step. The default value is OFF. 
        substructureCutoffMultiplier
            A Float specifying the cutoff frequency for substructure eigenproblems, defined as a 
            multiplier of the maximum frequency of interest. The default value is 5.0. 
        firstCutoffMultiplier
            A Float specifying the first cutoff frequency for a reduced eigenproblem, defined as a 
            multiplier of the maximum frequency of interest. The default value is 1.7. 
        secondCutoffMultiplier
            A Float specifying the second cutoff frequency for a reduced eigenproblem defined as a 
            multiplier of the maximum frequency of interest. The default value is 1.1. 
        residualModeRegion
            None or a sequence of Strings specifying the name of a region for which residual modes 
            are requested. The default value is None. 
        residualModeDof
            None or a sequence of Ints specifying the degree of freedom for which residual modes are 
            requested. The default value is None. 
        limitSavedEigenvectorRegion
            None or a Region object specifying a region for which eigenvectors should be saved or 
            the SymbolicConstant None representing the whole model. The default value is None.

        Raises
        ------
        RangeError
        """
        pass
