

class GapHeatGeneration:
    """The GapHeatGeneration object specifies heat generation for a contact interaction
    property. 

    Attributes
    ----------
    conversionFraction: float
        A Float specifying the fraction of dissipated energy caused by friction or electric
        currents that is converted to heat. The default value is 1.0.
    secondaryFraction: float
        A Float specifying the fraction of converted heat distributed to the secondary surface.
        The default value is 0.5.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import interaction
        mdb.models[name].interactionProperties[name].heatGeneration

    The corresponding analysis keywords are:

    - GAP HEAT GENERATION

    """

    # A Float specifying the fraction of dissipated energy caused by friction or electric 
    # currents that is converted to heat. The default value is 1.0. 
    conversionFraction: float = 1

    # A Float specifying the fraction of converted heat distributed to the secondary surface. 
    # The default value is 0.5. 
    secondaryFraction: float = 0

    def __init__(self, conversionFraction: float = 1, secondaryFraction: float = 0):
        """This method creates a GapHeatGeneration object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].interactionProperties[name].HeatGeneration
        
        Parameters
        ----------
        conversionFraction
            A Float specifying the fraction of dissipated energy caused by friction or electric 
            currents that is converted to heat. The default value is 1.0. 
        secondaryFraction
            A Float specifying the fraction of converted heat distributed to the secondary surface. 
            The default value is 0.5. 

        Returns
        -------
            A GapHeatGeneration object.
        """
        pass

    def setValues(self):
        """This method modifies the GapHeatGeneration object.
        """
        pass
