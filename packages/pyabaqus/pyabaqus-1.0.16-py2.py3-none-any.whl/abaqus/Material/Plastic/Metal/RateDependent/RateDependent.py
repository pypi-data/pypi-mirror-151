
from abaqusConstants import *


class RateDependent:
    """The RateDependent object defines a rate-dependent viscoplastic model.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].crushableFoam.rateDependent
        mdb.models[name].materials[name].druckerPrager.rateDependent
        mdb.models[name].materials[name].Plastic.rateDependent
        import odbMaterial
        session.odbs[name].materials[name].crushableFoam.rateDependent
        session.odbs[name].materials[name].druckerPrager.rateDependent
        session.odbs[name].materials[name].Plastic.rateDependent

    The table data for this object are:
    
    - If *type*=POWER_LAW, the table data specify the following:
        - D.
        - n.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *type*=YIELD_RATIO, the table data specify the following:
        - Yield stress ratio, R=¯σ/σ0.
        - Equivalent Plastic strain rate, ˙¯εpl.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *type*=JOHNSON_COOK, the table data specify the following:
        - C.
        - ˙ε0.

    The corresponding analysis keywords are:

    - RATE DEPENDENT

    """

    def __init__(self, table: tuple, type: SymbolicConstant = POWER_LAW, temperatureDependency: Boolean = OFF,
                 dependencies: int = 0):
        """This method creates a RateDependent object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].crushableFoam.RateDependent
                mdb.models[name].materials[name].druckerPrager.RateDependent
                mdb.models[name].materials[name].Plastic.RateDependent
                session.odbs[name].materials[name].crushableFoam.RateDependent
                session.odbs[name].materials[name].druckerPrager.RateDependent
                session.odbs[name].materials[name].Plastic.RateDependent
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        type
            A SymbolicConstant specifying the type of rate-dependent data. Possible values are 
            POWER_LAW, YIELD_RATIO, and JOHNSON_COOK. The default value is POWER_LAW. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A RateDependent object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the RateDependent object.

        Raises
        ------
        RangeError
        """
        pass
