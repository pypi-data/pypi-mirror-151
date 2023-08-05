from abaqusConstants import *


class GasketTransverseShearElastic:
    """The GasketTransverseShearElastic object defines the elastic parameters for the
    transverse shear behavior of a gasket. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].gasketTransverseShearElastic
        import odbMaterial
        session.odbs[name].materials[name].gasketTransverseShearElastic

    The table data for this object are:

    - Shear stiffness. (This value cannot be negative.)
    - Temperature, if the data depend on temperature.
    - Value of the first field variable, if the data depend on field variables.
    - Value of the second field variable.
    - Etc.

    The corresponding analysis keywords are:

    - GASKET ELASTICITY

    """

    def __init__(self, table: tuple, variableUnits: SymbolicConstant = STRESS,
                 temperatureDependency: Boolean = OFF, dependencies: int = 0):
        """This method creates a GasketTransverseShearElastic object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].GasketTransverseShearElastic
                session.odbs[name].materials[name].GasketTransverseShearElastic
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        variableUnits
            A SymbolicConstant specifying the unit system in which the transverse shear behavior 
            will be defined. Possible values are STRESS and FORCE. The default value is STRESS. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A GasketTransverseShearElastic object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the GasketTransverseShearElastic object.

        Raises
        ------
        RangeError
        """
        pass
