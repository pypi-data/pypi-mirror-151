class MdbDataInstance:
    """The MdbDataInstance object instance data. It corresponds to same named part instance
    with a mesh in the cae model. 

    Attributes
    ----------
    name: str
        A String specifying the instance name. This attribute is read-only.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.mdbData[name].instances[i]

    """

    # A String specifying the instance name. This attribute is read-only. 
    name: str = ''
