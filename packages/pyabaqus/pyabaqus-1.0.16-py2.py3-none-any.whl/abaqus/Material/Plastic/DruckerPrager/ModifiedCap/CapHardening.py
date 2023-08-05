from abaqusConstants import *


class CapHardening:
    """The CapHardening object specifies Drucker-Prager/Cap plasticity hardening.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].capPlasticity.capHardening
        import odbMaterial
        session.odbs[name].materials[name].capPlasticity.capHardening

    The table data for this object are:

    - Hydrostatic pressure yield stress.
    - Absolute value of the corresponding volumetric inelastic strain.
    - Temperature, if the data depend on temperature.
    - Value of the first field variable, if the data depend on field variables.
    - Value of the second field variable.
    - Etc.

    The corresponding analysis keywords are:

    - CAP HARDENING

    """

    def __init__(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0):
        """This method creates a CapHardening object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].capPlasticity.CapHardening
                session.odbs[name].materials[name].capPlasticity.CapHardening
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A CapHardening object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the CapHardening object.

        Raises
        ------
        RangeError
        """
        pass
