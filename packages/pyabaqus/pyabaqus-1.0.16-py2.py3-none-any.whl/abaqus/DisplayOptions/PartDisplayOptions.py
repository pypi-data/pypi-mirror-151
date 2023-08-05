from abaqusConstants import *
from .EngineeringFeatureDisplayOptions import EngineeringFeatureDisplayOptions
from .GeometryDisplayOptions import GeometryDisplayOptions
from .MeshDisplayOptions import MeshDisplayOptions
from ..DisplayGroup.DisplayGroup import DisplayGroup
from ..DisplayGroup.DisplayGroupInstance import DisplayGroupInstance
from ..DisplayGroup.Leaf import Leaf


class PartDisplayOptions:
    """The PartDisplayOptions object stores settings that specify how parts are to be displayed
    in a particular viewport. The PartDisplayOptions object has no constructor. When you 
    create a new viewport, the settings are copied from the current viewport. 

    Attributes
    ----------
    engineeringFeatures: Boolean
        A Boolean specifying whether engineering features are shown. The default value is OFF.
    renderBeamProfiles: Boolean
        A Boolean specifying whether to render the beam profiles. The default value is OFF.
    beamScaleFactor: float
        A Float specifying the beam profile scale factor. The beamScaleFactor must be greater
        than zero. The default value is 1.0.
    mesh: Boolean
        A Boolean specifying whether the mesh should be displayed.
    renderStyle: SymbolicConstant
        A SymbolicConstant specifying how the image in the viewport is rendered. Possible values
        are WIREFRAME, HIDDEN, and SHADED. The default value is WIREFRAME.
    displayGroup: DisplayGroup
        A :py:class:`~abaqus.DisplayGroup.DisplayGroup.DisplayGroup` object specifying the current display group :py:class:`~.an`d referring to :py:class:`~.an` object in
        the **displayGroups** member of Session.
    displayGroupInstances: dict[str, DisplayGroupInstance]
        A repository of :py:class:`~abaqus.DisplayGroup.DisplayGroupInstance.DisplayGroupInstance` objects.
    engineeringFeatureOptions: EngineeringFeatureDisplayOptions
        An :py:class:`~abaqus.DisplayOptions.EngineeringFeatureDisplayOptions.EngineeringFeatureDisplayOptions` object.
    geometryOptions: GeometryDisplayOptions
        A :py:class:`~abaqus.DisplayOptions.GeometryDisplayOptions.GeometryDisplayOptions` object.
    meshOptions: MeshDisplayOptions
        A :py:class:`~abaqus.DisplayOptions.MeshDisplayOptions.MeshDisplayOptions` object.

    Notes
    -----
    This object can be accessed by:

    .. code-block::
    
        session.viewports[name].layers[name].partDisplay
        import part
        session.viewports[name].partDisplay

    """

    # A Boolean specifying whether engineering features are shown. The default value is OFF. 
    engineeringFeatures: Boolean = OFF

    # A Boolean specifying whether to render the beam profiles. The default value is OFF. 
    renderBeamProfiles: Boolean = OFF

    # A Float specifying the beam profile scale factor. The beamScaleFactor must be greater 
    # than zero. The default value is 1.0. 
    beamScaleFactor: float = 1

    # A Boolean specifying whether the mesh should be displayed. 
    mesh: Boolean = OFF

    # A SymbolicConstant specifying how the image in the viewport is rendered. Possible values 
    # are WIREFRAME, HIDDEN, and SHADED. The default value is WIREFRAME. 
    renderStyle: SymbolicConstant = WIREFRAME

    # A DisplayGroup object specifying the current display group and referring to an object in 
    # the *displayGroups* member of Session. 
    displayGroup: DisplayGroup = DisplayGroup('dg', Leaf(EMPTY_LEAF))

    # A repository of DisplayGroupInstance objects. 
    displayGroupInstances: dict[str, DisplayGroupInstance] = dict[str, DisplayGroupInstance]()

    # An EngineeringFeatureDisplayOptions object. 
    engineeringFeatureOptions: EngineeringFeatureDisplayOptions = EngineeringFeatureDisplayOptions()

    # A GeometryDisplayOptions object. 
    geometryOptions: GeometryDisplayOptions = GeometryDisplayOptions()

    # A MeshDisplayOptions object. 
    meshOptions: MeshDisplayOptions = MeshDisplayOptions()

    def setValues(self, renderStyle: SymbolicConstant = WIREFRAME,
                  visibleDisplayGroups: tuple[DisplayGroup] = (), engineeringFeatures: Boolean = OFF,
                  renderBeamProfiles: Boolean = OFF, beamScaleFactor: float = 1):
        """This method modifies the PartDisplayOptions object.
        
        Parameters
        ----------
        renderStyle
            A SymbolicConstant specifying how the image in the viewport is rendered. Possible values 
            are WIREFRAME, HIDDEN, and SHADED. The default value is WIREFRAME. 
        visibleDisplayGroups
            A sequence of DisplayGroup objects specifying the DisplayGroups visible in the viewport. 
            Currently the sequence can contain a maximum of one DisplayGroup object. The default 
            value is an empty sequence. 
        engineeringFeatures
            A Boolean specifying whether engineering features are shown. The default value is OFF. 
        renderBeamProfiles
            A Boolean specifying whether to render the beam profiles. The default value is OFF. 
        beamScaleFactor
            A Float specifying the beam profile scale factor. The beamScaleFactor must be greater 
            than zero. The default value is 1.0.

        Raises
        ------
        RangeError
        """
        pass
