from abaqusConstants import *
from .ConnectorBehaviorOption import ConnectorBehaviorOption
from .ConnectorOptions import ConnectorOptions
from .ConnectorPotentialArray import ConnectorPotentialArray
from .DerivedComponent import DerivedComponent
from .TangentialBehavior import TangentialBehavior


class ConnectorFriction(ConnectorBehaviorOption):
    """The ConnectorFriction object defines Coulomb-like or hysteretic friction behavior for
    one or more components of a connector's relative motion. 
    The ConnectorFriction object is derived from the ConnectorBehaviorOption object. 

    Attributes
    ----------
    tangentialBehavior: TangentialBehavior
        A :py:class:`~abaqus.Connector.TangentialBehavior.TangentialBehavior` object.
    derivedComponent: DerivedComponent
        A :py:class:`~abaqus.Connector.DerivedComponent.DerivedComponent` object specifying the :py:class:`~abaqus.Connector.DerivedComponent.DerivedComponent` used to compute the contact
        force component direction. This argument applies only if
        **frictionModel=USER_CUSTOMIZED**, if **useContactForceComponent=ON**, and if
        **contactForceStyle=DERIVED_COMPONENT**.
    options: ConnectorOptions
        A :py:class:`~abaqus.Connector.ConnectorOptions.ConnectorOptions` object specifying the :py:class:`~abaqus.Connector.ConnectorOptions.ConnectorOptions` used to define tabular options
        for this ConnectorBehaviorOption.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import section
        mdb.models[name].sections[name].behaviorOptions[i]
        import odbSection
        session.odbs[name].sections[name].behaviorOptions[i]

    The corresponding analysis keywords are:

    - CONNECTOR FRICTION

    """

    # A TangentialBehavior object. 
    tangentialBehavior: TangentialBehavior = TangentialBehavior()

    # A DerivedComponent object specifying the DerivedComponent used to compute the contact 
    # force component direction. This argument applies only if 
    # *frictionModel*=USER_CUSTOMIZED, if *useContactForceComponent*=ON, and if 
    # *contactForceStyle*=DERIVED_COMPONENT. 
    derivedComponent: DerivedComponent = DerivedComponent()

    # A ConnectorOptions object specifying the ConnectorOptions used to define tabular options 
    # for this ConnectorBehaviorOption. 
    options: ConnectorOptions = ConnectorOptions()

    def __init__(self, frictionModel: SymbolicConstant = PREDEFINED, slipStyle: SymbolicConstant = SPECIFY,
                 tangentDirection: int = None, stickStiffness: float = None,
                 componentType: SymbolicConstant = NO_INDEPENDENT_COMPONENTS,
                 slipDependency: Boolean = OFF, temperatureDependency: Boolean = OFF,
                 dependencies: int = 0, useContactForceComponent: Boolean = OFF,
                 contactForceStyle: SymbolicConstant = COMPONENT_NUMBER, contactForceComponent: int = 0,
                 forcePotentialOperator: SymbolicConstant = SUM, forcePotentialExponent: float = 2,
                 connectorPotentials: ConnectorPotentialArray = None,
                 table: tuple = (), independentComponents: tuple = ()):
        """This method creates a connector friction behavior option for a ConnectorSection object.
        Depending upon the arguments provided, the friction behavior can be Coulomb-like or
        hysteretic in nature.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

                      import connectorBehavior
                      connectorBehavior.ConnectorFriction
                      import odbConnectorBehavior
                      odbConnectorBehavior.ConnectorFriction
        
        Parameters
        ----------
        frictionModel
            A SymbolicConstant specifying the desired frictional response model. Possible values are 
            PREDEFINED and USER_CUSTOMIZED. The default value is PREDEFINED. 
        slipStyle
            A SymbolicConstant specifying the method of indicating the slip direction: either 
            specified or computed based upon the force potential data. Possible values are SPECIFY 
            and COMPUTE. The default value is SPECIFY.This argument is applicable only if 
            *frictionModel*=USER_CUSTOMIZED. 
        tangentDirection
            None or an Int specifying the direction for which the frictional behavior is specified. 
            Possible values are 1 ≤≤ *tangentDirection* ≤≤ 6, indicating an available component of 
            relative motion. This argument applies only if *frictionModel*=USER_CUSTOMIZED and if 
            *slipStyle*=SPECIFY. The default value is None. 
        stickStiffness
            None or a Float specifying the stick stiffness associated with the frictional behavior 
            in the direction specified by *tangentDirection*. If this argument is omitted, Abaqus 
            computes an appropriate number for the stick stiffness. The default value is None. 
        componentType
            A SymbolicConstant specifying the type of the *independentComponents*. Possible values 
            are POSITION, MOTION, and NO_INDEPENDENT_COMPONENTS. The default value is 
            NO_INDEPENDENT_COMPONENTS. 
        slipDependency
            A Boolean specifying whether the table data depend on accumulated slip. The default 
            value is OFF.This argument applies only if *frictionModel*=USER_CUSTOMIZED. 
        temperatureDependency
            A Boolean specifying whether the table data depend on temperature. The default value is 
            OFF.This argument applies only if *frictionModel*=USER_CUSTOMIZED. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0.This 
            argument applies only if *frictionModel*=USER_CUSTOMIZED. 
        useContactForceComponent
            A Boolean specifying whether the contact force component will be defined. The default 
            value is OFF.This argument applies only if *frictionModel*=USER_CUSTOMIZED. 
        contactForceStyle
            A SymbolicConstant specifying the method of indicating the contact force component 
            direction: either specified or computed based on upon a DerivedComponent. Possible 
            values are COMPONENT_NUMBER and DERIVED_COMPONENT. The default value is 
            COMPONENT_NUMBER.This argument is applicable only if *frictionModel*=USER_CUSTOMIZED and 
            if *useContactForceComponent*=ON. 
        contactForceComponent
            An Int specifying the contact force component direction. This argument applies only if 
            *frictionModel*=USER_CUSTOMIZED, if *useContactForceComponent*=ON, and if 
            *contactForceStyle*=COMPONENT_NUMBER. The default value is 0. 
        forcePotentialOperator
            A SymbolicConstant specifying the contribution operator for the force potential 
            contributions. Possible values are SUM and MAXIMUM. The default value is SUM.This 
            argument is applicable only if *frictionModel*=USER_CUSTOMIZED and if 
            *slipStyle*=COMPUTE. 
        forcePotentialExponent
            A Float specifying the number equal to the inverse of the overall exponent in the force 
            potential definition. The default value is 2.0.This argument is applicable only if 
            *frictionModel*=USER_CUSTOMIZED, if *slipStyle*=COMPUTE, and if 
            *forcePotentialOperator*=SUM. 
        connectorPotentials
            A ConnectorPotentialArray object specifying one ConnectorPotential object for each force 
            potential contribution. This member can be specified only if 
            *frictionModel*=USER_CUSTOMIZED, and if *slipStyle*=COMPUTE. 
        table
            A sequence of sequences of Floats specifying friction properties. The default value is 
            an empty sequence.If *frictionModel*=PREDEFINED, each sequence of the table data 
            specifies:If applicable, the first geometric scaling constant relevant to frictional 
            interactions.Etc., up to as many geometric scaling constants as are associated with this 
            connection type.Internal contact force/moment generating friction in the first 
            predefined slip direction.If applicable, internal contact force/moment generating 
            friction in the second predefined slip direction.Connector constitutive relative motion 
            in the direction specified by *independentComponent*.Accumulated slip in the first 
            predefined slip direction, if the data depend on accumulated slip.Temperature, if the 
            data depend on temperature.Value of the first field variable, if the data depend on 
            field variables.Value of the second field variable.Etc.If 
            *frictionModel*=USER_CUSTOMIZED, each sequence of the table data specifies:Effective 
            radius of the cylindrical or spherical surface over which frictional slip occurs in the 
            connector associated with frictional effects in the direction specified by 
            *tangentDirection*. This radius is relevant only if the connection type includes an 
            available rotational component of relative motion and 
            *tangentDirection*=SLIP_DIRECTION.Internal contact force/moment generating friction in 
            the direction specified by *tangentDirection*.Connector constitutive relative motion in 
            the direction specified by *independentComponent*.Accumulated slip in the direction 
            specified by *tangentDirection*, if the data depend on accumulated slip.Temperature, if 
            the data depend on temperature.Value of the first field variable, if the data depend on 
            field variables.Value of the second field variable.Etc. 
        independentComponents
            A sequence of Ints specifying the independent components. Possible values are 1 ≤≤ 
            *independentComponents* ≤≤ 6. In addition, each independent component value must be 
            unique. The *independentComponents* argument applies only if 
            *frictionModel*=USER_CUSTOMIZED. Only available components can be specified. The default 
            value is an empty sequence. 

        Returns
        -------
            A ConnectorFriction object. 

        Raises
        ------
            ValueError and TextError. 
        """
        super().__init__()
        pass

    def setValues(self):
        """This method modifies the ConnectorFriction object.

        Raises
        ------
            ValueError. 
        """
        pass
