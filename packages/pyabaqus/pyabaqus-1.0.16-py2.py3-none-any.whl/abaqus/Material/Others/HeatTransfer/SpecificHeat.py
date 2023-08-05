from abaqusConstants import *


class SpecificHeat:
    """The SpecificHeat object specifies a material's specific heat.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].specificHeat
        import odbMaterial
        session.odbs[name].materials[name].specificHeat

    The table data for this object are:

    - Specific heat per unit mass.
    - Temperature, if the data depend on temperature.
    - Value of the first field variable, if the data depend on field variables.
    - Value of the second field variable.
    - Etc.

    The corresponding analysis keywords are:

    - SPECIFIC HEAT

    """

    def __init__(self, table: tuple, law: SymbolicConstant = CONSTANTVOLUME,
                 temperatureDependency: Boolean = OFF, dependencies: int = 0):
        """This method creates a SpecificHeat object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].SpecificHeat
                session.odbs[name].materials[name].SpecificHeat
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        law
            A SymbolicConstant specifying the specific heat behavior. Possible values are 
            CONSTANTVOLUME and CONSTANTPRESSURE. The default value is CONSTANTVOLUME. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A SpecificHeat object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the SpecificHeat object.

        Raises
        ------
        RangeError
        """
        pass
