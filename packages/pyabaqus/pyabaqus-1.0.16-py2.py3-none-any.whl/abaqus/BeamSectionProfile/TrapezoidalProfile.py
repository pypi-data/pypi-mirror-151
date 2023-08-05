from .Profile import Profile

class TrapezoidalProfile(Profile):

    """The TrapezoidalProfile object defines the properties of a trapezoidal profile. 
    The TrapezoidalProfile object is derived from the Profile object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import section
        mdb.models[name].profiles[name]
        import odbSection
        session.odbs[name].profiles[name]

    The corresponding analysis keywords are:

    - BEAM SECTION

    """

    def __init__(self, name: str, a: float, b: float, c: float, d: float):
        """This method creates a TrapezoidalProfile object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].TrapezoidalProfile
            session.odbs[name].TrapezoidalProfile
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        a
            A positive Float specifying the *a* dimension of the Trapezoidal profile. For more 
            information, see [Beam cross-section 
            library](https://help.3ds.com/2021/English/DSSIMULIA_Established/SIMACAEELMRefMap/simaelm-c-beamcrosssectlib.htm?ContextScope=all). 
        b
            A positive Float specifying the *b* dimension of the Trapezoidal profile. 
        c
            A positive Float specifying the *c* dimension of the Trapezoidal profile. 
        d
            A Float specifying the *d* dimension of the Trapezoidal profile. 

        Returns
        -------
            A TrapezoidalProfile object. 

        Raises
        ------
        RangeError
            
        """
        super().__init__()
        pass

    def setValues(self):
        """This method modifies the TrapezoidalProfile object.

        Raises
        ------
        RangeError
            
        """
        pass

