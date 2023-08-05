from abaqusConstants import *


class PressureEffect:
    """The PressureEffect object defines equivalent pressure stress driven mass diffusion.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].diffusivity.pressureEffect
        import odbMaterial
        session.odbs[name].materials[name].diffusivity.pressureEffect

    The table data for this object are:

    - Pressure stress factor, κp.
    - Concentration.
    - Temperature, if the data depend on temperature.
    - Value of the first field variable, if the data depend on field variables.
    - Value of the second field variable.
    - Etc.

    The corresponding analysis keywords are:

    - KAPPA

    """

    def __init__(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0):
        """This method creates a PressureEffect object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].diffusivity.PressureEffect
                session.odbs[name].materials[name].diffusivity.PressureEffect
        
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
            A PressureEffect object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the PressureEffect object.

        Raises
        ------
        RangeError
        """
        pass
