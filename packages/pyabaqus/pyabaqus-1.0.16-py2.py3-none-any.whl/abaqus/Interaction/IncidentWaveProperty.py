from abaqusConstants import *
from .ContactProperty import ContactProperty


class IncidentWaveProperty(ContactProperty):
    """The IncidentWaveProperty object is an interaction property that defines the properties
    referred to by an IncidentWave object. 
    The IncidentWaveProperty object is derived from the InteractionProperty object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import interaction
        mdb.models[name].interactionProperties[name]

    The corresponding analysis keywords are:

    - INCIDENT WAVE INTERACTION PROPERTY
            - UNDEX CHARGE PROPERTY
            - CONWEP CHARGE PROPERTY

    """

    def __init__(self, name: str, definition: SymbolicConstant = PLANAR,
                 propagationModel: SymbolicConstant = ACOUSTIC, soundSpeed: float = None,
                 fluidDensity: float = None, specificHeatRatio: float = None, gravity: float = None,
                 atmosphericPressure: float = None, dragCoefficient: float = None,
                 dragExponent: float = 2, waveEffects: Boolean = ON, chargeDensity: float = None,
                 chargeMass: float = None, constantK1: float = None, constantK2: float = None,
                 constantA: float = None, constantB: float = None, constantKc: float = None,
                 duration: float = None, maximumSteps: int = 1500, relativeStepControl: float = None,
                 absoluteStepControl: float = None, stepControlExponent: float = 0, genDecayA: float = 0,
                 genDecayB: float = 0, genDecayC: float = 0, seedNumber: int = None,
                 massTNT: float = None, massFactor: float = 1, lengthFactor: float = 1,
                 timeFactor: float = 1, pressureFactor: float = 1):
        """This method creates an IncidentWaveProperty object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].IncidentWaveProperty
        
        Parameters
        ----------
        name
            A String specifying the interaction property repository key. 
        definition
            A SymbolicConstant specifying the type of wave to be defined. Possible values are 
            PLANAR, SPHERICAL, DIFFUSE, AIR_BLAST, and SURFACE_BLAST. The default value is PLANAR. 
        propagationModel
            A SymbolicConstant specifying the spherical propagation model. Possible values are 
            ACOUSTIC, UNDEX_CHARGE, and GENERALIZED_DECAY. The default value is ACOUSTIC.This 
            argument is valid only when *definition*=SPHERICAL. 
        soundSpeed
            A Float specifying the speed of sound in the fluid.This argument is not valid when 
            *definition*=AIR_BLAST or when *definition*=SURFACE_BLAST. 
        fluidDensity
            A Float specifying the fluid mass density.This argument is not valid when 
            *definition*=AIR_BLAST or when *definition*=SURFACE_BLAST. 
        specificHeatRatio
            None or a Float specifying the ratio of specific heats for gas. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        gravity
            None or a Float specifying the acceleration due to gravity. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        atmosphericPressure
            None or a Float specifying the atmospheric pressure. The default value is None.This 
            argument is valid only when *definition*=SPHERICAL and *propagationModel*=UNDEX_CHARGE. 
        dragCoefficient
            None or a Float specifying the fluid drag coefficient. The default value is None.This 
            argument is valid only when *definition*=SPHERICAL and *propagationModel*=UNDEX_CHARGE. 
        dragExponent
            A Float specifying the fluid drag exponent. The default value is 2.0.This argument is 
            valid only when *definition*=SPHERICAL and *propagationModel*=UNDEX_CHARGE. 
        waveEffects
            A Boolean specifying whether or not to include wave effects in the fluid and gas. The 
            default value is ON.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        chargeDensity
            None or a Float specifying the density of the charge material. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        chargeMass
            None or a Float specifying the mass of the charge material. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        constantK1
            None or a Float specifying the charge material constant K. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        constantK2
            None or a Float specifying the charge material constant k. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        constantA
            None or a Float specifying the charge material constant A. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        constantB
            None or a Float specifying the charge material constant B. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        constantKc
            None or a Float specifying the charge material constant Kc. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        duration
            None or a Float specifying the time duration for the bubble simulation. The default 
            value is None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        maximumSteps
            An Int specifying the maximum number of time steps for the bubble simulation. The 
            default value is 1500.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        relativeStepControl
            A Float specifying the relative step size control parameter. The default value is 
            1×10–11.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        absoluteStepControl
            A Float specifying the absolute step size control parameter. The default value is 
            1×10–11.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        stepControlExponent
            A Float specifying the step size control exponent. The default value is 0.2.This 
            argument is valid only when *definition*=SPHERICAL and *propagationModel*=UNDEX_CHARGE. 
        genDecayA
            A Float specifying the constant A associated with the generalized decay propagation 
            model. The default value is 0.0.This argument is valid only when *definition*=SPHERICAL 
            and *propagationModel*=GENERALIZED_DECAY. 
        genDecayB
            A Float specifying the constant B associated with the generalized decay propagation 
            model. The default value is 0.0.This argument is valid only when *definition*=SPHERICAL 
            and *propagationModel*=GENERALIZED_DECAY. 
        genDecayC
            A Float specifying the constant C associated with the generalized decay propagation 
            model. The default value is 0.0.This argument is valid only when *definition*=SPHERICAL 
            and *propagationModel*=GENERALIZED_DECAY. 
        seedNumber
            An Int specifying the seed number (N) for the diffuse source calculation. N2 sources 
            will be used in the simulation.This argument is valid only when *definition*=DIFFUSE. 
        massTNT
            A Float specifying the equivalent mass of TNT, in any preferred mass unit.This argument 
            is valid only when *definition*=AIR_BLAST or *definition*=SURFACE_BLAST. 
        massFactor
            A Float specifying the multiplication factor to convert from the preferred mass unit to 
            kilograms. The default value is 1.0.This argument is valid only when 
            *definition*=AIR_BLAST or *definition*=SURFACE_BLAST. 
        lengthFactor
            A Float specifying the multiplication factor to convert from the analysis length unit to 
            meters. The default value is 1.0.This argument is valid only when *definition*=AIR_BLAST 
            or *definition*=SURFACE_BLAST. 
        timeFactor
            A Float specifying the multiplication factor to convert from the analysis time unit to 
            seconds. The default value is 1.0.This argument is valid only when 
            *definition*=AIR_BLAST or *definition*=SURFACE_BLAST. 
        pressureFactor
            A Float specifying the multiplication factor to convert from the analysis pressure unit 
            to pascals. The default value is 1.0.This argument is valid only when 
            *definition*=AIR_BLAST or *definition*=SURFACE_BLAST. 

        Returns
        -------
            An IncidentWaveProperty object.
        """
        super().__init__(name)
        pass

    def setValues(self, definition: SymbolicConstant = PLANAR, propagationModel: SymbolicConstant = ACOUSTIC,
                  soundSpeed: float = None, fluidDensity: float = None, specificHeatRatio: float = None,
                  gravity: float = None, atmosphericPressure: float = None, dragCoefficient: float = None,
                  dragExponent: float = 2, waveEffects: Boolean = ON, chargeDensity: float = None,
                  chargeMass: float = None, constantK1: float = None, constantK2: float = None,
                  constantA: float = None, constantB: float = None, constantKc: float = None,
                  duration: float = None, maximumSteps: int = 1500, relativeStepControl: float = None,
                  absoluteStepControl: float = None, stepControlExponent: float = 0, genDecayA: float = 0,
                  genDecayB: float = 0, genDecayC: float = 0, seedNumber: int = None,
                  massTNT: float = None, massFactor: float = 1, lengthFactor: float = 1,
                  timeFactor: float = 1, pressureFactor: float = 1):
        """This method modifies the IncidentWaveProperty object.
        
        Parameters
        ----------
        definition
            A SymbolicConstant specifying the type of wave to be defined. Possible values are 
            PLANAR, SPHERICAL, DIFFUSE, AIR_BLAST, and SURFACE_BLAST. The default value is PLANAR. 
        propagationModel
            A SymbolicConstant specifying the spherical propagation model. Possible values are 
            ACOUSTIC, UNDEX_CHARGE, and GENERALIZED_DECAY. The default value is ACOUSTIC.This 
            argument is valid only when *definition*=SPHERICAL. 
        soundSpeed
            A Float specifying the speed of sound in the fluid.This argument is not valid when 
            *definition*=AIR_BLAST or when *definition*=SURFACE_BLAST. 
        fluidDensity
            A Float specifying the fluid mass density.This argument is not valid when 
            *definition*=AIR_BLAST or when *definition*=SURFACE_BLAST. 
        specificHeatRatio
            None or a Float specifying the ratio of specific heats for gas. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        gravity
            None or a Float specifying the acceleration due to gravity. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        atmosphericPressure
            None or a Float specifying the atmospheric pressure. The default value is None.This 
            argument is valid only when *definition*=SPHERICAL and *propagationModel*=UNDEX_CHARGE. 
        dragCoefficient
            None or a Float specifying the fluid drag coefficient. The default value is None.This 
            argument is valid only when *definition*=SPHERICAL and *propagationModel*=UNDEX_CHARGE. 
        dragExponent
            A Float specifying the fluid drag exponent. The default value is 2.0.This argument is 
            valid only when *definition*=SPHERICAL and *propagationModel*=UNDEX_CHARGE. 
        waveEffects
            A Boolean specifying whether or not to include wave effects in the fluid and gas. The 
            default value is ON.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        chargeDensity
            None or a Float specifying the density of the charge material. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        chargeMass
            None or a Float specifying the mass of the charge material. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        constantK1
            None or a Float specifying the charge material constant K. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        constantK2
            None or a Float specifying the charge material constant k. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        constantA
            None or a Float specifying the charge material constant A. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        constantB
            None or a Float specifying the charge material constant B. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        constantKc
            None or a Float specifying the charge material constant Kc. The default value is 
            None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        duration
            None or a Float specifying the time duration for the bubble simulation. The default 
            value is None.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        maximumSteps
            An Int specifying the maximum number of time steps for the bubble simulation. The 
            default value is 1500.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        relativeStepControl
            A Float specifying the relative step size control parameter. The default value is 
            1×10–11.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        absoluteStepControl
            A Float specifying the absolute step size control parameter. The default value is 
            1×10–11.This argument is valid only when *definition*=SPHERICAL and 
            *propagationModel*=UNDEX_CHARGE. 
        stepControlExponent
            A Float specifying the step size control exponent. The default value is 0.2.This 
            argument is valid only when *definition*=SPHERICAL and *propagationModel*=UNDEX_CHARGE. 
        genDecayA
            A Float specifying the constant A associated with the generalized decay propagation 
            model. The default value is 0.0.This argument is valid only when *definition*=SPHERICAL 
            and *propagationModel*=GENERALIZED_DECAY. 
        genDecayB
            A Float specifying the constant B associated with the generalized decay propagation 
            model. The default value is 0.0.This argument is valid only when *definition*=SPHERICAL 
            and *propagationModel*=GENERALIZED_DECAY. 
        genDecayC
            A Float specifying the constant C associated with the generalized decay propagation 
            model. The default value is 0.0.This argument is valid only when *definition*=SPHERICAL 
            and *propagationModel*=GENERALIZED_DECAY. 
        seedNumber
            An Int specifying the seed number (N) for the diffuse source calculation. N2 sources 
            will be used in the simulation.This argument is valid only when *definition*=DIFFUSE. 
        massTNT
            A Float specifying the equivalent mass of TNT, in any preferred mass unit.This argument 
            is valid only when *definition*=AIR_BLAST or *definition*=SURFACE_BLAST. 
        massFactor
            A Float specifying the multiplication factor to convert from the preferred mass unit to 
            kilograms. The default value is 1.0.This argument is valid only when 
            *definition*=AIR_BLAST or *definition*=SURFACE_BLAST. 
        lengthFactor
            A Float specifying the multiplication factor to convert from the analysis length unit to 
            meters. The default value is 1.0.This argument is valid only when *definition*=AIR_BLAST 
            or *definition*=SURFACE_BLAST. 
        timeFactor
            A Float specifying the multiplication factor to convert from the analysis time unit to 
            seconds. The default value is 1.0.This argument is valid only when 
            *definition*=AIR_BLAST or *definition*=SURFACE_BLAST. 
        pressureFactor
            A Float specifying the multiplication factor to convert from the analysis pressure unit 
            to pascals. The default value is 1.0.This argument is valid only when 
            *definition*=AIR_BLAST or *definition*=SURFACE_BLAST. 
        """
        pass
