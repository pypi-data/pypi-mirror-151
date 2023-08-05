import typing

from abaqusConstants import *
from .Amplitude import Amplitude
from .BaselineCorrection import BaselineCorrection


class TabularAmplitude(Amplitude):
    """The TabularAmplitude object defines an amplitude curve as a table of values at
    convenient points on the time scale. 
    The TabularAmplitude object is derived from the Amplitude object. 

    Attributes
    ----------
    baselineCorrection: BaselineCorrection
        A :py:class:`~abaqus.Amplitude.BaselineCorrection.BaselineCorrection` object.

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

    # A BaselineCorrection object. 
    baselineCorrection: BaselineCorrection = BaselineCorrection()

    def __init__(self, name: str, data: tuple, smooth: typing.Union[SymbolicConstant, float] = SOLVER_DEFAULT,
                 timeSpan: SymbolicConstant = STEP):
        """This method creates a TabularAmplitude object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].TabularAmplitude
            session.odbs[name].TabularAmplitude
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        data
            A sequence of pairs of Floats specifying time/frequency and amplitude pairs. Possible 
            values for time/frequency are positive numbers. 
        smooth
            The SymbolicConstant SOLVER_DEFAULT or a Float specifying the degree of smoothing. 
            Possible float values are between 0 and 0.5. If *smooth*=SOLVER_DEFAULT, the default 
            degree of smoothing will be determined by the solver. The default value is 
            SOLVER_DEFAULT. 
        timeSpan
            A SymbolicConstant specifying the time span of the amplitude. Possible values are STEP 
            and TOTAL. The default value is STEP. 

        Returns
        -------
            A TabularAmplitude object. 
            
        Raises
        ------
        InvalidNameError
        RangeError 
        """
        super().__init__()
        pass

    def setValues(self, smooth: typing.Union[SymbolicConstant, float] = SOLVER_DEFAULT,
                  timeSpan: SymbolicConstant = STEP):
        """This method modifies the TabularAmplitude object.
        
        Parameters
        ----------
        smooth
            The SymbolicConstant SOLVER_DEFAULT or a Float specifying the degree of smoothing. 
            Possible float values are between 0 and 0.5. If *smooth*=SOLVER_DEFAULT, the default 
            degree of smoothing will be determined by the solver. The default value is 
            SOLVER_DEFAULT. 
        timeSpan
            A SymbolicConstant specifying the time span of the amplitude. Possible values are STEP 
            and TOTAL. The default value is STEP.

        Raises
        ------
        RangeError
        """
        pass
