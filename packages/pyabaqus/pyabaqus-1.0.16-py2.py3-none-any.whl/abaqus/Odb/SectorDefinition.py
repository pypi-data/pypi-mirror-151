class SectorDefinition:
    """The SectorDefinition object describes the number of symmetry sectors and axis of
    symmetry for a cyclic symmetry model. 

    Attributes
    ----------
    numSectors: int
        An Int specifying the number of sectors in the cyclic symmetry model.
    symmetryAxis: float
        A tuple of tuples of Floats specifying the coordinates of two points on the axis of
        symmetry.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import odbAccess
        session.odbs[name].sectorDefinition

    """

    # An Int specifying the number of sectors in the cyclic symmetry model. 
    numSectors: int = None

    # A tuple of tuples of Floats specifying the coordinates of two points on the axis of 
    # symmetry. 
    symmetryAxis: float = None
