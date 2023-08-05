from abaqusConstants import *


class Density:
    """The Density object specifies the material density.

    Notes
    -----
    This object can be accessed by:
        
    .. code-block:: python
            
        import material
        mdb.models[name].materials[name].density
        import odbMaterial
        session.odbs[name].materials[name].density

    The table data for this object are:

    - The mass density.
    - Temperature, if the data depend on temperature.
    - Value of the first field variable, if the data depend on field variables.
    - Value of the second field variable.
    - Etc.

    The corresponding analysis keywords are:

    - DENSITY

    """

    def __init__(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0,
                 distributionType: SymbolicConstant = UNIFORM, fieldName: str = ''):
        """This method creates a Density object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Density
                session.odbs[name].materials[name].Density
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        distributionType
            A SymbolicConstant specifying how the density is distributed spatially. Possible values 
            are UNIFORM, ANALYTICAL_FIELD, and DISCRETE_FIELD. The default value is UNIFORM. 
        fieldName
            A String specifying the name of the AnalyticalField or DiscreteField object associated 
            with this material option. The *fieldName* argument applies only when 
            *distributionType*=ANALYTICAL_FIELD or *distributionType*=DISCRETE_FIELD. The default 
            value is an empty string. 

        Returns
        -------
            A Density object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the Density object.

        Raises
        ------
        RangeError
        """
        pass
