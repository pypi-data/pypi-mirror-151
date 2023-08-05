from abaqusConstants import *
from .Amplitude import Amplitude


class SpectrumAmplitude(Amplitude):
    """The SpectrumAmplitude object defines the spectrum of responses for displacement,
    velocity, or acceleration to be used in a response spectrum analysis. 
    The SpectrumAmplitude object is derived from the Amplitude object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import amplitude
        mdb.models[name].amplitudes[name]
        import odbAmplitude
        session.odbs[name].amplitudes[name]

    The corresponding analysis keywords are:

    - SPECTRUM

    """

    def __init__(self, name: str, method: SymbolicConstant, data: tuple,
                 specificationUnits: SymbolicConstant = ACCELERATION,
                 eventUnits: SymbolicConstant = EVENT_ACCELERATION,
                 solution: SymbolicConstant = ABSOLUTE_VALUE, timeIncrement: float = 0,
                 gravity: float = 1, criticalDamping: Boolean = OFF, timeSpan: SymbolicConstant = STEP,
                 amplitude: str = ''):
        """This method creates a SpectrumAmplitude object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].SpectrumAmplitude
            session.odbs[name].SpectrumAmplitude
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        method
            A SymbolicConstant specifying the method for specifying the spectrum. Possible values 
            are DEFINE and CALCULATE. 
        data
            A sequence of sequences of Floats specifying the magnitude, frequency, and damping 
            values. 
        specificationUnits
            A SymbolicConstant specifying the units used for specifying the spectrum. Possible 
            values are DISPLACEMENT, VELOCITY, ACCELERATION, and GRAVITY. The default value is 
            ACCELERATION. 
        eventUnits
            A SymbolicConstant specifying the units used to describe the dynamic event in the 
            amplitude used for the calculation. Possible values are EVENT_DISPLACEMENT, 
            EVENT_VELOCITY, EVENT_ACCELERATION, and EVENT_GRAVITY. The default value is 
            EVENT_ACCELERATION. 
        solution
            A SymbolicConstant specifying the solution method for the dynamic equations. Possible 
            values are ABSOLUTE_VALUE and RELATIVE_VALUE. The default value is ABSOLUTE_VALUE. 
        timeIncrement
            A Float specifying the implicit time increment used to calculate the spectrum. This 
            argument is required when the *method* = CALCULATE. The default value is 0.0. 
        gravity
            A Float specifying the acceleration due to gravity. This argument applies only when 
            *specificationUnits* = GRAVITY or*eventUnits* = GRAVITY. The default value is 1.0. 
        criticalDamping
            A Boolean specifying whether to calculate the spectrum for only the specified range of 
            critical damping values or a list of values. If *criticalDamping* = ON, the spectrum is 
            calculated only for the specified range of critical damping values. If *criticalDamping* 
            = OFF, the spectrum is calculated for a list of damping values. The default value is 
            OFF. 
        timeSpan
            A SymbolicConstant specifying the time span of the amplitude. Possible values are STEP 
            and TOTAL. The default value is STEP. 
        amplitude
            A String specifying the name of the amplitude that describes the dynamic event used to 
            calculate the spectrum. The default value is an empty string. 

        Returns
        -------
            A SpectrumAmplitude object. 
            
        Raises
        ------
        InvalidNameError
        RangeError 
        """
        super().__init__()
        pass

    def setValues(self, specificationUnits: SymbolicConstant = ACCELERATION,
                  eventUnits: SymbolicConstant = EVENT_ACCELERATION,
                  solution: SymbolicConstant = ABSOLUTE_VALUE, timeIncrement: float = 0,
                  gravity: float = 1, criticalDamping: Boolean = OFF, timeSpan: SymbolicConstant = STEP,
                  amplitude: str = ''):
        """This method modifies the SpectrumAmplitude object.
        
        Parameters
        ----------
        specificationUnits
            A SymbolicConstant specifying the units used for specifying the spectrum. Possible 
            values are DISPLACEMENT, VELOCITY, ACCELERATION, and GRAVITY. The default value is 
            ACCELERATION. 
        eventUnits
            A SymbolicConstant specifying the units used to describe the dynamic event in the 
            amplitude used for the calculation. Possible values are EVENT_DISPLACEMENT, 
            EVENT_VELOCITY, EVENT_ACCELERATION, and EVENT_GRAVITY. The default value is 
            EVENT_ACCELERATION. 
        solution
            A SymbolicConstant specifying the solution method for the dynamic equations. Possible 
            values are ABSOLUTE_VALUE and RELATIVE_VALUE. The default value is ABSOLUTE_VALUE. 
        timeIncrement
            A Float specifying the implicit time increment used to calculate the spectrum. This 
            argument is required when the *method* = CALCULATE. The default value is 0.0. 
        gravity
            A Float specifying the acceleration due to gravity. This argument applies only when 
            *specificationUnits* = GRAVITY or*eventUnits* = GRAVITY. The default value is 1.0. 
        criticalDamping
            A Boolean specifying whether to calculate the spectrum for only the specified range of 
            critical damping values or a list of values. If *criticalDamping* = ON, the spectrum is 
            calculated only for the specified range of critical damping values. If *criticalDamping* 
            = OFF, the spectrum is calculated for a list of damping values. The default value is 
            OFF. 
        timeSpan
            A SymbolicConstant specifying the time span of the amplitude. Possible values are STEP 
            and TOTAL. The default value is STEP. 
        amplitude
            A String specifying the name of the amplitude that describes the dynamic event used to 
            calculate the spectrum. The default value is an empty string.

        Raises
        ------
        RangeError
        """
        pass
