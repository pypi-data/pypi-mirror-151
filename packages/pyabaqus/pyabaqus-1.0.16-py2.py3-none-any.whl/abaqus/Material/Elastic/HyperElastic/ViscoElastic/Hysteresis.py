
class Hysteresis:
    """The Hysteresis object specifies the creep part of the material model for the hysteretic
    behavior of elastomers. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].hyperelastic.hysteresis
        import odbMaterial
        session.odbs[name].materials[name].hyperelastic.hysteresis

    The table data for this object are:

    - Stress scaling factor.
    - Creep parameter.
    - Effective stress exponent.
    - Creep strain exponent.

    The corresponding analysis keywords are:

    - HYSTERESIS

    """

    def __init__(self, table: tuple):
        """This method creates a Hysteresis object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].hyperelastic.Hysteresis
                session.odbs[name].materials[name].hyperelastic.Hysteresis
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 

        Returns
        -------
            A Hysteresis object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the Hysteresis object.

        Raises
        ------
        RangeError
        """
        pass
