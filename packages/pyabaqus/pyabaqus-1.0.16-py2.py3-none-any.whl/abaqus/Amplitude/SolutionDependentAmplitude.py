from abaqusConstants import *
from .Amplitude import Amplitude


class SolutionDependentAmplitude(Amplitude):
    """The SolutionDependentAmplitude object defines a solution-dependent amplitude for
    superplastic forming analysis. 
    The SolutionDependentAmplitude object is derived from the Amplitude object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import amplitude
        mdb.models[name].amplitudes[name]
        import odbAmplitude
        session.odbs[name].amplitudes[name]

    The corresponding analysis keywords are:

    - AMPLITUDE

    """

    def __init__(self, name: str, initial: float = 1, minimum: float = 0, maximum: float = 1000,
                 timeSpan: SymbolicConstant = STEP):
        """This method creates a SolutionDependentAmplitude object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].SolutionDependentAmplitude
            session.odbs[name].SolutionDependentAmplitude
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        initial
            A Float specifying the initial amplitude value. Possible values are those between 
            *minimum* and *maximum*. The default value is 1.0. 
        minimum
            A Float specifying the minimum amplitude value. Possible values are those smaller than 
            *maximum* and *initial*. The default value is 0.1. 
        maximum
            A Float specifying the maximum amplitude value. Possible values are those larger than 
            *minimum* and *initial*. The default value is 1000.0. 
        timeSpan
            A SymbolicConstant specifying the time span of the amplitude. Possible values are STEP 
            and TOTAL. The default value is STEP. 

        Returns
        -------
            A SolutionDependentAmplitude object. 
            
        Raises
        ------
        InvalidNameError
        RangeError 
        """
        super().__init__()
        pass

    def setValues(self, initial: float = 1, minimum: float = 0, maximum: float = 1000,
                  timeSpan: SymbolicConstant = STEP):
        """This method modifies the SolutionDependentAmplitude object.
        
        Parameters
        ----------
        initial
            A Float specifying the initial amplitude value. Possible values are those between 
            *minimum* and *maximum*. The default value is 1.0. 
        minimum
            A Float specifying the minimum amplitude value. Possible values are those smaller than 
            *maximum* and *initial*. The default value is 0.1. 
        maximum
            A Float specifying the maximum amplitude value. Possible values are those larger than 
            *minimum* and *initial*. The default value is 1000.0. 
        timeSpan
            A SymbolicConstant specifying the time span of the amplitude. Possible values are STEP 
            and TOTAL. The default value is STEP.

        Raises
        ------
        RangeError
        """
        pass
