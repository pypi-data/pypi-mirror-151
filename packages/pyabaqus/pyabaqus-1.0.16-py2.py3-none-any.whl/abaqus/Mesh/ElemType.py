from abaqusConstants import *


class ElemType:
    """The ElemType object is an argument object used as an argument in the setElementType
    command. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import mesh

    """

    def __init__(self, elemCode: SymbolicConstant, elemLibrary: SymbolicConstant = STANDARD,
                 hourglassStiffness: float = 0, bendingHourglass: float = 0,
                 drillingHourglass: float = 0, kinematicSplit: SymbolicConstant = AVERAGE_STRAIN,
                 distortionControl: Boolean = OFF, lengthRatio: float = ON,
                 secondOrderAccuracy: Boolean = OFF, hourglassControl: SymbolicConstant = ENHANCED,
                 weightFactor: float = 0, displacementHourglass: float = 1,
                 rotationalHourglass: float = 1, outOfPlaneDisplacementHourglass: float = 1,
                 elemDeletion: SymbolicConstant = DEFAULT,
                 particleConversion: SymbolicConstant = DEFAULT, particleConversionThreshold: float = 0,
                 particleConversionPPD: int = 1, particleConversionKernel: SymbolicConstant = CUBIC,
                 maxDegradation: float = None, viscosity: float = 0, linearBulkViscosity: float = 1,
                 quadraticBulkViscosity: float = 1, numFourierModes: int = 1, nodeOffset: int = None,
                 linearKinematicCtrl: float = None, initialGapOpening: float = None):
        """This method creates an ElemType object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mesh.ElemType
        
        Parameters
        ----------
        elemCode
            A SymbolicConstant specifying the Abaqus element code or just the element shape. 
            Possible values are: 
            
            - C3D8R, specifying a 8-node linear brick, reduced integration with hourglass control. 
            - CODE, specifying add more codes. 
            - UNKNOWN_TRI, specifying an unknown element type associated with a triangular shape. 
            - UNKNOWN_QUAD, specifying an unknown element type associated with a quadrilateral 
            shape. 
            - UNKNOWN_HEX, specifying an unknown element type associated with a hexahedral shape. 
            - UNKNOWN_WEDGE, specifying an unknown element type associated with a wedge shape. 
            - UNKNOWN_TET, specifying an unknown element type associated with a tetrahedral shape. 
        elemLibrary
            A SymbolicConstant specifying the Abaqus element library to use. Possible values are 
            STANDARD and EXPLICIT. The default value is STANDARD. 
        hourglassStiffness
            A Float specifying the hourglass stiffness. (For shell elements this is the membrane 
            hourglass stiffness.) A value of zero indicates the default value should be used. The 
            default value will be used where appropriate. The default value is 0.0.This argument is 
            applicable only to some Abaqus/Standard elements. 
        bendingHourglass
            A Float specifying the bending hourglass stiffness. A value of zero indicates the 
            default value should be used. The default value will be used where appropriate. The 
            default value is 0.0.This argument is applicable only to some Abaqus/Standard elements. 
        drillingHourglass
            A Float specifying the drilling hourglass scaling factor. A value of zero indicates the 
            default value should be used. The default value will be used where appropriate. The 
            default value is 0.0.This argument is applicable only to some Abaqus/Standard elements. 
        kinematicSplit
            A SymbolicConstant specifying the kinematic split control. Possible values are 
            AVERAGE_STRAIN, ORTHOGONAL, and CENTROID. The default value is AVERAGE_STRAIN.This 
            argument is applicable only to some Abaqus/Explicit elements. 
        distortionControl
            A Boolean specifying whether to prevent negative element volumes or other excessive 
            distortions in crushable materials. The default value is OFF.This argument is applicable 
            only to some Abaqus/Explicit elements. 
        lengthRatio
            A Float specifying the length ratio for distortion control in crushable materials. 
            Possible values are 0.0 ≤≤ *lengthRatio* ≤≤ 1.0. The default value is 
            *lengthRatio*=0.10.1This argument is applicable only when *distortionControl* is ON. 
        secondOrderAccuracy
            A Boolean specifying the second-order accuracy option. The default value is OFF.This 
            argument is applicable only to some Abaqus/Explicit elements. 
        hourglassControl
            A SymbolicConstant specifying the hourglass control. Possible values are 
            RELAX_STIFFNESS, STIFFNESS, VISCOUS, ENHANCED, and COMBINED. The default value is 
            ENHANCED.This argument is applicable only to some Abaqus/Explicit elements. 
        weightFactor
            A Float specifying a weight factor when *hourglassControl*=COMBINED. The default value 
            is 0.5.This argument is applicable only to some Abaqus/Explicit elements. 
        displacementHourglass
            A Float specifying the displacement hourglass scaling factor. The default value will be 
            used where appropriate. The default value is 1.0.This argument is applicable only to 
            some Abaqus/Explicit elements. 
        rotationalHourglass
            A Float specifying the rotational hourglass scaling factor. The default value will be 
            used where appropriate. The default value is 1.0.This argument is applicable only to 
            some Abaqus/Explicit elements. 
        outOfPlaneDisplacementHourglass
            A Float specifying the out-of-plane displacement hourglass scaling factor. The default 
            value will be used where appropriate. The default value is 1.0.This argument is 
            applicable only to some Abaqus/Explicit elements. 
        elemDeletion
            A SymbolicConstant specifying the element deletion option. Possible values are DEFAULT, 
            ON, and OFF. The default value is DEFAULT. 
        particleConversion
            A SymbolicConstant specifying the particle conversion option for smoothed particle 
            hydrodynamics. When not OFF or DEFAULT this argument refers to the criterion used for 
            conversion of elements to particles. Possible values are DEFAULT, OFF, TIME, STRAIN, and 
            STRESS. The default value is DEFAULT.This argument is applicable only to some 
            Abaqus/Explicit elements. 
        particleConversionThreshold
            A Float specifying the threshold value for the particle conversion criterion specified 
            by *particleConversion*. The default value is 0.0.This argument is applicable only to 
            some Abaqus/Explicit elements. 
        particleConversionPPD
            An Int specifying the number of particles per direction for element conversion when 
            *particleConversion* is specified. The default value is 1.This argument is applicable 
            only to some Abaqus/Explicit elements. 
        particleConversionKernel
            A SymbolicConstant specifying the interpolation function for particle conversion when 
            *particleConversion* is specified. Possible values are CUBIC, QUADRATIC, and QUINTIC. 
            The default value is CUBIC.This argument is applicable only to some Abaqus/Explicit 
            elements. 
        maxDegradation
            A Float specifying the maximum degradation option for damage control. The default value 
            is −1.0. 
        viscosity
            A Float specifying the viscosity option. The default value is 0.0.This argument is 
            applicable only to some Abaqus/Standard elements. 
        linearBulkViscosity
            A Float specifying the linear bulk viscosity scaling factor option for Abaqus/Explicit. 
            The default value is 1.0. 
        quadraticBulkViscosity
            A Float specifying the quadratic bulk viscosity scaling factor option for 
            Abaqus/Explicit. The default value is 1.0. 
        numFourierModes
            An Int specifying the number of Fourier modes. Possible values are 1, 2, 3, and 4. The 
            default value is 1.This argument is applicable only for axisymmetric elements with 
            nonlinear asymmetric deformation. 
        nodeOffset
            An Int specifying the positive offset number for specifying the additional nodes needed 
            in the connectivity.This argument is applicable only for axisymmetric elements with 
            nonlinear asymmetric deformation. 
        linearKinematicCtrl
            A Float specifying the linear kinematic conversion value.This argument is applicable 
            only to some Abaqus/Explicit elements. 
        initialGapOpening
            A Float specifying the initial gap opening.This parameter is applicable only to some 
            Abaqus/Standard elements. 

        Returns
        -------
        elemType: ElemType
            An ElemType object 
        """
        pass
