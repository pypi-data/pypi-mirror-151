from abaqusConstants import *


class ConstrainedSketchGeometry:
    """The ConstrainedSketchGeometry object stores the geometry of a sketch, such as lines,
    circles, arcs, and construction lines. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import sketch
        mdb.models[name].sketches[name].geometry[i]
        mdb.models[name].sketches[name].geometry[i][i]

    """

    # An Int specifying the index of the sketch entity in the ConstrainedSketchGeometryArray. 
    id: int = None

    # A SymbolicConstant specifying the geometry of the sketch entity. Possible values are 
    # ARC, CIRCLE, ELLIPSE, LINE, and SPLINE. 
    curveType: SymbolicConstant = None

    # A SymbolicConstant specifying the type of sketch entity. Possible values are REGULAR, 
    # REFERENCE, and CONSTRUCTION. 
    type: SymbolicConstant = None

    # A tuple of Floats specifying the *X*- and*Y*-coordinates of a point located on the 
    # geometry. 
    pointOn: float = None
