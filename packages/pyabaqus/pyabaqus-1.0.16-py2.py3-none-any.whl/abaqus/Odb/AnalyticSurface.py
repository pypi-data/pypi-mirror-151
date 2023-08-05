from abaqusConstants import *
from .OdbSequenceAnalyticSurfaceSegment import OdbSequenceAnalyticSurfaceSegment


class AnalyticSurface:
    """The AnalyticSurface object is a geometric surface that can be described with straight
    and/or curved line segments. 

    Attributes
    ----------
    name: str
        A String specifying the name of the analytic surface.
    type: SymbolicConstant
        A SymbolicConstant specifying the type of :py:class:`~abaqus.Odb.AnalyticSurface.AnalyticSurface` object. Possible values are
        SEGMENTS, CYLINDER, and REVOLUTION.
    filletRadius: float
        A Float specifying radius of curvature to smooth discontinuities between adjoining
        segments. The default value is 0.0.
    segments: OdbSequenceAnalyticSurfaceSegment
        An :py:class:`~abaqus.Odb.OdbSequenceAnalyticSurfaceSegment.OdbSequenceAnalyticSurfaceSegment` object specifying the profile associated with the
        surface.
    localCoordData: float
        A tuple of tuples of Floats specifying the global coordinates of points representing the
        local coordinate system, if used.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import odbAccess
        session.odbs[name].parts[name].analyticSurface
        session.odbs[name].rootAssembly.instances[name].analyticSurface
        session.odbs[name].steps[name].frames[i].fieldOutputs[name].values[i].instance.analyticSurface

    """

    # A String specifying the name of the analytic surface. 
    name: str = ''

    # A SymbolicConstant specifying the type of AnalyticSurface object. Possible values are 
    # SEGMENTS, CYLINDER, and REVOLUTION. 
    type: SymbolicConstant = None

    # A Float specifying radius of curvature to smooth discontinuities between adjoining 
    # segments. The default value is 0.0. 
    filletRadius: float = 0

    # An OdbSequenceAnalyticSurfaceSegment object specifying the profile associated with the 
    # surface. 
    segments: OdbSequenceAnalyticSurfaceSegment = OdbSequenceAnalyticSurfaceSegment()

    # A tuple of tuples of Floats specifying the global coordinates of points representing the 
    # local coordinate system, if used. 
    localCoordData: float = None
