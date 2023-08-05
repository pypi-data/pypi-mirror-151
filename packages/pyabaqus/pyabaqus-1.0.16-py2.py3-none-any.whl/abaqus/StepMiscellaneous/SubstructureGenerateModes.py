class SubstructureGenerateModes:
    """A SubstructureGenerateModes object is used to define the modes to be used in a modal
    dynamic analysis. 

    Attributes
    ----------
    start: int
        An Int specifying the mode number of the lowest mode of a range.
    end: int
        An Int specifying the mode number of the highest mode of a range.
    increment: int
        An Int specifying the increment used to define the intermediate mode numbers beginning
        from the lowest mode to the highest mode.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
    
        import step
        mdb.models[name].steps[name].modeRange[i]

    """

    # An Int specifying the mode number of the lowest mode of a range. 
    start: int = None

    # An Int specifying the mode number of the highest mode of a range. 
    end: int = None

    # An Int specifying the increment used to define the intermediate mode numbers beginning 
    # from the lowest mode to the highest mode. 
    increment: int = None
