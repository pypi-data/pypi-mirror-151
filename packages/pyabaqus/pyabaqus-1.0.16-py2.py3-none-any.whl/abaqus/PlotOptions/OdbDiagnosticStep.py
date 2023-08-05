from abaqusConstants import *
from .OdbContactDiagnostics import OdbContactDiagnostics
from .OdbDiagnosticIncrement import OdbDiagnosticIncrement


class OdbDiagnosticStep:
    """The OdbDiagnosticStep object stores step data.

    Attributes
    ----------
    activeXplStatus: tuple
        A Tuple of the status values. This attribute is read-only.
    characteristicElementLength: str
        A float specifying the characteristic element length for the step. This attribute is
        read-only.
    contactDiagnostics: dict[str, OdbContactDiagnostics]
        A repository of :py:class:`~abaqus.PlotOptions.OdbContactDiagnostics.OdbContactDiagnostics` objects.
    explicitIncrementStatus: tuple
        A sequence of string specifying the explicit increment status. This attribute is
        read-only.
    extrapolation: str
        A String specifying the method (Linear or logarithmic) used for extrapolation. This
        attribute is read-only.
    incrementationScheme: str
        A String specifying the method of incrementation (Auto or fixed). This attribute is
        read-only.
    incrementsCompleted: str
        An int specifying the number of completed increments. This attribute is read-only.
    increments: dict[str, OdbDiagnosticIncrement]
        A repository of :py:class:`~abaqus.PlotOptions.OdbDiagnosticIncrement.OdbDiagnosticIncrement` objects.
    initialTimeIncrement: str
        A float specifying the initial increment size for the step. This attribute is read-only.
    isNlgeom: Boolean
        A boolean specifying whether or not the effects of geometric nonlinearities are
        considered. This attribute is read-only.
    isPerturbation: Boolean
        A boolean specifying whether or not the step is a perturbation step. This attribute is
        read-only.
    isStabilized: Boolean
        A boolean specifying whether or not stabilization for the system in any form is
        considered. This attribute is read-only.
    isRiks: Boolean
        A boolean specifying whether the step is static riks. This attribute is read-only.
    isUnsymm: Boolean
        A boolean specifying whether the matrix storage is unsymmetric. This attribute is
        read-only.
    matrixSolver: str
        A string specifying the method of solving (Direct or Iterative). This attribute is
        read-only.
    maximumNumberOfIncrements: str
        An int specifying the maximum number of allowed increments in the step. This attribute
        is read-only.
    maximumTimeIncrement: str
        A float specifying the size of the allowed maximum time increment in the step. This
        attribute is read-only.
    minimumTimeIncrement: str
        A float specifying the size of the allowed minimum time increment in the step. This
        attribute is read-only.
    name: str
        A string specifying the name of the step. This attribute is read-only.
    number: str
        An int specifying the step number. This attribute is read-only.
    numberOfContactDiagnostics: str
        An int specifying the number of contact diagnostics encountered. This attribute is
        read-only.
    numberOfIncrements: str
        An int specifying the number of increments taken in the step to complete the solution.
        This attribute is read-only.
    numberOfXplStatus: str
        An int specifying the number of the explicit status. This attribute is read-only.
    stabilizeFactor: str
        A float specifying the stabilize factor. This attribute is read-only.
    stepTimeCompleted: str
        A float specifying the time taken for the completion of the step. This attribute is
        read-only.
    timePeriod: str
        A float specifying the duration for the step. This attribute is read-only.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.odbData[name].diagnosticData.steps[i]

    """

    # A Tuple of the status values. This attribute is read-only. 
    activeXplStatus: tuple = ()

    # A float specifying the characteristic element length for the step. This attribute is 
    # read-only. 
    characteristicElementLength: str = ''

    # A repository of OdbContactDiagnostics objects. 
    contactDiagnostics: dict[str, OdbContactDiagnostics] = dict[str, OdbContactDiagnostics]()

    # A sequence of string specifying the explicit increment status. This attribute is 
    # read-only. 
    explicitIncrementStatus: tuple = ()

    # A String specifying the method (Linear or logarithmic) used for extrapolation. This 
    # attribute is read-only. 
    extrapolation: str = ''

    # A String specifying the method of incrementation (Auto or fixed). This attribute is 
    # read-only. 
    incrementationScheme: str = ''

    # An int specifying the number of completed increments. This attribute is read-only. 
    incrementsCompleted: str = ''

    # A repository of OdbDiagnosticIncrement objects. 
    increments: dict[str, OdbDiagnosticIncrement] = dict[str, OdbDiagnosticIncrement]()

    # A float specifying the initial increment size for the step. This attribute is read-only. 
    initialTimeIncrement: str = ''

    # A boolean specifying whether or not the effects of geometric nonlinearities are 
    # considered. This attribute is read-only. 
    isNlgeom: Boolean = OFF

    # A boolean specifying whether or not the step is a perturbation step. This attribute is 
    # read-only. 
    isPerturbation: Boolean = OFF

    # A boolean specifying whether or not stabilization for the system in any form is 
    # considered. This attribute is read-only. 
    isStabilized: Boolean = OFF

    # A boolean specifying whether the step is static riks. This attribute is read-only. 
    isRiks: Boolean = OFF

    # A boolean specifying whether the matrix storage is unsymmetric. This attribute is 
    # read-only. 
    isUnsymm: Boolean = OFF

    # A string specifying the method of solving (Direct or Iterative). This attribute is 
    # read-only. 
    matrixSolver: str = ''

    # An int specifying the maximum number of allowed increments in the step. This attribute 
    # is read-only. 
    maximumNumberOfIncrements: str = ''

    # A float specifying the size of the allowed maximum time increment in the step. This 
    # attribute is read-only. 
    maximumTimeIncrement: str = ''

    # A float specifying the size of the allowed minimum time increment in the step. This 
    # attribute is read-only. 
    minimumTimeIncrement: str = ''

    # A string specifying the name of the step. This attribute is read-only. 
    name: str = ''

    # An int specifying the step number. This attribute is read-only. 
    number: str = ''

    # An int specifying the number of contact diagnostics encountered. This attribute is 
    # read-only. 
    numberOfContactDiagnostics: str = ''

    # An int specifying the number of increments taken in the step to complete the solution. 
    # This attribute is read-only. 
    numberOfIncrements: str = ''

    # An int specifying the number of the explicit status. This attribute is read-only. 
    numberOfXplStatus: str = ''

    # A float specifying the stabilize factor. This attribute is read-only. 
    stabilizeFactor: str = ''

    # A float specifying the time taken for the completion of the step. This attribute is 
    # read-only. 
    stepTimeCompleted: str = ''

    # A float specifying the duration for the step. This attribute is read-only. 
    timePeriod: str = ''

    def extractData(self, incrementStatistics: str):
        """This method creates a temporary XYData object, with increments on the x-axis and
        requested output on the y-axis.
        
        Parameters
        ----------
        incrementStatistics
            An enum specifying the requested output variable for the data table. Possible enum 
            values are NUM_ATTEMPTS (the number of attempts), NUM_SDI (the number of severe 
            discontinuity iterations), NUM_EQI (the number of equivalent iterations), NUM_ITERS (the 
            number of iterations), STEP_TIME (the cumulative step time until that increment) or 
            INC_SIZE (the step time for each increment). 
        """
        pass
