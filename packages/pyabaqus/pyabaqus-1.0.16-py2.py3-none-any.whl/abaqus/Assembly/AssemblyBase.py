import typing

from abaqusConstants import *
from .AssemblyModel import AssemblyModel
from .ConnectorOrientationArray import ConnectorOrientationArray
from .Feature import Feature
from .ModelInstance import ModelInstance
from .PartInstance import PartInstance
from ..BasicGeometry.EdgeArray import EdgeArray
from ..BasicGeometry.Face import Face
from ..BasicGeometry.ReferencePoint import ReferencePoint
from ..BasicGeometry.VertexArray import VertexArray
from ..Datum.Datum import Datum
from ..EngineeringFeature.EngineeringFeature import EngineeringFeature
from ..Mesh.MeshElement import MeshElement
from ..Mesh.MeshElementArray import MeshElementArray
from ..Mesh.MeshFace import MeshFace
from ..Mesh.MeshNode import MeshNode
from ..Mesh.MeshNodeArray import MeshNodeArray
from ..Part.Part import Part
from ..Property.SectionAssignmentArray import SectionAssignmentArray
from ..Region.Set import Set
from ..Region.Skin import Skin
from ..Region.Stringer import Stringer
from ..Region.Surface import Surface


class AssemblyBase(Feature):
    """An Assembly object is a container for instances of parts. The Assembly object has no
    constructor command. Abaqus creates the *rootAssembly* member when a Model object is 
    created. 

    Attributes
    ----------
    isOutOfDate: int
        An Int specifying that feature parameters have been modified but that the assembly has
        not been regenerated. Possible values are 0 and 1.
    timeStamp: float
        A Float specifying which gives an indication when the assembly was last modified.
    isLocked: int
        An Int specifying whether the assembly is locked or not. Possible values are 0 and 1.
    regenerateConstraintsTogether: Boolean
        A Boolean specifying whether the positioning constraints in the assembly should be
        regenerated together before regenerating other assembly features. The default value is
        ON.If the assembly has position constraint features and you modify the value of
        **regenerateConstraintsTogether**, Abaqus/CAE will regenerate the assembly features.
    vertices: VertexArray
        A :py:class:`~abaqus.BasicGeometry.VertexArray.VertexArray` object specifying all the vertices existing at the assembly level. This
        member does not provide access to the vertices at the instance level.
    edges: EdgeArray
        An :py:class:`~abaqus.BasicGeometry.EdgeArray.EdgeArray` object specifying all the edges existing at the assembly level. This member
        does not provide access to the edges at the instance level.
    elements: MeshElementArray
        A :py:class:`~abaqus.Mesh.MeshElementArray.MeshElementArray` object specifying all the elements existing at the assembly level.
        This member does not provide access to the elements at the instance level.
    nodes: MeshNodeArray
        A :py:class:`~abaqus.Mesh.MeshNodeArray.MeshNodeArray` object specifying all the nodes existing at the assembly level. This
        member does not provide access to the nodes at the instance level.
    instances: dict[str, PartInstance]
        A repository of :py:class:`~abaqus.Assembly.PartInstance.PartInstance` objects.
    datums: list[Datum]
        A repository of :py:class:`~abaqus.:py:class:`~abaqus.Datum.Datum.Datum`.:py:class:`~abaqus.Datum.Datum.Datum`.:py:class:`~abaqus.Datum.Datum.Datum`` objects specifying all :py:class:`~abaqus.:py:class:`~abaqus.Datum.Datum.Datum`.:py:class:`~abaqus.Datum.Datum.Datum`.:py:class:`~abaqus.Datum.Datum.Datum`` objects in the assembly.
    features: dict[str, Feature]
        A repository of :py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature`` objects specifying all :py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature`` objects in the assembly.
    featuresById: dict[str, Feature]
        A repository of :py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature``.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature```.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature``.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature```` objects specifying all :py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature``.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature```.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature``.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature```` objects in :py:class:`~.:py:class:`~.the`` assembly.The
        :py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature``.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature```.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature``.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature```` objects in :py:class:`~.:py:class:`~.the`` featuresById repository are :py:class:`~.:py:class:`~.the`` same as :py:class:`~.:py:class:`~.the`` :py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature``.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature```.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature``.:py:class:`~abaqus.Assembly.:py:class:`~abaqus.Assembly.Feature.Feature`.:py:class:`~abaqus.Assembly.Feature.Feature```` objects in
        :py:class:`~.:py:class:`~.the`` features repository. However, :py:class:`~.:py:class:`~.the`` key to :py:class:`~.:py:class:`~.the`` objects in :py:class:`~.:py:class:`~.the`` featuresById repository
        is an integer specifying :py:class:`~.:py:class:`~.the`` **ID**, whereas :py:class:`~.:py:class:`~.the`` key to :py:class:`~.:py:class:`~.the`` objects in :py:class:`~.:py:class:`~.the`` features
        repository is a string specifying :py:class:`~.:py:class:`~.the`` **name**.
    surfaces: dict[str, Surface]
        A repository of :py:class:`~abaqus.Region.Surface.Surface` objects specifying for more information, see [Region
        commands](https://help.3ds.com/2022/english/DSSIMULIA_Established/SIMACAEKERRefMap/simaker-m-RegPyc-sb.htm?ContextScope=all).
    allSurfaces: dict[str, Surface]
        A repository of :py:class:`~abaqus.Region.Surface.Surface` objects specifying for more information, see [Region
        commands](https://help.3ds.com/2022/english/DSSIMULIA_Established/SIMACAEKERRefMap/simaker-m-RegPyc-sb.htm?ContextScope=all).
    allInternalSurfaces: dict[str, Surface]
        A repository of :py:class:`~abaqus.Region.Surface.Surface` objects specifying picked regions.
    sets: dict[str, Set]
        A repository of :py:class:`~abaqus.Region.Set.Set` objects.
    allSets: dict[str, Set]
        A repository of :py:class:`~abaqus.Region.Set.Set` objects specifying for more information, see [Region
        commands](https://help.3ds.com/2022/english/DSSIMULIA_Established/SIMACAEKERRefMap/simaker-m-RegPyc-sb.htm?ContextScope=all).
    allInternalSets: dict[str, Set]
        A repository of :py:class:`~abaqus.Region.Set.Set` objects specifying picked regions.
    skins: dict[str, Skin]
        A repository of :py:class:`~abaqus.Region.Skin.Skin` objects specifying the skins created on the assembly.
    stringers: dict[str, Stringer]
        A repository of :py:class:`~abaqus.Region.Stringer.Stringer` objects specifying the stringers created on the assembly.
    referencePoints: dict[str, ReferencePoint]
        A repository of :py:class:`~abaqus.BasicGeometry.ReferencePoint.ReferencePoint` objects.
    modelInstances: dict[str, ModelInstance]
        A repository of :py:class:`~abaqus.Model.Model.ModelInstance` objects.
    allInstances: dict[str, typing.Union[PartInstance, ModelInstance]]
        A :py:class:`~abaqus.Assembly.PartInstance.PartInstance` object specifying the :py:class:`~abaqus.Assembly.PartInstance.PartInstance`s and A :py:class:`~abaqus.Model.Model.ModelInstance` object specifying
        the :py:class:`~abaqus.Model.Model.ModelInstance`s.
    engineeringFeatures: EngineeringFeature
        An :py:class:`~abaqus.EngineeringFeature.EngineeringFeature.EngineeringFeature` object.
    modelName: str
        A String specifying the name of the model to which the assembly belongs.
    connectorOrientations: ConnectorOrientationArray
        A :py:class:`~abaqus.Assembly.ConnectorOrientationArray.ConnectorOrientationArray` object.
    sectionAssignments: SectionAssignmentArray
        A :py:class:`~abaqus.Property.SectionAssignmentArray.SectionAssignmentArray` object.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import assembly
        mdb.models[name].rootAssembly

    """

    # An Int specifying that feature parameters have been modified but that the assembly has 
    # not been regenerated. Possible values are 0 and 1. 
    isOutOfDate: int = None

    # A Float specifying which gives an indication when the assembly was last modified. 
    timeStamp: float = None

    # An Int specifying whether the assembly is locked or not. Possible values are 0 and 1. 
    isLocked: int = None

    # A Boolean specifying whether the positioning constraints in the assembly should be 
    # regenerated together before regenerating other assembly features. The default value is 
    # ON.If the assembly has position constraint features and you modify the value of 
    # *regenerateConstraintsTogether*, Abaqus/CAE will regenerate the assembly features. 
    regenerateConstraintsTogether: Boolean = ON

    # A VertexArray object specifying all the vertices existing at the assembly level. This 
    # member does not provide access to the vertices at the instance level. 
    vertices: VertexArray = VertexArray([])

    # An EdgeArray object specifying all the edges existing at the assembly level. This member 
    # does not provide access to the edges at the instance level. 
    edges: EdgeArray = EdgeArray([])

    # A MeshElementArray object specifying all the elements existing at the assembly level. 
    # This member does not provide access to the elements at the instance level. 
    elements: MeshElementArray = MeshElementArray([])

    # A MeshNodeArray object specifying all the nodes existing at the assembly level. This 
    # member does not provide access to the nodes at the instance level. 
    nodes: MeshNodeArray = MeshNodeArray([])

    # A repository of PartInstance objects. 
    instances: dict[str, PartInstance] = dict[str, PartInstance]()

    # A repository of Datum objects specifying all Datum objects in the assembly. 
    datums: list[Datum] = list[Datum]()

    # A repository of Feature objects specifying all Feature objects in the assembly. 
    features: dict[str, Feature] = dict[str, Feature]()

    # A repository of Feature objects specifying all Feature objects in the assembly.The 
    # Feature objects in the featuresById repository are the same as the Feature objects in 
    # the features repository. However, the key to the objects in the featuresById repository 
    # is an integer specifying the *ID*, whereas the key to the objects in the features 
    # repository is a string specifying the *name*. 
    featuresById: dict[str, Feature] = dict[str, Feature]()

    # A repository of Surface objects specifying for more information, see [Region 
    # commands](https://help.3ds.com/2022/english/DSSIMULIA_Established/SIMACAEKERRefMap/simaker-m-RegPyc-sb.htm?ContextScope=all). 
    surfaces: dict[str, Surface] = dict[str, Surface]()

    # A repository of Surface objects specifying for more information, see [Region 
    # commands](https://help.3ds.com/2022/english/DSSIMULIA_Established/SIMACAEKERRefMap/simaker-m-RegPyc-sb.htm?ContextScope=all). 
    allSurfaces: dict[str, Surface] = dict[str, Surface]()

    # A repository of Surface objects specifying picked regions. 
    allInternalSurfaces: dict[str, Surface] = dict[str, Surface]()

    # A repository of Set objects. 
    sets: dict[str, Set] = dict[str, Set]()

    # A repository of Set objects specifying for more information, see [Region 
    # commands](https://help.3ds.com/2022/english/DSSIMULIA_Established/SIMACAEKERRefMap/simaker-m-RegPyc-sb.htm?ContextScope=all). 
    allSets: dict[str, Set] = dict[str, Set]()

    # A repository of Set objects specifying picked regions. 
    allInternalSets: dict[str, Set] = dict[str, Set]()

    # A repository of Skin objects specifying the skins created on the assembly. 
    skins: dict[str, Skin] = dict[str, Skin]()

    # A repository of Stringer objects specifying the stringers created on the assembly. 
    stringers: dict[str, Stringer] = dict[str, Stringer]()

    # A repository of ReferencePoint objects. 
    referencePoints: dict[str, ReferencePoint] = dict[str, ReferencePoint]()

    # A repository of ModelInstance objects. 
    modelInstances: dict[str, ModelInstance] = dict[str, ModelInstance]()

    # A PartInstance object specifying the PartInstances and A ModelInstance object specifying 
    # the ModelInstances. 
    allInstances: dict[str, typing.Union[PartInstance, ModelInstance]] = dict[str, typing.Union[PartInstance, ModelInstance]]()

    # An EngineeringFeature object. 
    engineeringFeatures: EngineeringFeature = EngineeringFeature()

    # A String specifying the name of the model to which the assembly belongs. 
    modelName: str = ''

    # A ConnectorOrientationArray object. 
    connectorOrientations: ConnectorOrientationArray = ConnectorOrientationArray()

    # A SectionAssignmentArray object. 
    sectionAssignments: SectionAssignmentArray = SectionAssignmentArray()

    @typing.overload
    def Instance(self, name: str, part: Part, autoOffset: Boolean = OFF, dependent: Boolean = OFF) -> PartInstance:
        """This method creates a PartInstance object and puts it into the instances repository.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].rootAssembly.Instance
        
        Parameters
        ----------
        name
            A String specifying the repository key. The name must be a valid Abaqus object name.
        part
            A Part object to be instanced. If the part does not exist, no PartInstance object is
            created.
        autoOffset
            A Boolean specifying whether to apply an auto offset to the new part instance that will
            offset it from existing part instances. The default value is OFF.
        dependent
            A Boolean specifying whether the part instance is dependent or independent. If
            *dependent*=OFF, the part instance is independent. The default value is OFF.

        Returns
        -------
            A PartInstance object.
        """
        pass

    @typing.overload
    def Instance(self, name: str, model: AssemblyModel, autoOffset: Boolean = OFF) -> ModelInstance:
        """This method creates a ModelInstance object and puts it into the instances repository.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].rootAssembly.Instance
        
        Parameters
        ----------
        name
            The repository key. The name must be a valid Abaqus object name.
        model
            A Model object to be instanced. If the model does not exist, no ModelInstance object is
            created.
        autoOffset
            A Boolean specifying whether to apply an auto offset to the new instance that will
            offset it from existing instances. The default value is OFF.

        Returns
        -------
            A ModelInstance object.
        """
        pass

    def Instance(self, name: str, *args, **kwargs) -> typing.Union[PartInstance, ModelInstance]:
        """This method creates a PartInstance object and puts it into the instances repository.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].rootAssembly.Instance
        
        Parameters
        ----------
        name
            A String specifying the repository key. The name must be a valid Abaqus object name.
        part
            A Part object to be instanced. If the part does not exist, no PartInstance object is
            created.
        autoOffset
            A Boolean specifying whether to apply an auto offset to the new part instance that will
            offset it from existing part instances. The default value is OFF.
        dependent
            A Boolean specifying whether the part instance is dependent or independent. If
            *dependent*=OFF, the part instance is independent. The default value is OFF.

        Returns
        -------
            A PartInstance object.
        """
        if 'part' in kwargs.keys() or (len(args) > 0 and isinstance(args[0], Part)):
            instance = PartInstance(name, *args, **kwargs)
        else:
            instance = ModelInstance(name, *args, **kwargs)
            self.modelInstances[name] = instance
        self.instances[name] = instance
        self.allInstances[name] = instance
        return instance

    def backup(self):
        """This method makes a backup copy of the features in the assembly. The backup() method is
        used in conjunction with the restore() method.
        """
        pass

    def clearGeometryCache(self):
        """This method deletes the geometry cache. Deleting the geometry cache reduces the amount
        of memory being used.
        """
        pass

    def deleteAllFeatures(self):
        """This method deletes all the features in the assembly.
        """
        pass

    def deleteFeatures(self, featureNames: tuple):
        """This method deletes specified features from the assembly.
        
        Parameters
        ----------
        featureNames
            A sequence of Strings specifying the feature names that will be deleted from the 
            assembly. 
        """
        pass

    def excludeFromSimulation(self, instances: tuple[PartInstance], exclude: str):
        """This method excludes the specified part instances from the analysis.
        
        Parameters
        ----------
        instances
            A sequence of PartInstance objects to be excluded from the analysis. 
        exclude
            A Bool specifying whether to exclude the selected instances from the analysis or include 
            them. 
        """
        pass

    def featurelistInfo(self):
        """This method prints the name and status of all the features in the feature lists.
        """
        pass

    def getMassProperties(self, regions: str = '', relativeAccuracy: SymbolicConstant = LOW, useMesh: Boolean = False,
                          specifyDensity: Boolean = False, density: str = '', specifyThickness: Boolean = False,
                          thickness: str = '', miAboutCenterOfMass: Boolean = True, miAboutPoint: tuple = ()):
        """This method returns the mass properties of the assembly, or instances or regions. Only
        beams, trusses, shells, solids, point, nonstructural mass, and rotary inertia elements
        are supported.
        
        Parameters
        ----------
        regions
            A MeshElementArray, CellArray, FaceArray, EdgeArray, or list of PartInstance objects 
            specifying the regions whose mass properties are to be queried. The whole assembly is 
            queried by default. 
        relativeAccuracy
            A SymbolicConstant specifying the relative accuracy for geometry computation. Possible 
            values are LOW, MEDIUM, and HIGH. The default value is LOW. 
        useMesh
            A Boolean specifying whether the mesh should be used in the computation if the geometry 
            is meshed. The default value is False. 
        specifyDensity
            A Boolean specifying whether a user-specified density should be used in regions with 
            density errors such as undefined material density. The default value is False. 
        density
            A double value specifying the user-specified density value to be used in regions with 
            density errors. The user-specified density should be greater than 0. 
        specifyThickness
            A Boolean specifying whether a user-specified thickness should be used in regions with 
            thickness errors such as undefined thickness. The default value is False. 
        thickness
            A double value specifying the user-specified thickness value to be used in regions with 
            thickness errors. The user-specified thickness should be greater than 0. 
        miAboutCenterOfMass
            A Boolean specifying if the moments of inertia should be evaluated about the center of 
            mass. The default value is True. 
        miAboutPoint
            A tuple of three floats specifying the coordinates of the point about which to evaluate 
            the moment of inertia. By default if the moments of inertia are not being evaluated 
            about the center of mass, they will be evaluated about the origin. 

        Returns
        -------
        properties: dict
            A Dictionary object with the following items: 
            *area*: None or a Float specifying the sum of the area of the specified faces. The area 
            is computed only for one side for shells. 
            *areaCentroid*: None or a tuple of three Floats representing the coordinates of the area 
            centroid. 
            *volume*: None or a Float specifying the volume of the specified regions. 
            *volumeCentroid*: None or a tuple of three Floats representing the coordinates of the 
            volume centroid. 
            *massFromMassPerUnitSurfaceArea*: None or a Float specifying the mass due to mass per 
            unit surface area. 
            *mass*: None or a Float specifying the mass of the specified regions. It is the total 
            mass and includes mass from quantities such as mass per unit surface area. 
            *centerOfMass*: None or a tuple of three Floats representing the coordinates of the 
            center of mass. 
            *momentOfInertia*: None or a tuple of six Floats representing the moments of inertia 
            about the center of mass or about the point specified. 
            *warnings*: A tuple of SymbolicConstants representing the problems encountered while 
            computing the mass properties. Possible SymbolicConstants are: 
            UNSUPPORTED_ENTITIES: Some unsupported entities exist in the specified regions. The mass 
            properties are computed only for beams, trusses, shells, solids, point and 
            non-structural mass elements, and rotary inertia elements. The mass properties are not 
            computed for axisymmetric elements, springs, connectors, gaskets, or any other elements. 
            MISSING_THICKNESS: For some regions, the section definitions are missing thickness 
            values. 
            ZERO_THICKNESS: For some regions, the section definitions have a zero thickness value. 
            VARIABLE_THICKNESS: The nodal thickness or field thickness specified for some regions 
            has been ignored. 
            NON_APPLICABLE_THICKNESS: For some regions, the thickness value is not applicable to the 
            corresponding sections specified on the regions. 
            MISSING_DENSITY: For some regions, the section definitions are missing material density 
            values. 
            MISSING_MATERIAL_DEFINITION: For some regions, the material definition is missing. 
            ZERO_DENSITY: For some regions, the section definitions have a zero material density 
            value. 
            UNSUPPORTED_DENSITY: For some regions, either a negative material density or a 
            temperature dependent density has been specified, or the material value is missing for 
            one or more plies in the composite section. 
            SHELL_OFFSETS: For shells, this method does not account for any offsets specified. 
            MISSING_SECTION_DEFINITION: For some regions, the section definition is missing. 
            UNSUPPORTED_SECTION_DEFINITION: The section definition provided for some regions is not 
            supported. 
            REINFORCEMENTS: This method does not account for any reinforcements specified on the 
            model. 
            SMEARED_PROPERTIES: For regions with composite section assignments, the density is 
            smeared across the thickness. The volume centroid and center of mass computations for a 
            composite shell use a lumped mass approach where the volume and mass is assumed to be 
            lumped in the plane of the shell. As a result of these approximations the volume 
            centroid, center of mass and moments of inertia may be slightly inaccurate for regions 
            with composite section assignments. 
            UNSUPPORTED_NON_STRUCTURAL_MASS_ENTITIES: This method does not account for any 
            non-structural mass on wires. 
            INCORRECT_MOMENT_OF_INERTIA: For geometry regions with non-structural mass per volume, 
            the non-structural mass is assumed to be a point mass at the centroid of the regions. 
            Thus, the moments of inertia may be inaccurate as the distribution of the non-structural 
            mass is not accounted for. Use the mesh for accurately computing the moments of inertia. 
            MISSING_BEAM_ORIENTATIONS: For some regions with beam section assignments, the beam 
            section orientations are missing. 
            UNSUPPORTED_BEAM_PROFILES: This method supports the Box, Pipe, Circular, Rectangular, 
            Hexagonal, Trapezoidal, I, L, T, Arbitrary, and Tapered beam profiles. Any other beam 
            profile is not supported. 
            TAPERED_BEAM_MI: Moment of inertia calculations for tapered beams are not accurate. 
            SUBSTRUCTURE_INCORRECT_PROPERTIES: The user assigned density and thickness is not 
            considered for substructures.
        """
        pass

    def getAngle(self, plane1: str, plane2: str, line1: str, line2: str, commonVertex: str = ''):
        """This method returns the angle between the specified entities.
        
        Parameters
        ----------
        plane1
            A Face, MeshFace, or a Datum object specifying the first plane. The Datum object must 
            represent a datum plane. The *plane1* and *line1* arguments are mutually exclusive. One 
            of them must be specified. 
        plane2
            A Face, MeshFace, or a Datum object specifying the second plane. The Datum object must 
            represent a datum plane. The *plane2* and *line2* arguments are mutually exclusive. One 
            of them must be specified. 
        line1
            An Edge, MeshEdge, or a Datum object specifying the first curve. The Datum object must 
            represent a datum axis. The *plane1* and *line1* arguments are mutually exclusive. One 
            of them must be specified. 
        line2
            An Edge, MeshEdge, or a Datum object specifying the second curve. The Datum object must 
            represent a datum axis. The *plane2* and *line2* arguments are mutually exclusive. One 
            of them must be specified. 
        commonVertex
            If the two selected Edge objects have more than one vertex in common, this ConstrainedSketchVertex object
            specifies the vertex at which to evaluate the angle. 

        Returns
        -------
            A Float specifying the angle between the specified entities. If you provide a plane as 
            an argument, Abaqus/CAE computes the angle using the normal to the plane.
        """
        pass

    def getCoordinates(self, entity: str):
        """This method returns the coordinates of a specified point.
        
        Parameters
        ----------
        entity
            A ConstrainedSketchVertex, Datum point, MeshNode, or ReferencePoint specifying the entity to query.

        Returns
        -------
            A tuple of three Floats representing the coordinates of the specified point.
        """
        pass

    def getDistance(self, entity1: str, entity2: str, printResults: Boolean = OFF):
        """Depending on the arguments provided, this method returns one of the following:
            - The distance between two points.
            - The minimum distance between a point and an edge.
            - The minimum distance between two edges.
        
        Parameters
        ----------
        entity1
            A ConstrainedSketchVertex, Datum point, MeshNode, or Edge specifying the first entity from which to
            measure. 
        entity2
            A ConstrainedSketchVertex, Datum point, MeshNode, or Edge specifying the second entity to which to
            measure. 
        printResults
            A Boolean that determines whether a verbose output is to be printed. The default is True 

        Returns
        -------
            A Float specifying the calculated distance.
        """
        pass

    def getFacesAndVerticesOfAttachmentLines(self, edges: EdgeArray):
        """Given an array of edge objects, this method returns a tuple of dictionary objects. Each
        object consists of five members including the attachment line and associated face and
        vertex objects.
        
        Parameters
        ----------
        edges
            An EdgeArray object which is a sequence of Edge objects. 

        Returns
        -------
            A tuple of dictionary objects. Each dictionary contains five items with the following 
            keys: 
            *edge*: An Edge object specifying the attachment line. 
            *startFace*: A Face object specifying the face associated with one end of the attachment 
            line. 
            *endFace*: A Face object specifying the face associated with the other end of the 
            attachment line. 
            *startVertex*: A ConstrainedSketchVertex object specifying the vertex associated with one end of the
            attachment line. This end is also associated with the startFace. 
            *endVertex*: A ConstrainedSketchVertex object specifying the vertex associated with the other end of the
            attachment line. This end is also associated with the endFace.
        """
        pass

    def getSurfaceSections(self, surface: str):
        """This method returns a list of the sections assigned to the regions encompassed by the
        specified surface.
        
        Parameters
        ----------
        surface
            A string specifying the Surface name. 

        Returns
        -------
            A tuple of strings representing the section names. If no section names are found, the 
            tuple will contain one empty string.
        """
        pass

    def importEafFile(self, filename: str, ids: tuple = ()):
        """This method imports an assembly from an EAF file into the root assembly.
        
        Parameters
        ----------
        filename
            A String specifying the path to the EAF file from which to import the assembly. 
        ids
            A sequence of Ints. Each Int in the sequence is a unique identifier of the occurrence in 
            the assembly tree or component identifier associated with the part in the EAF file. If 
            *ids* is an empty sequence, all occurrences or parts will be imported. The default value 
            is an empty sequence. 
        """
        pass

    def importParasolidFile(self, filename: str, ids: tuple = ()):
        """This method imports an assembly from the Parasolid file into the root assembly.
        
        Parameters
        ----------
        filename
            A String specifying the path to a Parasolid file from which to import the assembly. 
        ids
            A sequence of Ints. Each Int in the sequence is a unique identifier of the occurrence in 
            the assembly tree or component identifier associated with the part in the EAF file. If 
            *ids* is an empty sequence, all occurrences or parts will be imported. The default value 
            is an empty sequence. 
        """
        pass

    def importCatiaV5File(self, filename: str, ids: tuple = ()):
        """This method imports an assembly from a CATIA V5 Elysium Neutral file into the root
        assembly.
        
        Parameters
        ----------
        filename
            A String specifying the path to the CATIA V5 Elysium Neutral file from which to import 
            the assembly. 
        ids
            A sequence of Ints. Each Int in the sequence is a unique identifier of the occurrence in 
            the assembly tree or component identifier associated with the part in the EAF file. If 
            *ids* is an empty sequence, all occurrences or parts will be imported. The default value 
            is an empty sequence. 
        """
        pass

    def importEnfFile(self, filename: str, ids: tuple = ()):
        """This method imports an assembly from an Elysium Neutral file created by Pro/ENGINEER,
        I-DEAS, or CATIA V5 into the root assembly.
        
        Parameters
        ----------
        filename
            A String specifying the path to the Elysium Neutral file from which to import the 
            assembly. 
        ids
            A sequence of Ints. Each Int in the sequence is a unique identifier of the occurrence in 
            the assembly tree or component identifier associated with the part in the EAF file. If 
            *ids* is an empty sequence, all occurrences or parts will be imported. The default value 
            is an empty sequence. 
        """
        pass

    def importIdeasFile(self, filename: str, ids: tuple = ()):
        """This method imports an assembly from an I-DEAS Elysium Neutral file into the root
        assembly.
        
        Parameters
        ----------
        filename
            A String specifying the path to the I-DEAS Elysium Neutral file from which to import the 
            assembly. 
        ids
            A sequence of Ints. Each Int in the sequence is a unique identifier of the occurrence in 
            the assembly tree or component identifier associated with the part in the EAF file. If 
            *ids* is an empty sequence, all occurrences or parts will be imported. The default value 
            is an empty sequence. 
        """
        pass

    def importProEFile(self, filename: str, ids: tuple = ()):
        """This method imports an assembly from a Pro/ENGINEER Elysium Neutral file into the root
        assembly.
        
        Parameters
        ----------
        filename
            A String specifying the path to the Pro/ENGINEER Elysium Neutral file from which to 
            import the assembly. 
        ids
            A sequence of Ints. Each Int in the sequence is a unique identifier of the occurrence in 
            the assembly tree or component identifier associated with the part in the EAF file. If 
            *ids* is an empty sequence, all occurrences or parts will be imported. The default value 
            is an empty sequence. 
        """
        pass

    def makeDependent(self, instances: tuple[PartInstance]):
        """This method converts the specified part instances from independent to dependent part
        instances.
        
        Parameters
        ----------
        instances
            A sequence of PartInstance objects to convert to dependent part instances. 
        """
        pass

    def makeIndependent(self, instances: tuple[PartInstance]):
        """This method converts the specified part instances from dependent to independent part
        instances.
        
        Parameters
        ----------
        instances
            A sequence of PartInstance objects to convert to independent part instances. 
        """
        pass

    def printAssignedSections(self):
        """This method prints a summary of assigned connector sections.
        """
        pass

    def printConnectorOrientations(self):
        """This method prints a summary of connector orientations.
        """
        pass

    def projectReferencesOntoSketch(self, sketch: str, filter: SymbolicConstant = ALL_EDGES,
                                    upToFeature: Feature = Feature(),
                                    edges: tuple = (), vertices: tuple = ()):
        """This method projects the specified edges, vertices, and datum points from the assembly
        onto the specified ConstrainedSketch object. The edges, vertices, and datum points
        appear on the sketch as reference geometry.
        
        Parameters
        ----------
        sketch
            The ConstrainedSketch object on which the edges, vertices, and datum points are 
            projected. 
        filter
            A SymbolicConstant specifying how to limit the amount of projection. Possible values are 
            ALL_EDGES and COPLANAR_EDGES. If *filter*=COPLANAR_EDGES, edges that are coplanar to the 
            sketching plane are the only candidates for projection. The default value is ALL_EDGES. 
        upToFeature
            A Feature object specifying a marker in the feature-based history of the part. 
            Abaqus/CAE projects onto the sketch only the part entities that were created before the 
            feature specified by this marker. By default, all part entities are candidates for 
            projection. 
        edges
            A sequence of candidate edges to be projected onto the sketch. By default, all edges are 
            candidates for projection. 
        vertices
            A sequence of candidate vertices to be projected onto the sketch. By default, all 
            vertices are candidates for projection. 
        """
        pass

    def queryCachedStates(self):
        """This method displays the position of geometric states relative to the sequence of
        features in the assembly cache. The output is displayed in the message area.
        """
        pass

    def regenerate(self):
        """This method regenerates the assembly and brings it up to date with the latest values of
        the assembly parameters. When you modify features of an assembly, it may be convenient
        to postpone regeneration until you make all your changes, since regeneration can be time
        consuming. In contrast, when you modify features of a part that is included in the
        assembly, you should use this command to regenerate the assembly. When you regenerate
        the assembly, it will reflect the changes that you made to the part.
        """
        pass

    def regenerationWarnings(self):
        """This method prints any regeneration warnings associated with the features.
        """
        pass

    def restore(self):
        """This method restores the parameters of all features in the assembly to the value they
        had before a failed regeneration. Use the restore method after a failed regeneration,
        followed by a regenerate command.
        """
        pass

    def resumeAllFeatures(self):
        """This method resumes all the suppressed features in the part or assembly.
        """
        pass

    def resumeFeatures(self, featureNames: tuple):
        """This method resumes the specified suppressed features in the assembly.
        
        Parameters
        ----------
        featureNames
            A sequence of Strings specifying the names of features to resume. 
        """
        pass

    def resumeLastSetFeatures(self):
        """This method resumes the last set of features to be suppressed in the assembly.
        """
        pass

    def rotate(self, instanceList: tuple, axisPoint: tuple, axisDirection: tuple, angle: float):
        """This method rotates given instances by the specified amount.
        
        Parameters
        ----------
        instanceList
            A sequence of Strings specifying the names of instances to rotate. 
        axisPoint
            A sequence of three Floats specifying the coordinates of a point on the axis. 
        axisDirection
            A sequence of three Floats specifying the direction of the axis. 
        angle
            A Float specifying the rotation angle in degrees. Use the right-hand rule to determine 
            the direction. 
        """
        pass

    def translate(self, instanceList: tuple, vector: tuple):
        """This method translates given instances by the specified amount.
        
        Parameters
        ----------
        instanceList
            A sequence of Strings specifying the names of instances to translate. 
        vector
            A sequence of three Floats specifying a translation vector. 
        """
        pass

    def saveGeometryCache(self):
        """This method caches the current geometry, which improves regeneration performance.
        """
        pass

    def setValues(self, regenerateConstraintsTogether: Boolean):
        """This method modifies the behavior associated with the specified assembly.
        
        Parameters
        ----------
        regenerateConstraintsTogether
            A Boolean specifying whether the positioning constraints in the assembly should be 
            regenerated together before regenerating other assembly features. The default value is 
            ON.If the assembly has position constraint features and you modify the value of 
            *regenerateConstraintsTogether*, Abaqus/CAE will regenerate the assembly features.

        Raises
        ------
            - If one or more features in the assembly fails to regenerate: 
              FeatureError: Regeneration failed 
        """
        pass

    def suppressFeatures(self, featureNames: tuple):
        """This method suppresses specified features.
        
        Parameters
        ----------
        featureNames
            A sequence of Strings specifying the names of features to suppress in the assembly. 
        """
        pass

    def unlinkInstances(self, instances: tuple[PartInstance]):
        """This method converts the specified PartInstance objects from linked child instances to
        regular instances. The parts associated with the selected instances will be converted to
        regular parts as well.
        
        Parameters
        ----------
        instances
            A sequence of PartInstance objects to be converted to regular part instances. 
        """
        pass

    def writeAcisFile(self, fileName: str, version: float = None):
        """This method exports the assembly to a named file in ACIS part (SAT) or assembly (ASAT)
        format.
        
        Parameters
        ----------
        fileName
            A String specifying the name of the file to which to write. The file name's extension is 
            used to determine whether a part or assembly is written. Use the file extension .asat 
            for the assembly format. 
        version
            A Float specifying the ACIS version. For example, the Float 12.0 corresponds to ACIS 
            Version 12.0. The default value is the current version of ACIS. 
        """
        pass

    def writeCADParameters(self, paramFile: str, modifiedParams: tuple = (), updatePaths: str = ''):
        """This method writes the parameters that were imported from the CAD system to a parameter
        file.
        
        Parameters
        ----------
        paramFile
            A String specifying the parameter file name. 
        modifiedParams
            A tuple of tuples each containing the part name, the parameter name and the modified 
            parameter value. Default is an empty tuple. 
        updatePaths
            A Bool specifying whether to update the path of the CAD model file specified in the 
            *parameterFile* to the current directory, if the CAD model is present in the current 
            directory. 
        """
        pass

    def lock(self):
        """This method locks the assembly. Locking the assembly prevents any further changes to the
        assembly that can trigger regeneration of the assembly.
        """
        pass

    def unlock(self):
        """This method unlocks the assembly. Unlocking the assembly allows it to be regenerated
        after any modifications to the assembly.
        """
        pass

    def setMeshNumberingControl(self, instances: tuple[PartInstance], startNodeLabel: int = None,
                                startElemLabel: int = None):
        """This method changes the start node and/or element labels on the specified independent
        part instances before or after Abaqus/CAE generates the meshes. For the meshed
        instances, Abaqus/CAE changes the node and/or element labels while preserving the
        original order and incrementation.
        
        Parameters
        ----------
        instances
            A sequence of PartInstance objects to change the start node and/or element labels. 
        startNodeLabel
            A positive Integer specifying the new start node label. 
        startElemLabel
            A positive Integer specifying the new start element label. 
        """
        pass

    def copyMeshPattern(self, elements: tuple[MeshElement] = (), faces: tuple[Face] = (),
                        elemFaces: tuple[MeshFace] = (), targetFace: MeshFace = MeshFace(),
                        nodes: tuple[MeshNode] = (), coordinates: tuple = ()):
        """This method copies a mesh pattern from a source region consisting of a set of shell
        elements or element faces onto a target face, mapping nodes and elements in a one-one
        correspondence between source and target.
        
        Parameters
        ----------
        elements
            A sequence of MeshElement objects or a Set object containing elements and specifying the 
            source region. 
        faces
            A sequence of Face objects that have associated with shell elements or element faces and 
            specifying the source region. 
        elemFaces
            A sequence of MeshFace objects specifying the source region. 
        targetFace
            A MeshFace object specifying the target region. The target face can be of a different 
            part instance. 
        nodes
            A sequence of MeshNode objects or a Set object containing nodes on the boundary of 
            source region which are to be positioned to the boundary of target face. 
        coordinates
            A sequence of three-dimensional coordinate tuples specifying the coordinates for each of 
            the given nodes. When specified, the number of coordinate tuples must match the number 
            of given nodes, and be ordered to correspond to the given nodes in *ascending order* 
            according to index. These coordinates are positions of the nodes of a mesh that will be 
            the target face corresponding to nodes provided. 
        """
        pass

    def smoothNodes(self, nodes: tuple[MeshNode]):
        """This method smooths the given nodes of a native mesh, moving them locally to a more
        optimal location that improves the quality of the mesh
        
        Parameters
        ----------
        nodes
            A sequence of MeshNode objects or a Set object containing nodes. 
        """
        pass
