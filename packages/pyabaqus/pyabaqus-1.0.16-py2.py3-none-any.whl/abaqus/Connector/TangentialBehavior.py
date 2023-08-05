from abaqusConstants import *


class TangentialBehavior:
    """The TangentialBehavior object specifies tangential behavior for a connector friction
    behavior option. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import section
        mdb.models[name].sections[name].behaviorOptions[i].tangentialBehavior
        import odbSection
        session.odbs[name].sections[name].behaviorOptions[i].tangentialBehavior

        The table data for this object are:

        - If *formulation*=PENALTY, the table data specify the following:
            - Friction coefficient in the slip direction, μμ.
            - Slip rate, if the data depend on slip rate.
            - Contact pressure, if the data depend on contact pressure.
            - Temperature, if the data depend on temperature.
            - Value of the first field variable, if the data depend on field variables.
            - Value of the second field variable.
            - Etc.
        - If *formulation*=EXPONENTIAL_DECAY and *exponentialDecayDefinition*=COEFFICIENTS, the table data specify the following:
            - Static friction coefficient, μsμs.
            - Kinetic friction coefficient, μkμk.
            - Decay coefficient, dcdc.
        - If *formulation*=EXPONENTIAL_DECAY and *exponentialDecayDefinition*=TEST_DATA, the table data specify the following:
            - Static coefficient of friction.
            - Dynamic friction coefficient measured at the reference slip rate, ˙γ2γ˙2.
            - Reference slip rate, ˙γ2γ˙2, used to measure the dynamic friction coefficient.
            - Kinetic friction coefficient, μ∞μ∞. This value corresponds to the asymptotic value of the friction coefficient at infinite slip rate, ˙γ∞γ˙∞.

    The corresponding analysis keywords are:

    - FRICTION

    """

    def __init__(self, formulation: SymbolicConstant = PENALTY, slipRateDependency: Boolean = OFF,
                 pressureDependency: Boolean = OFF, temperatureDependency: Boolean = OFF,
                 dependencies: int = 0, exponentialDecayDefinition: SymbolicConstant = COEFFICIENTS,
                 shearStressLimit: float = None, maximumElasticSlip: SymbolicConstant = FRACTION,
                 fraction: float = None, absoluteDistance: float = None, table: tuple = ()):
        """This method creates a TangentialBehavior object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].sections[name].behaviorOptions[i].TangentialBehavior
            session.odbs[name].sections[name].behaviorOptions[i].TangentialBehavior
        
        Parameters
        ----------
        formulation
            A SymbolicConstant specifying the friction coefficient formulation. Possible values are 
            PENALTY and EXPONENTIAL_DECAY. The default value is PENALTY. 
        slipRateDependency
            A Boolean specifying whether the data depend on slip rate. The default value is OFF. 
        pressureDependency
            A Boolean specifying whether the data depend on contact pressure. The default value is 
            OFF. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variables for the data. The default value is 0. 
        exponentialDecayDefinition
            A SymbolicConstant specifying the exponential decay definition for the data. Possible 
            values are COEFFICIENTS and TEST_DATA. The default value is COEFFICIENTS. 
        shearStressLimit
            None or a Float specifying no upper limit or the friction coefficient shear stress 
            limit. The default value is None. 
        maximumElasticSlip
            A SymbolicConstant specifying the method for modifying the allowable elastic slip. 
            Possible values are FRACTION and ABSOLUTE_DISTANCE. The default value is FRACTION.This 
            argument applies only to Abaqus/Standard analyses. 
        fraction
            A Float specifying the ratio of the allowable maximum elastic slip to a characteristic 
            model dimension. The default value is 10–4.This argument applies only to Abaqus/Standard 
            analyses. 
        absoluteDistance
            None or a Float specifying the absolute magnitude of the allowable elastic slip. The 
            default value is None.This argument applies only to Abaqus/Standard analyses. 
        table
            A sequence of sequences of Floats specifying the tangential properties. Items in the 
            table data are described below. The default value is an empty sequence. 

        Returns
        -------
            A TangentialBehavior object.
        """
        pass

    def setValues(self):
        """This method modifies the TangentialBehavior object.
        """
        pass
