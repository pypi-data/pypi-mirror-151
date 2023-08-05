from abaqusConstants import *
from .CastIronCompressionHardening import CastIronCompressionHardening
from .CastIronTensionHardening import CastIronTensionHardening


class CastIronPlasticity:
    """The CastIronPlasticity object specifies the Cast Iron plasticity model.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].castIronPlasticity
        import odbMaterial
        session.odbs[name].materials[name].castIronPlasticity

    The table data for this object are:
    
    - Plastic Poisson's ratio, νp⁢l (dimensionless).
    - Temperature, if the data depend on temperature.
    - Value of the first field variable, if the data depend on field variables.
    - Value of the second field variable.
    - Etc.

    The corresponding analysis keywords are:

    - CAST IRON PLASTICITY

    """

    # A CastIronTensionHardening object. 
    castIronTensionHardening: CastIronTensionHardening = CastIronTensionHardening(((),))

    # A CastIronCompressionHardening object. 
    castIronCompressionHardening: CastIronCompressionHardening = CastIronCompressionHardening(((),))

    def __init__(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0):
        """This method creates a CastIronPlasticity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].CastIronPlasticity
                session.odbs[name].materials[name].CastIronPlasticity
        
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
            A CastIronPlasticity object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the CastIronPlasticity object.

        Raises
        ------
        RangeError
        """
        pass
