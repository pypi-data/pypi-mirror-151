from abaqusConstants import *


class Ratios:
    """The Ratios object specifies ratios that define anisotropic swelling.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].moistureSwelling.ratios
        mdb.models[name].materials[name].swelling.ratios
        import odbMaterial
        session.odbs[name].materials[name].moistureSwelling.ratios
        session.odbs[name].materials[name].swelling.ratios

        The table data for this object are:
            - r11.
            - r22.
            - r33.
            - Temperature, if the data depend on temperature.
            - Value of the first field variable, if the data depend on field variables.
            - Value of the second field variable.
            - Etc.

    The corresponding analysis keywords are:

    - RATIOS

    """

    def __init__(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0):
        """This method creates a Ratios object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].materials[name].moistureSwelling.Ratios
            mdb.models[name].materials[name].swelling.Ratios
            session.odbs[name].materials[name].moistureSwelling.Ratios
            session.odbs[name].materials[name].swelling.Ratios
        
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
            A Ratios object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the Ratios object.

        Raises
        ------
        RangeError
        """
        pass
