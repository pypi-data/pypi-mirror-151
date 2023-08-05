from abaqusConstants import *
from .Trs import Trs


class Viscosity:
    """The Viscosity object specifies mechanical viscosity.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].viscosity
        import odbMaterial
        session.odbs[name].materials[name].viscosity

    The table data for this object are:
    
    - If *type*=NEWTONIAN, the table data specify the following:

        - Viscosity, k.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.

    The corresponding analysis keywords are:

    - VISCOSITY

    """

    # A Trs object. 
    trs: Trs = Trs()

    def __init__(self, table: tuple, type: SymbolicConstant = NEWTONIAN, temperatureDependency: Boolean = OFF,
                 dependencies: int = 0):
        """This method creates a Viscosity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Viscosity
                session.odbs[name].materials[name].Viscosity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        type
            A SymbolicConstant specifying the type of viscosity. The default value is NEWTONIAN. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Viscosity object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the Viscosity object.

        Raises
        ------
        RangeError
        """
        pass
