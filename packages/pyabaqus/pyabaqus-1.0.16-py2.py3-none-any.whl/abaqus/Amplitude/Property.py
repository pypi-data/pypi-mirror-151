from abaqusConstants import *
from ..Datum.Datum import Datum
from ..Region.Region import Region

"""The Property assignment commands are used to assign and unassign properties to parts. 
The part and section modules must be imported to give access to the Property assignment 
commands. 

Notes
-----
        import part
        import section

"""


def assignBeamSectionOrientatio(region: tuple, method: SymbolicConstant, n1: tuple):
    """This method assigns a beam section orientation to a region of a part.

    Notes
    -----
        This function can be accessed by:
        
        .. code-block:: python
        
            mdb.models[name].parts[*name*].assignBeamSectionOrientation

    Parameters
    ----------
    region
        A sequence of geomSequences of Edge objects or a sequence of sequences of 
        one-dimensional elements. 
    method
        A SymbolicConstant specifying the assignment method. Only a value of N1_COSINES is 
        currently supported. 
    n1
        A sequence of three Floats specifying the approximate local n1n1-direction of the beam 
        cross-section. 

    """
    pass


def assignMaterialOrientatio(region: tuple, localCsys: Datum, axis: SymbolicConstant = AXIS_1, angle: float = 0):
    """This method assigns a material orientation to a region.

    Notes
    -----
        This function can be accessed by:
        
        .. code-block:: python
        
            mdb.models[name].parts[*name*].assignMaterialOrientation

    Parameters
    ----------
    region
        A sequence of geomSequences of ConstrainedSketchVertex, Edge, Face, and Cell objects or a sequence of
        sequences of elements. 
    localCsys
        A Datum object specifying the local coordinate system or None, indicating the global 
        coordinate system. 
    axis
        A SymbolicConstant specifying the axis of a cylindrical or spherical datum coordinate 
        system about which an additional rotation is applied. For shells this axis is also the 
        shell normal. Possible values are AXIS_1, AXIS_2, and AXIS_3. The default value is 
        AXIS_1. 
    angle
        A Float specifying the angle of the additional rotation. The default value is 0.0. 

    """
    pass


def assignRebarOrientatio(region: tuple, localCsys: Datum, axis: SymbolicConstant = AXIS_1, angle: float = 0):
    """This method assigns a rebar reference orientation to a region.

    Notes
    -----
        This function can be accessed by:
        
        .. code-block:: python
        
            mdb.models[name].parts[*name*].assignRebarOrientation

    Parameters
    ----------
    region
        A sequence of geomSequences of ConstrainedSketchVertex, Edge, Face, and Cell objects or a sequence of
        sequences of elements. 
    localCsys
        A Datum object specifying the local coordinate system or None, indicating the global 
        coordinate system. 
    axis
        A SymbolicConstant specifying the axis of a cylindrical or spherical datum coordinate 
        system about which an additional rotation is applied. For shells this axis is also the 
        shell normal. Possible values are AXIS_1, AXIS_2, and AXIS_3. The default value is 
        AXIS_1. 
    angle
        A Float specifying the angle of the additional rotation. The default value is 0.0. 

    """
    pass


def flipNorma(regions: Region, referenceRegion: str = ''):
    """This method flips the normals of shell or membrane elements of an orphan mesh or of
    two-dimensional geometric regions.

    Notes
    -----
        This function can be accessed by:
        
        .. code-block:: python
        
            mdb.models[name].parts[*name*].flipNormal

    Parameters
    ----------
    regions
        A Region object specifying the region on which normals are flipped. For 3D parts, the 
        region contains Face objects or two-dimensional triangle or quadrilateral Element 
        objects. For axisymmetric parts, the region contains Edge objects or line Elements 
        objects. 
    referenceRegion
        A two-dimensional element object whose normal is to be matched. If unspecified, all the 
        normals associated with the given regions will be flipped. The *referenceRegion* 
        argument is applicable only if the argument regions contain a sequence of quadrilateral 
        or triangular elements. 

    """
    pass


def flipTangen(regions: Region):
    """This method flips the tangents of beam or truss elements of an orphan mesh or of
    one-dimensional geometric regions.

    Notes
    -----
        This function can be accessed by:
        
        .. code-block:: python
        
            mdb.models[name].parts[*name*].flipTangent

    Parameters
    ----------
    regions
        A Region object specifying the region on which normals are flipped. The region contains 
        Edge objects or one-dimensional Element objects. 

    """
    pass


def unassignBeamSectionOrientatio(index: int):
    """This method deletes a beam section orientation assignment.

    Notes
    -----
        This function can be accessed by:
        
        .. code-block:: python
        
            mdb.models[name].parts[*name*].unassignBeamSectionOrientation

    Parameters
    ----------
    index
        An Int specifying the number of the beam section orientation assignment to be deleted. 

    """
    pass


def unassignMaterialOrientatio(index: int):
    """This method deletes a material orientation assignment.

    Notes
    -----
        This function can be accessed by:
        
        .. code-block:: python
        
            mdb.models[name].parts[*name*].unassignMaterialOrientation

    Parameters
    ----------
    index
        An Int specifying the number of the material assignment to be deleted. 

    """
    pass


def unassignRebarOrientatio(index: int):
    """This method deletes a rebar orientation assignment.

    Notes
    -----
        This function can be accessed by:
        
        .. code-block:: python
        
            mdb.models[name].parts[*name*].unassignRebarOrientation

    Parameters
    ----------
    index
        An Int specifying the number of the rebar reference orientation assignment to be 
        deleted. 

    """
    pass
