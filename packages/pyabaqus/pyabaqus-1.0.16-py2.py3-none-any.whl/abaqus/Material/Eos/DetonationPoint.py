class DetonationPoint:
    """A DetonationPoint object specifies a suboption of the Eos object. The DetonationPoint
    object defines either isotropic linear elastic shear or linear viscous shear behavior 
    for a hydrodynamic material. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].eos.detonationPoint
        import odbMaterial
        session.odbs[name].materials[name].eos.detonationPoint

    The table data for this object are:
        - X value for coordinate of detonation point.
        - Y value for coordinate of detonation point.
        - Z value for coordinate of detonation point.
        - Detonation delay time.

    The corresponding analysis keywords are:

    - DETONATION POINT

    """

    def __init__(self, table: tuple):
        """This method creates a DetonationPoint object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].eos.DetonationPoint
                session.odbs[name].materials[name].eos.DetonationPoint
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 

        Returns
        -------
            A DetonationPoint object.
        """
        pass

    def setValues(self):
        """This method modifies the DetonationPoint object.
        """
        pass
