from abaqusConstants import *


class OdbDataDatumCsys:
    """The OdbDataDatumCsys object stores coordinate system data.

    Attributes
    ----------
    name: str
        A String specifying the coordinate system name. This String is read-only.
    type: SymbolicConstant
        A SymbolicConstant specifying the coordinate system type. This String is read-only.
        Possible values are CARTESIAN, CYLINDRICAL, and SPHERICAL.
    xAxis: tuple
        A tuple of three Floats specifying a sequence of three floats specifying the x-Axis
        vector. The default value is (1, 0, 0).
    yAxis: tuple
        A tuple of three Floats specifying a sequence of three floats specifying the y-Axis
        vector. The default value is (0, 1, 0).
    zAxis: tuple
        A tuple of three Floats specifying a sequence of three floats specifying the z-Axis
        vector. The default value is (0, 0, 1).
    origin: tuple
        A tuple of three Floats specifying a sequence of three floats specifying the origin. The
        default value is (0, 0, 0).

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.odbData[name].datumCsyses[i]

    """

    # A String specifying the coordinate system name. This String is read-only. 
    name: str = ''

    # A SymbolicConstant specifying the coordinate system type. This String is read-only. 
    # Possible values are CARTESIAN, CYLINDRICAL, and SPHERICAL. 
    type: SymbolicConstant = None

    # A tuple of three Floats specifying a sequence of three floats specifying the x-Axis 
    # vector. The default value is (1, 0, 0). 
    xAxis: tuple = ()

    # A tuple of three Floats specifying a sequence of three floats specifying the y-Axis 
    # vector. The default value is (0, 1, 0). 
    yAxis: tuple = ()

    # A tuple of three Floats specifying a sequence of three floats specifying the z-Axis 
    # vector. The default value is (0, 0, 1). 
    zAxis: tuple = ()

    # A tuple of three Floats specifying a sequence of three floats specifying the origin. The 
    # default value is (0, 0, 0). 
    origin: tuple = ()
