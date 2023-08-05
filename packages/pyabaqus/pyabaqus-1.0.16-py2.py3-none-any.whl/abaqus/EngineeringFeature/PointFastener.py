import typing

from abaqusConstants import *
from .Fastener import Fastener
from ..Region.Region import Region
from ..Region.RegionArray import RegionArray


class PointFastener(Fastener):
    """The PointFastener object defines a point fastener.
    The PointFastener object is derived from the Fastener object. 

    Attributes
    ----------
    suppressed: Boolean
        A Boolean specifying whether the fastener is suppressed or not. The default value is
        OFF.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import part
        mdb.models[name].parts[name].engineeringFeatures.fasteners[name]
        import assembly
        mdb.models[name].rootAssembly.engineeringFeatures.fasteners[name]

    The corresponding analysis keywords are:

    - FASTENER

    """

    # A Boolean specifying whether the fastener is suppressed or not. The default value is 
    # OFF. 
    suppressed: Boolean = OFF

    def __init__(self, name: str, region: Region, physicalRadius: float, directionVector: tuple = None,
                 targetSurfaces: RegionArray = MODEL, ur1: Boolean = ON, ur2: Boolean = ON,
                 ur3: Boolean = ON, attachmentMethod: SymbolicConstant = FACETOFACE,
                 influenceRadius: typing.Union[SymbolicConstant, float] = DEFAULT,
                 searchRadius: typing.Union[SymbolicConstant, float] = DEFAULT,
                 maximumLayers: SymbolicConstant = ALL, coupling: SymbolicConstant = CONTINUUM,
                 weightingMethod: SymbolicConstant = UNIFORM, additionalMass: float = 0,
                 adjustOrientation: Boolean = ON, localCsys: int = None,
                 connectionType: SymbolicConstant = CONNECTOR, sectionName: str = '',
                 connectorOrientationLocalCsys1: int = None, axis1: SymbolicConstant = AXIS_1,
                 angle1: float = 0, orient2SameAs1: Boolean = ON,
                 connectorOrientationLocalCsys2: int = None, axis2: SymbolicConstant = AXIS_1,
                 angle2: float = 0, unsorted: Boolean = OFF):
        """This method creates a PointFastener object. Although the constructor is available both
        for parts and for the assembly, PointFastener objects are currently supported only under
        the assembly.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].parts[name].engineeringFeatures.PointFastener
            mdb.models[name].rootAssembly.engineeringFeatures.PointFastener
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        region
            A Region object specifying the region to which fasteners are applied. 
        physicalRadius
            A Float specifying the physical fastener radius. 
        directionVector
            A VertexArray object of length 2 specifying the direction of projection. Instead of 
            through a ConstrainedSketchVertex, each point may be specified through a tuple of coordinates. The
            default value is None. 
        targetSurfaces
            A RegionArray object specifying surfaces to be fastened. The default value is MODEL. 
        ur1
            A Boolean specifying whether to constrain rotational displacement component about the 
            1-direction. The default value is ON. 
        ur2
            A Boolean specifying whether to constrain rotational displacement component about the 
            2-direction. The default value is ON. 
        ur3
            A Boolean specifying whether to constrain rotational displacement component about the 
            3-direction. The default value is ON. 
        attachmentMethod
            A SymbolicConstant specifying the method used to locate points for attaching fasteners. 
            Possible values are FACETOFACE, EDGETOFACE, FACETOEDGE, and EDGETOEDGE. The default 
            value is FACETOFACE. 
        influenceRadius
            The SymbolicConstant DEFAULT or a Float specifying the maximum distance from the 
            projection point on a connected surface within which the nodes on that surface must lie 
            to contribute to the motion of the projection point. If the value is DEFAULT, a radius 
            is computed from the fastener diameter and the surface facet lengths. The default value 
            is DEFAULT. 
        searchRadius
            The SymbolicConstant DEFAULT or a Float specifying the distance from the positioning 
            points within which the connected points must lie. The default value is DEFAULT. 
        maximumLayers
            The SymbolicConstant ALL or an Int specifying the maximum number of layers for each 
            fastener. If the value is ALL, the maximum possible number of layers within the 
            searchRadius will be used for each fastener. The default value is ALL. 
        coupling
            A SymbolicConstant specifying the coupling method used to couple the displacement and 
            rotation of each attachment point to the average motion of the surface nodes within the 
            radius of influence from the fastener projection point. Possible values are CONTINUUM 
            and STRUCTURAL. The default value is CONTINUUM. 
        weightingMethod
            A SymbolicConstant specifying the weighting scheme to be used to weight the contribution 
            of the displacements of the surface nodes within the radius of influence to the motion 
            of the fastener projection point. UNIFORM, LINEAR, QUADRATIC, and CUBIC indicate 
            uniform, linear decreasing, quadratic polynomial decreasing, and cubic polynomial 
            monotonic decreasing weight distributions. Possible values are UNIFORM, LINEAR, 
            QUADRATIC, and CUBIC. The default value is UNIFORM. 
        additionalMass
            A Float specifying the mass that will be distributed to fastener attachment points. The 
            default value is 0.0. 
        adjustOrientation
            A Boolean specifying whether to adjust localCsys such that the local z-axis for each 
            fastener is normal to the surface that is closest to the reference node for that 
            fastener. The default value is ON. 
        localCsys
            None or a DatumCsys object specifying the local coordinate system. If *localCsys*=None, 
            the global coordinate system is used. When this member is queried, it returns an Int. 
            The default value is None. 
        connectionType
            A SymbolicConstant specifying the fastener connection type. Possible values are 
            CONNECTOR and BEAM_MPC. The default value is CONNECTOR. 
        sectionName
            A String specifying the connector section assigned to generated connectors. The default 
            value is an empty string. 
        connectorOrientationLocalCsys1
            None or a DatumCsys object specifying the local coordinate system of the first connector 
            point in generated connectors. If *connectorOrientationLocalCsys1*=None, the degrees of 
            freedom are defined in the global coordinate system. When this member is queried, it 
            returns an Int. The default value is None. 
        axis1
            A SymbolicConstant specifying the axis of a datum coordinate system about which an 
            additional rotation is applied for the first point in generated connectors. Possible 
            values are AXIS_1, AXIS_2, and AXIS_3. The default value is AXIS_1. 
        angle1
            A Float specifying the angle of the additional rotation for the first point in generated 
            connectors. The default value is 0.0. 
        orient2SameAs1
            A Boolean specifying whether or not the second connector point in generated connectors 
            is to use the same local coordinate system, axis, and angle as the first point. The 
            default value is ON. 
        connectorOrientationLocalCsys2
            None or a DatumCsys object specifying the local coordinate system of the second 
            connector point in generated connectors. If *connectorOrientationLocalCsys2*=None, the 
            degrees of freedom are defined in the global coordinate system. When this member is 
            queried, it returns an Int. The default value is None. 
        axis2
            A SymbolicConstant specifying the axis of a datum coordinate system about which an 
            additional rotation is applied for the second point in generated connectors. Possible 
            values are AXIS_1, AXIS_2, and AXIS_3. The default value is AXIS_1. 
        angle2
            A Float specifying the angle of the additional rotation for the second point in 
            generated connectors. The default value is 0.0. 
        unsorted
            A Boolean specifying whether the analysis product should leave targetSurfaces in the 
            given unsorted order, or sort them by proximity to determine the connectivity of 
            fastening points. The default value is OFF. 

        Returns
        -------
            A PointFastener object.
        """
        super().__init__()
        pass

    def setValues(self, directionVector: tuple = None, targetSurfaces: RegionArray = MODEL, ur1: Boolean = ON,
                  ur2: Boolean = ON, ur3: Boolean = ON, attachmentMethod: SymbolicConstant = FACETOFACE,
                  influenceRadius: typing.Union[SymbolicConstant, float] = DEFAULT,
                  searchRadius: typing.Union[SymbolicConstant, float] = DEFAULT,
                  maximumLayers: SymbolicConstant = ALL, coupling: SymbolicConstant = CONTINUUM,
                  weightingMethod: SymbolicConstant = UNIFORM, additionalMass: float = 0,
                  adjustOrientation: Boolean = ON, localCsys: int = None,
                  connectionType: SymbolicConstant = CONNECTOR, sectionName: str = '',
                  connectorOrientationLocalCsys1: int = None, axis1: SymbolicConstant = AXIS_1,
                  angle1: float = 0, orient2SameAs1: Boolean = ON,
                  connectorOrientationLocalCsys2: int = None, axis2: SymbolicConstant = AXIS_1,
                  angle2: float = 0, unsorted: Boolean = OFF):
        """This method modifies the PointFastener object.
        
        Parameters
        ----------
        directionVector
            A VertexArray object of length 2 specifying the direction of projection. Instead of 
            through a ConstrainedSketchVertex, each point may be specified through a tuple of coordinates. The
            default value is None. 
        targetSurfaces
            A RegionArray object specifying surfaces to be fastened. The default value is MODEL. 
        ur1
            A Boolean specifying whether to constrain rotational displacement component about the 
            1-direction. The default value is ON. 
        ur2
            A Boolean specifying whether to constrain rotational displacement component about the 
            2-direction. The default value is ON. 
        ur3
            A Boolean specifying whether to constrain rotational displacement component about the 
            3-direction. The default value is ON. 
        attachmentMethod
            A SymbolicConstant specifying the method used to locate points for attaching fasteners. 
            Possible values are FACETOFACE, EDGETOFACE, FACETOEDGE, and EDGETOEDGE. The default 
            value is FACETOFACE. 
        influenceRadius
            The SymbolicConstant DEFAULT or a Float specifying the maximum distance from the 
            projection point on a connected surface within which the nodes on that surface must lie 
            to contribute to the motion of the projection point. If the value is DEFAULT, a radius 
            is computed from the fastener diameter and the surface facet lengths. The default value 
            is DEFAULT. 
        searchRadius
            The SymbolicConstant DEFAULT or a Float specifying the distance from the positioning 
            points within which the connected points must lie. The default value is DEFAULT. 
        maximumLayers
            The SymbolicConstant ALL or an Int specifying the maximum number of layers for each 
            fastener. If the value is ALL, the maximum possible number of layers within the 
            searchRadius will be used for each fastener. The default value is ALL. 
        coupling
            A SymbolicConstant specifying the coupling method used to couple the displacement and 
            rotation of each attachment point to the average motion of the surface nodes within the 
            radius of influence from the fastener projection point. Possible values are CONTINUUM 
            and STRUCTURAL. The default value is CONTINUUM. 
        weightingMethod
            A SymbolicConstant specifying the weighting scheme to be used to weight the contribution 
            of the displacements of the surface nodes within the radius of influence to the motion 
            of the fastener projection point. UNIFORM, LINEAR, QUADRATIC, and CUBIC indicate 
            uniform, linear decreasing, quadratic polynomial decreasing, and cubic polynomial 
            monotonic decreasing weight distributions. Possible values are UNIFORM, LINEAR, 
            QUADRATIC, and CUBIC. The default value is UNIFORM. 
        additionalMass
            A Float specifying the mass that will be distributed to fastener attachment points. The 
            default value is 0.0. 
        adjustOrientation
            A Boolean specifying whether to adjust localCsys such that the local z-axis for each 
            fastener is normal to the surface that is closest to the reference node for that 
            fastener. The default value is ON. 
        localCsys
            None or a DatumCsys object specifying the local coordinate system. If *localCsys*=None, 
            the global coordinate system is used. When this member is queried, it returns an Int. 
            The default value is None. 
        connectionType
            A SymbolicConstant specifying the fastener connection type. Possible values are 
            CONNECTOR and BEAM_MPC. The default value is CONNECTOR. 
        sectionName
            A String specifying the connector section assigned to generated connectors. The default 
            value is an empty string. 
        connectorOrientationLocalCsys1
            None or a DatumCsys object specifying the local coordinate system of the first connector 
            point in generated connectors. If *connectorOrientationLocalCsys1*=None, the degrees of 
            freedom are defined in the global coordinate system. When this member is queried, it 
            returns an Int. The default value is None. 
        axis1
            A SymbolicConstant specifying the axis of a datum coordinate system about which an 
            additional rotation is applied for the first point in generated connectors. Possible 
            values are AXIS_1, AXIS_2, and AXIS_3. The default value is AXIS_1. 
        angle1
            A Float specifying the angle of the additional rotation for the first point in generated 
            connectors. The default value is 0.0. 
        orient2SameAs1
            A Boolean specifying whether or not the second connector point in generated connectors 
            is to use the same local coordinate system, axis, and angle as the first point. The 
            default value is ON. 
        connectorOrientationLocalCsys2
            None or a DatumCsys object specifying the local coordinate system of the second 
            connector point in generated connectors. If *connectorOrientationLocalCsys2*=None, the 
            degrees of freedom are defined in the global coordinate system. When this member is 
            queried, it returns an Int. The default value is None. 
        axis2
            A SymbolicConstant specifying the axis of a datum coordinate system about which an 
            additional rotation is applied for the second point in generated connectors. Possible 
            values are AXIS_1, AXIS_2, and AXIS_3. The default value is AXIS_1. 
        angle2
            A Float specifying the angle of the additional rotation for the second point in 
            generated connectors. The default value is 0.0. 
        unsorted
            A Boolean specifying whether the analysis product should leave targetSurfaces in the 
            given unsorted order, or sort them by proximity to determine the connectivity of 
            fastening points. The default value is OFF. 
        """
        pass
