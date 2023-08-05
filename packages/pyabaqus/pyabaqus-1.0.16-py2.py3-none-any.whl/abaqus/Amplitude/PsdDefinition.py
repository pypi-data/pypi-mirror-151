from abaqusConstants import *
from .Amplitude import Amplitude


class PsdDefinition(Amplitude):
    """The PsdDefinition object defines the cross-spectral density frequency function for
    random response loading. 
    The PsdDefinition object is derived from the Amplitude object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import amplitude
        mdb.models[name].amplitudes[name]
        import odbAmplitude
        session.odbs[name].amplitudes[name]

    The corresponding analysis keywords are:

    - PSD-DEFINITION

    """

    def __init__(self, name: str, data: tuple, unitType: SymbolicConstant = FORCE,
                 referenceGravityAcceleration: float = 1, referenecePower: float = 0,
                 user: Boolean = OFF, timeSpan: SymbolicConstant = STEP, amplitude: str = ''):
        """This method creates a PsdDefinition object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].PsdDefinition
            session.odbs[name].PsdDefinition
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        data
            A sequence of sequences of Floats specifying the real part of the frequency function, 
            the imaginary part of the frequency function, and the frequency or frequency band number 
            values, depending on the value of *unitType*. 
        unitType
            A SymbolicConstant specifying the type of units for specifying the frequency function. 
            FORCE implies power units. BASE implies gravity used to define base motion. DB implies 
            decibel units. Possible values are FORCE, BASE, and DB. The default value is FORCE. 
        referenceGravityAcceleration
            A Float specifying the reference gravity acceleration. This argument applies when 
            *unitType* = BASE. The default value is 1.0. 
        referenecePower
            A Float specifying the reference power value, in load units squared. This argument 
            applies when *unitType* = DB. The default value is 0.0. 
        user
            A Boolean specifying whether the frequency function is defined in user subroutine UPSD. 
            If specified, then *data* is not applicable, and the *unitType* value must not be DB. 
            The default value is OFF. 
        timeSpan
            A SymbolicConstant specifying the time span of the amplitude. Possible values are STEP 
            and TOTAL. The default value is STEP. 
        amplitude
            A String specifying the name of the amplitude that describes the dynamic event used to 
            define the cross-spectral density frequency function. The default value is an empty 
            string. 

        Returns
        -------
            A PsdDefinition object. 
            
        Raises
        ------
        InvalidNameError
        RangeError 
        """
        super().__init__()
        pass

    def setValues(self, unitType: SymbolicConstant = FORCE, referenceGravityAcceleration: float = 1,
                  referenecePower: float = 0, user: Boolean = OFF, timeSpan: SymbolicConstant = STEP,
                  amplitude: str = ''):
        """This method modifies the PsdDefinition object.
        
        Parameters
        ----------
        unitType
            A SymbolicConstant specifying the type of units for specifying the frequency function. 
            FORCE implies power units. BASE implies gravity used to define base motion. DB implies 
            decibel units. Possible values are FORCE, BASE, and DB. The default value is FORCE. 
        referenceGravityAcceleration
            A Float specifying the reference gravity acceleration. This argument applies when 
            *unitType* = BASE. The default value is 1.0. 
        referenecePower
            A Float specifying the reference power value, in load units squared. This argument 
            applies when *unitType* = DB. The default value is 0.0. 
        user
            A Boolean specifying whether the frequency function is defined in user subroutine UPSD. 
            If specified, then *data* is not applicable, and the *unitType* value must not be DB. 
            The default value is OFF. 
        timeSpan
            A SymbolicConstant specifying the time span of the amplitude. Possible values are STEP 
            and TOTAL. The default value is STEP. 
        amplitude
            A String specifying the name of the amplitude that describes the dynamic event used to 
            define the cross-spectral density frequency function. The default value is an empty 
            string.

        Raises
        ------
        RangeError
        """
        pass
