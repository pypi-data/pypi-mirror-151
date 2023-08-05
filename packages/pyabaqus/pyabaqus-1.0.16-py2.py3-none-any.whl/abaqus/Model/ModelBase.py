from abaqusConstants import *

from .KeywordBlock import KeywordBlock
from ..Adaptivity.AdaptiveMeshConstraint import AdaptiveMeshConstraint
from ..Adaptivity.AdaptiveMeshControl import AdaptiveMeshControl
from ..Adaptivity.RemeshingRule import RemeshingRule
from ..Amplitude.Amplitude import Amplitude
from ..Assembly.Assembly import Assembly
from ..BeamSectionProfile.Profile import Profile
from ..BoundaryCondition.BoundaryCondition import BoundaryCondition
from ..BoundaryCondition.Calibration import Calibration
from ..Constraint.Constraint import Constraint
from ..Feature.FeatureOptions import FeatureOptions
from ..Field.AnalyticalField import AnalyticalField
from ..Field.DiscreteField import DiscreteField
from ..Filter.Filter import Filter
from ..Interaction.ContactControl import ContactControl
from ..Interaction.ContactInitialization import ContactInitialization
from ..Interaction.ContactProperty import ContactProperty
from ..Interaction.ContactStabilization import ContactStabilization
from ..Interaction.Interaction import Interaction
from ..Load.Load import Load
from ..Material.Material import Material
from ..Optimization.OptimizationTask import OptimizationTask
from ..Part.Part import Part
from ..PredefinedField.PredefinedField import PredefinedField
from ..Section.Section import Section
from ..Sketcher.ConstrainedSketch import ConstrainedSketch
from ..Step.InitialStep import InitialStep
from ..Step.Step import Step
from ..StepOutput.FieldOutputRequest import FieldOutputRequest
from ..StepOutput.HistoryOutputRequest import HistoryOutputRequest
from ..StepOutput.IntegratedOutputSection import IntegratedOutputSection
from ..StepOutput.TimePoint import TimePoint
from ..TableCollection.EventSeriesData import EventSeriesData
from ..TableCollection.EventSeriesType import EventSeriesType
from ..TableCollection.TableCollection import TableCollection


