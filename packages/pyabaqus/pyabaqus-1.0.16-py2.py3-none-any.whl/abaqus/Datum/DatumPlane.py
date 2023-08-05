from .Datum import Datum


class DatumPlane(Datum):
    """The DatumPlane object has no direct constructor; it is created when a Feature object is
    created. For example, the DatumPlaneByPrincipalPlane method creates a Feature object 
    that creates a DatumPlane object. 
    The DatumPlane object is derived from the Datum object. 

    Attributes
    ----------
    pointOn: float
        A tuple of Floats specifying the **X**-, **Y**-, and **Z**-coordinates of a point located on
        the datum.
    normal: tuple
        A tuple of Floats specifying a sequence of three Floats specifying the normal.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import part
        mdb.models[name].parts[name].datums[i]
        import assembly
        mdb.models[name].rootAssembly.allInstances[name].datums[i]
        mdb.models[name].rootAssembly.datums[i]
        mdb.models[name].rootAssembly.instances[name].datums[i]

    """

    # A tuple of Floats specifying the *X*-, *Y*-, and *Z*-coordinates of a point located on 
    # the datum. 
    pointOn: float = None

    # A tuple of Floats specifying a sequence of three Floats specifying the normal. 
    normal: tuple = ()
