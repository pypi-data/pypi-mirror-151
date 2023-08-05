from abaqusConstants import *
from .ContactControl import ContactControl


class StdContactControl(ContactControl):
    """The StdContactControl object is used in Abaqus/Standard analyses to specify optional
    solution controls for problems involving contact between bodies. 
    The StdContactControl object is derived from the ContactControl object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import interaction
        mdb.models[name].contactControls[name]

    The corresponding analysis keywords are:

    - CONTACT CONTROLS

    """

    def __init__(self, name: str, stiffnessScaleFactor: float = 1,
                 penetrationTolChoice: SymbolicConstant = RELATIVE,
                 relativePenetrationTolerance: float = None, absolutePenetrationTolerance: float = None,
                 frictionOnset: SymbolicConstant = None, automaticTolerances: Boolean = OFF,
                 maxchp: int = 0, perrmx: float = 0, uerrmx: float = 0,
                 stabilizeChoice: SymbolicConstant = NONE, dampFactor: float = 1, dampCoef: float = 0,
                 tangFraction: float = 1, eosFraction: float = 0,
                 zeroDampingChoice: SymbolicConstant = COMPUTE, zeroDamping: float = None,
                 enforceWithLagrangeMultipliers: SymbolicConstant = DEFAULT):
        """This method creates an StdContactControl object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].StdContactControl
        
        Parameters
        ----------
        name
            A String specifying the contact controls repository key. 
        stiffnessScaleFactor
            A Float specifying the factor by which Abaqus/Standard will scale the default penalty 
            stiffness to obtain the stiffnesses used for the contact pairs. Only contact 
            interactions defined with augmented Lagrangian surface behavior will be affected by this 
            argument. The default value is 1.0. 
        penetrationTolChoice
            A SymbolicConstant specifying whether the allowable penetration is an absolute value or 
            a value relative to the characteristic contact surface face dimension. Only contact 
            interactions defined with augmented Lagrangian surface behavior will be affected by this 
            argument. Possible values are RELATIVE and ABSOLUTE. The default value is RELATIVE. 
        relativePenetrationTolerance
            A Float specifying the ratio of the allowable penetration to the characteristic contact 
            surface face dimension. The float values represent percentages (e.g.: 0.001=0.1%). Only 
            contact interactions defined with augmented Lagrangian surface behavior will be affected 
            by this argument. The default value is 10–3.The *relativePenetrationTolerance* argument 
            applies only when *penetrationTolChoice*=RELATIVE. The *relativePenetrationTolerance* 
            and *absolutePenetrationTolerance* arguments are mutually exclusive. 
        absolutePenetrationTolerance
            None or a Float specifying the allowable penetration. Only contact interactions defined 
            with augmented Lagrangian surface behavior will be affected by this argument. The 
            *absolutePenetrationTolerance* argument applies only when 
            *penetrationTolChoice*=ABSOLUTE. The *relativePenetrationTolerance* and 
            *absolutePenetrationTolerance* arguments are mutually exclusive. The default value is 
            None. 
        frictionOnset
            A SymbolicConstant specifying when the application of friction occurs. Possible values 
            are: 
            - IMMEDIATE, specifying the friction is included in the increment when contact occurs. 
            - DELAYED, specifying the application of friction is delayed until the increment after 
            contact occurs. 
        automaticTolerances
            A Boolean specifying whether Abaqus/Standard should automatically compute an overclosure 
            tolerance and a separation tolerance to prevent chattering in contact. The default value 
            is OFF.The *automaticTolerances* argument cannot be used with the *maxchp*, *perrmx*, 
            and *uerrmx* arguments. 
        maxchp
            An Int specifying the maximum number of points that are permitted to violate contact 
            conditions in any increment. The default value is 0.Either the *perrmx* or the *uerrmx* 
            argument must be specified in conjunction with the *maxchp* argument. 
        perrmx
            A Float specifying the maximum value of tensile stress (tensile force in GAP- or 
            ITT-type contact elements) allowed to be transmitted at a contact point. The default 
            value is 0.0.The *perrmx* argument must be specified in conjunction with the *maxchp* 
            argument. 
        uerrmx
            A Float specifying the maximum overclosure distance allowed at a secondary node that is 
            considered to be open. The default value is 0.0.The *uerrmx* argument must be specified 
            in conjunction with the *maxchp* argument. 
        stabilizeChoice
            A SymbolicConstant specifying whether or not viscous damping will be specified, and if 
            so, how it will be specified. Possible values are NONE, AUTOMATIC, and COEFFICIENT. The 
            default value is NONE. 
        dampFactor
            A Float specifying the value of the damping factor. This value is multiplied by the 
            calculated damping coefficient. The default value is 1.0.This argument is only valid 
            when *stabilizeChoice*=AUTOMATIC. 
        dampCoef
            A Float specifying the damping coefficient. The default value is 0.0.This argument is 
            only valid when *stabilizeChoice*=COEFFICIENT. 
        tangFraction
            A Float specifying the tangential stabilization as a fraction of the normal 
            stabilization (damping). The default value is 1.0.This argument is valid only if 
            *stabilizeChoice* = AUTOMATIC or COEFFICIENT. 
        eosFraction
            A Float specifying the fraction of the damping that remains at the end of the step. The 
            default value is 0.0.This argument is valid only if *stabilizeChoice* = AUTOMATIC or 
            COEFFICIENT. 
        zeroDampingChoice
            A SymbolicConstant specifying how the zero-damping clearance will be specified. Possible 
            values are COMPUTE and SPECIFY. The default value is COMPUTE.This argument is valid only 
            if *stabilizeChoice* = AUTOMATIC or COEFFICIENT. 
        zeroDamping
            None or a Float specifying the clearance at which damping becomes zero. This argument is 
            valid only when *zeroDampingChoice*=SPECIFY. This argument is valid only if 
            *stabilizeChoice* = AUTOMATIC or COEFFICIENT. The default value is None. 
        enforceWithLagrangeMultipliers
            A SymbolicConstant specifying whether to enforce the contact constraints with Lagrange 
            multipliers. Possible values are DEFAULT, ENFORCEMENT_OFF, and ENFORCEMENT_ON. The 
            default value is DEFAULT. 

        Returns
        -------
            A StdContactControl object. 

        Raises
        ------
        RangeError
        """
        super().__init__()
        pass

    def setValues(self, stiffnessScaleFactor: float = 1, penetrationTolChoice: SymbolicConstant = RELATIVE,
                  relativePenetrationTolerance: float = None, absolutePenetrationTolerance: float = None,
                  frictionOnset: SymbolicConstant = None, automaticTolerances: Boolean = OFF,
                  maxchp: int = 0, perrmx: float = 0, uerrmx: float = 0,
                  stabilizeChoice: SymbolicConstant = NONE, dampFactor: float = 1, dampCoef: float = 0,
                  tangFraction: float = 1, eosFraction: float = 0,
                  zeroDampingChoice: SymbolicConstant = COMPUTE, zeroDamping: float = None,
                  enforceWithLagrangeMultipliers: SymbolicConstant = DEFAULT):
        """This method modifies the StdContactControl object.
        
        Parameters
        ----------
        stiffnessScaleFactor
            A Float specifying the factor by which Abaqus/Standard will scale the default penalty 
            stiffness to obtain the stiffnesses used for the contact pairs. Only contact 
            interactions defined with augmented Lagrangian surface behavior will be affected by this 
            argument. The default value is 1.0. 
        penetrationTolChoice
            A SymbolicConstant specifying whether the allowable penetration is an absolute value or 
            a value relative to the characteristic contact surface face dimension. Only contact 
            interactions defined with augmented Lagrangian surface behavior will be affected by this 
            argument. Possible values are RELATIVE and ABSOLUTE. The default value is RELATIVE. 
        relativePenetrationTolerance
            A Float specifying the ratio of the allowable penetration to the characteristic contact 
            surface face dimension. The float values represent percentages (e.g.: 0.001=0.1%). Only 
            contact interactions defined with augmented Lagrangian surface behavior will be affected 
            by this argument. The default value is 10–3.The *relativePenetrationTolerance* argument 
            applies only when *penetrationTolChoice*=RELATIVE. The *relativePenetrationTolerance* 
            and *absolutePenetrationTolerance* arguments are mutually exclusive. 
        absolutePenetrationTolerance
            None or a Float specifying the allowable penetration. Only contact interactions defined 
            with augmented Lagrangian surface behavior will be affected by this argument. The 
            *absolutePenetrationTolerance* argument applies only when 
            *penetrationTolChoice*=ABSOLUTE. The *relativePenetrationTolerance* and 
            *absolutePenetrationTolerance* arguments are mutually exclusive. The default value is 
            None. 
        frictionOnset
            A SymbolicConstant specifying when the application of friction occurs. Possible values 
            are: 
            - IMMEDIATE, specifying the friction is included in the increment when contact occurs. 
            - DELAYED, specifying the application of friction is delayed until the increment after 
            contact occurs. 
        automaticTolerances
            A Boolean specifying whether Abaqus/Standard should automatically compute an overclosure 
            tolerance and a separation tolerance to prevent chattering in contact. The default value 
            is OFF.The *automaticTolerances* argument cannot be used with the *maxchp*, *perrmx*, 
            and *uerrmx* arguments. 
        maxchp
            An Int specifying the maximum number of points that are permitted to violate contact 
            conditions in any increment. The default value is 0.Either the *perrmx* or the *uerrmx* 
            argument must be specified in conjunction with the *maxchp* argument. 
        perrmx
            A Float specifying the maximum value of tensile stress (tensile force in GAP- or 
            ITT-type contact elements) allowed to be transmitted at a contact point. The default 
            value is 0.0.The *perrmx* argument must be specified in conjunction with the *maxchp* 
            argument. 
        uerrmx
            A Float specifying the maximum overclosure distance allowed at a secondary node that is 
            considered to be open. The default value is 0.0.The *uerrmx* argument must be specified 
            in conjunction with the *maxchp* argument. 
        stabilizeChoice
            A SymbolicConstant specifying whether or not viscous damping will be specified, and if 
            so, how it will be specified. Possible values are NONE, AUTOMATIC, and COEFFICIENT. The 
            default value is NONE. 
        dampFactor
            A Float specifying the value of the damping factor. This value is multiplied by the 
            calculated damping coefficient. The default value is 1.0.This argument is only valid 
            when *stabilizeChoice*=AUTOMATIC. 
        dampCoef
            A Float specifying the damping coefficient. The default value is 0.0.This argument is 
            only valid when *stabilizeChoice*=COEFFICIENT. 
        tangFraction
            A Float specifying the tangential stabilization as a fraction of the normal 
            stabilization (damping). The default value is 1.0.This argument is valid only if 
            *stabilizeChoice* = AUTOMATIC or COEFFICIENT. 
        eosFraction
            A Float specifying the fraction of the damping that remains at the end of the step. The 
            default value is 0.0.This argument is valid only if *stabilizeChoice* = AUTOMATIC or 
            COEFFICIENT. 
        zeroDampingChoice
            A SymbolicConstant specifying how the zero-damping clearance will be specified. Possible 
            values are COMPUTE and SPECIFY. The default value is COMPUTE.This argument is valid only 
            if *stabilizeChoice* = AUTOMATIC or COEFFICIENT. 
        zeroDamping
            None or a Float specifying the clearance at which damping becomes zero. This argument is 
            valid only when *zeroDampingChoice*=SPECIFY. This argument is valid only if 
            *stabilizeChoice* = AUTOMATIC or COEFFICIENT. The default value is None. 
        enforceWithLagrangeMultipliers
            A SymbolicConstant specifying whether to enforce the contact constraints with Lagrange 
            multipliers. Possible values are DEFAULT, ENFORCEMENT_OFF, and ENFORCEMENT_ON. The 
            default value is DEFAULT.

        Raises
        ------
        RangeError
        """
        pass