class ModelBase:
    """Abaqus creates a Model object named `Model-1` when a session is started.

    Attributes
    ----------
    name: str
        A String specifying the repository key.
    stefanBoltzmann: float
        None or a Float specifying the Stefan-Boltzmann constant. The default value is None.
    absoluteZero: float
        None or a Float specifying the absolute zero constant. The default value is None.
    waveFormulation: SymbolicConstant
        A SymbolicConstant specifying the type of incident wave formulation to be used in
        acoustic problems. Possible values are NOT_SET, SCATTERED, and TOTAL. The default value
        is NOT_SET.
    universalGas: float
        None or a Float specifying the universal gas constant. The default value is None.
    noPartsInputFile: Boolean
        A Boolean specifying whether an input file should be written without parts and
        assemblies. The default value is OFF.
    restartIncrement: SymbolicConstant
        An Int specifying the increment, interval, iteration or cycle where the restart analysis
        will start. To select the end of the step use the SymbolicConstant STEP_END.
    endRestartStep: Boolean
        A Boolean specifying that the step specified by **restartStep** should be terminated at
        the increment specified by **restartIncrement**.
    shellToSolid: Boolean
        A Boolean specifying that a shell global model drives a solid submodel.
    lastChangedCount: float
        A Float specifying the time stamp that indicates when the model was last changed.
    description: str
        A String specifying the purpose and contents of the :py:class:`~abaqus.Model.Model.Model` object. The default value is
        an empty string.
    restartJob: str
        A String specifying the name of the job that generated the restart data.
    restartStep: str
        A String specifying the name of the step where the restart analysis will start.
    globalJob: str
        A String specifying the name of the job that generated the results for the global model.
    copyConstraints: Boolean
        A boolean specifying the status of constraints created in a model, in the model which
        instances this model.
    copyConnectors: Boolean
        A boolean specifying the status of connectors created in a model, in the model which
        instances this model.
    copyInteractions: Boolean
        A boolean specifying the status of interactions created in a model, in the model which
        instances this model.
    keywordBlock: KeywordBlock
        A :py:class:`~abaqus.Model.KeywordBlock.KeywordBlock` object.
    rootAssembly: Assembly
        An :py:class:`~abaqus.Assembly.Assembly.Assembly` object.
    amplitudes: dict[str, Amplitude]
        A repository of :py:class:`~abaqus.Amplitude.Amplitude.Amplitude` objects.
    profiles: dict[str, Profile]
        A repository of :py:class:`~abaqus.BeamSectionProfile.Profile.Profile` objects.
    boundaryConditions: dict[str, BoundaryCondition]
        A repository of :py:class:`~abaqus.BoundaryCondition.BoundaryCondition.BoundaryCondition` objects.
    constraints: dict[str, Constraint]
        A repository of :py:class:`~abaqus.Sketcher.ConstrainedSketchConstraint.ConstrainedSketchConstraint.ConstrainedSketchConstraint` objects.
    analyticalFields: dict[str, AnalyticalField]
        A repository of :py:class:`~abaqus.Field.AnalyticalField.AnalyticalField` objects.
    discreteFields: dict[str, DiscreteField]
        A repository of :py:class:`~abaqus.Field.DiscreteField.DiscreteField` objects.
    predefinedFields: dict[str, PredefinedField]
        A repository of :py:class:`~abaqus.PredefinedField.PredefinedField.PredefinedField` objects.
    interactions: dict[str, Interaction]
        A repository of :py:class:`~abaqus.Interaction.Interaction.Interaction` objects.
    interactionProperties: dict[str, ContactProperty]
        A repository of :py:class:`~abaqus.Interaction.InteractionProperty.InteractionProperty` objects.
    contactControls: dict[str, ContactControl]
        A repository of :py:class:`~abaqus.Interaction.ContactControl.ContactControl` objects.
    contactInitializations: dict[str, ContactInitialization]
        A repository of :py:class:`~abaqus.Interaction.ContactInitialization.ContactInitialization` objects.
    contactStabilizations: dict[str, ContactStabilization]
        A repository of :py:class:`~abaqus.Interaction.ContactStabilization.ContactStabilization` objects.
    linkedInstances: tuple
        A tuple of tuples of Strings specifying the linked child PartInstance name in the
        current model to the corresponding parent PartInstance name in a different model.
    linkedParts: tuple
        A tuple of tuples of Strings specifying the linked child Part name in the current model
        to the corresponding parent Part name in a different model.
    loads: dict[str, Load]
        A repository of :py:class:`~abaqus.Load.Load.Load` objects.
    materials: dict[str, Material]
        A repository of :py:class:`~abaqus.Material.Material.Material` objects.
    calibrations: dict[str, Calibration]
        A repository of :py:class:`~abaqus.BoundaryCondition.Calibration.Calibration` objects.
    sections: dict[str, Section]
        A repository of :py:class:`~abaqus.Section.Section.Section` objects.
    remeshingRules: dict[str, RemeshingRule]
        A repository of :py:class:`~abaqus.Adaptivity.RemeshingRule.RemeshingRule` objects.
    sketches: dict[str, ConstrainedSketch]
        A repository of :py:class:`~abaqus.Sketcher.ConstrainedSketch.ConstrainedSketch` objects.
    parts: dict[str, Part]
        A repository of :py:class:`~abaqus.Part.Part.Part` objects.
    steps: dict[str, Step]
        A repository of :py:class:`~abaqus.Step.Step.Step` objects.
    featureOptions: FeatureOptions
        A :py:class:`~abaqus.Feature.FeatureOptions.FeatureOptions` object.
    adaptiveMeshConstraints: dict[str, AdaptiveMeshConstraint]
        A repository of :py:class:`~abaqus.Adaptivity.AdaptiveMeshConstraint.AdaptiveMeshConstraint` objects.
    adaptiveMeshControls: dict[str, AdaptiveMeshControl]
        A repository of :py:class:`~abaqus.Adaptivity.AdaptiveMeshControl.AdaptiveMeshControl` objects.
    timePoints: dict[str, TimePoint]
        A repository of :py:class:`~abaqus.StepOutput.TimePoint.TimePoint` objects.
    filters: dict[str, Filter]
        A repository of :py:class:`~abaqus.Filter.Filter.Filter` objects.
    integratedOutputSections: dict[str, IntegratedOutputSection]
        A repository of :py:class:`~abaqus.StepOutput.IntegratedOutputSection.IntegratedOutputSection` objects.
    fieldOutputRequests: dict[str, FieldOutputRequest]
        A repository of :py:class:`~abaqus.StepOutput.FieldOutputRequest.FieldOutputRequest` objects.
    historyOutputRequests: dict[str, HistoryOutputRequest]
        A repository of :py:class:`~abaqus.StepOutput.HistoryOutputRequest.HistoryOutputRequest` objects.
    optimizationTasks: dict[str, OptimizationTask]
        A repository of :py:class:`~abaqus.Optimization.OptimizationTask.OptimizationTask` objects.
    tableCollections: dict[str, TableCollection]
        A repository of :py:class:`~abaqus.TableCollection.TableCollection.TableCollection` objects.
    eventSeriesTypes: dict[str, EventSeriesType]
        A repository of :py:class:`~abaqus.TableCollection.EventSeriesType.EventSeriesType` objects.
    eventSeriesDatas: dict[str, EventSeriesData]
        A repository of :py:class:`~abaqus.TableCollection.EventSeriesData.EventSeriesData` objects.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        mdb.models[name]

    The corresponding analysis keywords are:

    - PHYSICAL CONSTANTS

    """

    # A String specifying the repository key. 
    name: str = ''

    # None or a Float specifying the Stefan-Boltzmann constant. The default value is None. 
    stefanBoltzmann: float = None

    # None or a Float specifying the absolute zero constant. The default value is None. 
    absoluteZero: float = None

    # A SymbolicConstant specifying the type of incident wave formulation to be used in 
    # acoustic problems. Possible values are NOT_SET, SCATTERED, and TOTAL. The default value 
    # is NOT_SET. 
    waveFormulation: SymbolicConstant = NOT_SET

    # None or a Float specifying the universal gas constant. The default value is None. 
    universalGas: float = None

    # A Boolean specifying whether an input file should be written without parts and 
    # assemblies. The default value is OFF. 
    noPartsInputFile: Boolean = OFF

    # An Int specifying the increment, interval, iteration or cycle where the restart analysis 
    # will start. To select the end of the step use the SymbolicConstant STEP_END. 
    restartIncrement: SymbolicConstant = None

    # A Boolean specifying that the step specified by *restartStep* should be terminated at 
    # the increment specified by *restartIncrement*. 
    endRestartStep: Boolean = OFF

    # A Boolean specifying that a shell global model drives a solid submodel. 
    shellToSolid: Boolean = OFF

    # A Float specifying the time stamp that indicates when the model was last changed. 
    lastChangedCount: float = None

    # A String specifying the purpose and contents of the Model object. The default value is 
    # an empty string. 
    description: str = ''

    # A String specifying the name of the job that generated the restart data. 
    restartJob: str = ''

    # A String specifying the name of the step where the restart analysis will start. 
    restartStep: str = ''

    # A String specifying the name of the job that generated the results for the global model. 
    globalJob: str = ''

    # A boolean specifying the status of constraints created in a model, in the model which 
    # instances this model. 
    copyConstraints: Boolean = OFF

    # A boolean specifying the status of connectors created in a model, in the model which 
    # instances this model. 
    copyConnectors: Boolean = OFF

    # A boolean specifying the status of interactions created in a model, in the model which 
    # instances this model. 
    copyInteractions: Boolean = OFF

    # A KeywordBlock object. 
    keywordBlock: KeywordBlock = KeywordBlock()

    # An Assembly object. 
    rootAssembly: Assembly = Assembly()

    # A repository of Amplitude objects. 
    amplitudes: dict[str, Amplitude] = dict[str, Amplitude]()

    # A repository of Profile objects. 
    profiles: dict[str, Profile] = dict[str, Profile]()

    # A repository of BoundaryCondition objects. 
    boundaryConditions: dict[str, BoundaryCondition] = dict[str, BoundaryCondition]()

    # A repository of ConstrainedSketchConstraint objects.
    constraints: dict[str, Constraint] = dict[str, Constraint]()

    # A repository of AnalyticalField objects. 
    analyticalFields: dict[str, AnalyticalField] = dict[str, AnalyticalField]()

    # A repository of DiscreteField objects. 
    discreteFields: dict[str, DiscreteField] = dict[str, DiscreteField]()

    # A repository of PredefinedField objects. 
    predefinedFields: dict[str, PredefinedField] = dict[str, PredefinedField]()

    # A repository of Interaction objects. 
    interactions: dict[str, Interaction] = dict[str, Interaction]()

    # A repository of InteractionProperty objects. 
    interactionProperties: dict[str, ContactProperty] = dict[str, ContactProperty]()

    # A repository of ContactControl objects. 
    contactControls: dict[str, ContactControl] = dict[str, ContactControl]()

    # A repository of ContactInitialization objects. 
    contactInitializations: dict[str, ContactInitialization] = dict[str, ContactInitialization]()

    # A repository of ContactStabilization objects. 
    contactStabilizations: dict[str, ContactStabilization] = dict[str, ContactStabilization]()

    # A tuple of tuples of Strings specifying the linked child PartInstance name in the 
    # current model to the corresponding parent PartInstance name in a different model. 
    linkedInstances: tuple = ()

    # A tuple of tuples of Strings specifying the linked child Part name in the current model 
    # to the corresponding parent Part name in a different model. 
    linkedParts: tuple = ()

    # A repository of Load objects. 
    loads: dict[str, Load] = dict[str, Load]()

    # A repository of Material objects. 
    materials: dict[str, Material] = dict[str, Material]()

    # A repository of Calibration objects. 
    calibrations: dict[str, Calibration] = dict[str, Calibration]()

    # A repository of Section objects. 
    sections: dict[str, Section] = dict[str, Section]()

    # A repository of RemeshingRule objects. 
    remeshingRules: dict[str, RemeshingRule] = dict[str, RemeshingRule]()

    # A repository of ConstrainedSketch objects. 
    sketches: dict[str, ConstrainedSketch] = dict[str, ConstrainedSketch]()

    # A repository of Part objects. 
    parts: dict[str, Part] = dict[str, Part]()

    # A repository of Step objects. 
    steps: dict[str, Step] = dict[str, Step]()

    # A FeatureOptions object. 
    featureOptions: FeatureOptions = FeatureOptions()

    # A repository of AdaptiveMeshConstraint objects. 
    adaptiveMeshConstraints: dict[str, AdaptiveMeshConstraint] = dict[str, AdaptiveMeshConstraint]()

    # A repository of AdaptiveMeshControl objects. 
    adaptiveMeshControls: dict[str, AdaptiveMeshControl] = dict[str, AdaptiveMeshControl]()

    # A repository of TimePoint objects. 
    timePoints: dict[str, TimePoint] = dict[str, TimePoint]()

    # A repository of Filter objects. 
    filters: dict[str, Filter] = dict[str, Filter]()

    # A repository of IntegratedOutputSection objects. 
    integratedOutputSections: dict[str, IntegratedOutputSection] = dict[str, IntegratedOutputSection]()

    # A repository of FieldOutputRequest objects. 
    fieldOutputRequests: dict[str, FieldOutputRequest] = dict[str, FieldOutputRequest]()

    # A repository of HistoryOutputRequest objects. 
    historyOutputRequests: dict[str, HistoryOutputRequest] = dict[str, HistoryOutputRequest]()

    # A repository of OptimizationTask objects. 
    optimizationTasks: dict[str, OptimizationTask] = dict[str, OptimizationTask]()

    # A repository of TableCollection objects. 
    tableCollections: dict[str, TableCollection] = dict[str, TableCollection]()

    # A repository of EventSeriesType objects. 
    eventSeriesTypes: dict[str, EventSeriesType] = dict[str, EventSeriesType]()

    # A repository of EventSeriesData objects. 
    eventSeriesDatas: dict[str, EventSeriesData] = dict[str, EventSeriesData]()

    def __init__(self, name: str, description: str = '', stefanBoltzmann: float = None,
                 absoluteZero: float = None, waveFormulation: SymbolicConstant = NOT_SET,
                 modelType: SymbolicConstant = STANDARD_EXPLICIT, universalGas: float = None,
                 copyConstraints: Boolean = ON, copyConnectors: Boolean = ON,
                 copyInteractions: Boolean = ON):
        """This method creates a Model object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.Model
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        description
            A String specifying the purpose and contents of the Model object. The default value is 
            an empty string. 
        stefanBoltzmann
            None or a Float specifying the Stefan-Boltzmann constant. The default value is None. 
        absoluteZero
            None or a Float specifying the absolute zero constant. The default value is None. 
        waveFormulation
            A SymbolicConstant specifying the type of incident wave formulation to be used in 
            acoustic problems. Possible values are NOT_SET, SCATTERED, and TOTAL. The default value 
            is NOT_SET. 
        modelType
            A SymbolicConstant specifying the analysis model type. Possible values are 
            STANDARD_EXPLICIT and ELECTROMAGNETIC. The default is STANDARD_EXPLICIT. 
        universalGas
            None or a Float specifying the universal gas constant. The default value is None. 
        copyConstraints
            A boolean specifying whether to copy the constraints created in the model to the model 
            that instances this model. The default value is ON. 
        copyConnectors
            A boolean specifying whether to copy the connectors created in the model to the model 
            that instances this model. The default value is ON. 
        copyInteractions
            A boolean specifying whether to copy the interactions created in the model to the model 
            that instances this model. The default value is ON. 

        Returns
        -------
            A Model object.
        """
        self.steps['Initial'] = InitialStep()

    def ModelFromInputFile(self, name: str, inputFileName: str):
        """This method creates a Model object by reading the keywords in an input file and creating
        the corresponding Abaqus/CAE objects.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.Model
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        inputFileName
            A String specifying the name of the input file (including the .inp extension) to be 
            parsed into the new model. This String can also be the full path to the input file if it 
            is located in another directory. 

        Returns
        -------
            A Model object.
        """
        pass

    def ModelFromOdbFile(self, name: str, odbFileName: str):
        """This method creates a Model object by reading an output database and creating any
        corresponding Abaqus/CAE objects.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.Model
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        odbFileName
            A String specifying the name of the output database file (including the .odb extension) 
            to be read into the new model. This String can also be the full path to the output 
            database file if it is located in another directory. 

        Returns
        -------
            A Model object.
        """
        pass

    def ModelFromNastranFile(self, modelName: str, inputFileName: str,
                             sectionConsolidation: SymbolicConstant = PRESERVE_SECTION,
                             preIntegratedShell: Boolean = OFF, weightMassScaling: Boolean = ON,
                             loadCases: Boolean = ON, coupleBeamOffsets: Boolean = ON, cbar: str = B31,
                             cquad4: str = S4, chexa: str = C3D8I, ctetra: str = C3D10,
                             keepTranslatedFiles: Boolean = ON):
        """This method creates a Model object by reading the keywords in a Nastran bulk data file
        or Nastran input file and creating any corresponding Abaqus/CAE objects. The default
        values is discussed in following and can be defined alternatively in the Abaqus
        environment file as the one used for the translator from Nastran to Abaqus. For more
        information, see Translating Nastran data to Abaqus files.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.Model
        
        Parameters
        ----------
        modelName
            A String specifying the repository key. 
        inputFileName
            A String specifying the name of the Nastran input file (including the .bdf, .dat, .nas, 
            .nastran, .blk, .bulk extension) to be read into the new model. This String can also be 
            the full path to the Nastran input file if it is located in another directory. 
        sectionConsolidation
            A SymbolicConstant specifying the method used to create shell section. Possible values 
            are PRESERVE_SECTION, GROUP_BY_MATERIAL, and NONE. If PRESERVE_SECTION is used, an 
            Abaqus section is created corresponding to each shell property ID. If GROUP_BY_MATERIAL 
            is used, a single Abaqus section is created for all homogeneous elements referencing the 
            same material. In both cases, material orientations and offsets are created using 
            discrete fields. If NONE is used, a separate shell section is created for each 
            combination of orientation, material offset, and/or thickness. The default is 
            PRESERVE_SECTION. 
        preIntegratedShell
            A Boolean specifying whether the pre-integrated shell section is created in default for 
            shell element. The default value is OFF. 
        weightMassScaling
            A Boolean specifying whether the value on the Nastran data line PARAM, WTMASS is used as 
            a multiplier for all density, mass, and rotary inertia values created in the Abaqus 
            input file. The default value is ON. 
        loadCases
            A Boolean specifying whether each SUBCASE for linear static analyses is translated to a 
            LOAD CASE option, and all such LOAD CASE options are grouped in a single STEP option. 
            The default value is ON. 
        coupleBeamOffsets
            A Boolean specifying whether to translate the beam element connectivity to newly created 
            nodes at the offset location and rigidly coupling the new and original nodes. If not, 
            beam element offsets are translated to the CENTROID and SHEAR CENTER options, which are 
            suboptions of the BEAM GENERAL SECTION option. The default value is ON. When the beam 
            element references a PBARL or PBEAML property or if the beam offset has a significant 
            component in the direction of the beam axis, the setting for this argument is always ON. 
        cbar
            A String specifying the 2-node beam that is created from CBAR and CBEAM elements. 
            Possible values are B31 and B33. The default is B31. 
        cquad4
            A String specifying the 4-node shell that is created from CQUAD4 elements. Possible 
            values are S4 and S4R. The default is S4. If a reduced-integration element is chosen, 
            the enhanced hourglass formulation is applied automatically. 
        chexa
            A String specifying the 8-node brick that is created from CHEXA elements. Possible 
            values are C3D8I, C3D8 and C3D8R. The default is C3D8I. If a reduced-integration element 
            is chosen, the enhanced hourglass formulation is applied automatically. 
        ctetra
            A String specifying the 10-node tetrahedron that is created from CTETRA elements. 
            Possible values are C3D10 and C3D10M. The default is C3D10. 
        keepTranslatedFiles
            A Boolean specifying whether to keep the generated Abaqus input file after the model is 
            created from the Nastran input file. The default value is ON. 

        Returns
        -------
            A Model object.
        """
        pass

    def setValues(self, description: str = '', noPartsInputFile: Boolean = OFF, absoluteZero: float = None,
                  stefanBoltzmann: float = None, waveFormulation: SymbolicConstant = NOT_SET,
                  universalGas: float = None, restartJob: str = '', restartStep: str = '',
                  restartIncrement: SymbolicConstant = None, endRestartStep: Boolean = OFF,
                  globalJob: str = '', shellToSolid: Boolean = OFF, copyConstraints: Boolean = OFF,
                  copyConnectors: Boolean = OFF, copyInteractions: Boolean = OFF):
        """This method modifies the Model object.
        
        Parameters
        ----------
        description
            A String specifying the purpose and contents of the Model object. The default value is 
            an empty string. 
        noPartsInputFile
            A Boolean specifying whether an input file should be written without parts and 
            assemblies. The default value is OFF. 
        absoluteZero
            None or a Float specifying the absolute zero constant. The default value is None. 
        stefanBoltzmann
            None or a Float specifying the Stefan-Boltzmann constant. The default value is None. 
        waveFormulation
            A SymbolicConstant specifying the type of incident wave formulation to be used in 
            acoustic problems. Possible values are NOT_SET, SCATTERED, and TOTAL. The default value 
            is NOT_SET. 
        universalGas
            None or a Float specifying the universal gas constant. The default value is None. 
        restartJob
            A String specifying the name of the job that generated the restart data. 
        restartStep
            A String specifying the name of the step where the restart analysis will start. 
        restartIncrement
            An Int specifying the increment, interval, iteration or cycle where the restart analysis 
            will start. To select the end of the step use the SymbolicConstant STEP_END. 
        endRestartStep
            A Boolean specifying that the step specified by *restartStep* should be terminated at 
            the increment specified by *restartIncrement*. 
        globalJob
            A String specifying the name of the job that generated the results for the global model. 
        shellToSolid
            A Boolean specifying that a shell global model drives a solid submodel. 
        copyConstraints
            A Boolean specifying whether to copy the constraints created in the model to the model 
            that instances this model. 
        copyConnectors
            A Boolean specifying whether to copy the connectors created in the model to the model 
            that instances this model 
        copyInteractions
            A Boolean specifying whether to copy the interactions created in the model to the model 
            that instances this model. 
        """
        pass
