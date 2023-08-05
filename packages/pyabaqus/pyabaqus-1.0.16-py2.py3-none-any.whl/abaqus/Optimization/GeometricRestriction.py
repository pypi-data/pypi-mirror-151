from ..Region.Region import Region


class GeometricRestriction:
    """The GeometricRestriction object is the abstract base type for other GeometricRestriction
    objects. The GeometricRestriction object has no explicit constructor. The methods and 
    members of the GeometricRestriction object are common to all objects derived from 
    GeometricRestriction. 

    Attributes
    ----------
    name: str
        A String specifying the geometric restriction repository key.
    region: Region
        A :py:class:`~abaqus.Region.Region.Region` object specifying the region to which the geometric restriction is applied.
        When used with a TopologyTask, there is no default value. When used with a ShapeTask,
        the default value is MODEL.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import optimization
        mdb.models[name].optimizationTasks[name].geometricRestrictions[name]

    """

    # A String specifying the geometric restriction repository key. 
    name: str = ''

    # A Region object specifying the region to which the geometric restriction is applied. 
    # When used with a TopologyTask, there is no default value. When used with a ShapeTask, 
    # the default value is MODEL. 
    region: Region = Region()
