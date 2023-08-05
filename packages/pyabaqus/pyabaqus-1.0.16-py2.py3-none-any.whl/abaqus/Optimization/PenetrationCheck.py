from abaqusConstants import *
from .GeometricRestriction import GeometricRestriction
from ..Region.Region import Region


class PenetrationCheck(GeometricRestriction):
    """The PenetrationCheck object defines a penetration check geometric restriction.
    The PenetrationCheck object is derived from the GeometricRestriction object. 
    This page discusses: 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import optimization
        mdb.models[name].optimizationTasks[name].geometricRestrictions[name]

    """

    def __init__(self, name: str, penetrationCheckRegion: Region, region: Region,
                 presumeFeasibleRegionAtStart: Boolean = ON):
        """This method creates a PenetrationCheck object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

                      mdb.models[name].optimizationTasks[name].PenetrationCheck
        
        Parameters
        ----------
        name
            A String specifying the geometric restriction repository key. 
        penetrationCheckRegion
            A Region object specifying the penetration check region. 
        region
            A Region object specifying the region to which the geometric restriction is applied. 
            When used with a TopologyTask, there is no default value. When used with a ShapeTask, 
            the default value is MODEL. 
        presumeFeasibleRegionAtStart
            A Boolean specifying whether to ignore the geometric restriction in the first design 
            cycle. The default value is ON. 

        Returns
        -------
            A PenetrationCheck object.
        """
        super().__init__()
        pass

    def setValues(self, presumeFeasibleRegionAtStart: Boolean = ON):
        """This method modifies the PenetrationCheck object.
        
        Parameters
        ----------
        presumeFeasibleRegionAtStart
            A Boolean specifying whether to ignore the geometric restriction in the first design 
            cycle. The default value is ON. 
        """
        pass
