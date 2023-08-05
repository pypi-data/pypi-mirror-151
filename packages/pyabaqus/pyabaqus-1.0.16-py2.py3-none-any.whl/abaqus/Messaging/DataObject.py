from abaqusConstants import *


class DataObject:
    """An instance of the DataObject object is passed to each callback. The DataObject object
    has no methods. The members of a DataObject object depend on the type of the object. All 
    DataObject instances have the following members, regardless of type: 

    Attributes
    ----------
    phase: SymbolicConstant
        A SymbolicConstant specifying the phase of the analysis. Possible values are
        BATCHPRE_PHASE, PACKAGER_PHASE, STANDARD_PHASE, EXPLICIT_PHASE, CALCULATOR_PHASE, and
        UNKNOWN_PHASE.
    processId: int
        An Int specifying the process ID of the analysis product.
    threadId: int
        An Int specifying the thread ID of the analysis product. Threads are used for parallel
        or multiprocessing; in most cases **threadId** is set to zero.
    timeStamp: int
        An Int specifying the time the message was sent in seconds since 00:00:00 UTC, January
        1, 1970.
    attempts: int
        An Int specifying the number of attempts made to reach equilibrium during this step.
    dof: int
        An Int specifying the degree of freedom requested for monitoring the output.
    equilibrium: int
        An Int specifying the number of equilibrium iterations made during this increment.
    increment: int
        An Int specifying the increment of the analysis.
    iterations: int
        An Int specifying the number of iterations in the step.
    node: int
        An Int specifying the node number requested for monitoring output.
    severe: int
        An Int specifying the number of severe discontinuity iterations completed during this
        increment.
    step: int
        An Int specifying the current step number. Step number 1 corresponds to the first step.
    stepId: int
        An Int specifying the ID of the step.
    stepTime: float
        A Float specifying the step time corresponding to the current increment.
    time: float
        A Float specifying the total time corresponding to the monitor data.
    timeIncrement: float
        A Float specifying the time increment used in the current step.
    totalTime: float
        A Float specifying the total time completed in the analysis.
    value: float
        A Float specifying the current value of the degree of freedom requested for monitoring.
    clientHost: str
        A String specifying the host name of the machine that is running the analysis.
    clientName: str
        A String specifying the name of the client that responded to the callback function.
        Possible values are BatchPre, Packager, Standard, Explicit, and Calculator.
    file: str
        A String specifying the full path of the output database.
    heading: str
        A String specifying the job heading.
    message: str
        A String specifying the job heading.
    nset: str
        A String specifying the node set specified for monitoring output.
    stepName: str
        A String specifying the name of the step.

    Notes
    -----
    This object can be accessed by:     

    """

    # A SymbolicConstant specifying the phase of the analysis. Possible values are 
    # BATCHPRE_PHASE, PACKAGER_PHASE, STANDARD_PHASE, EXPLICIT_PHASE, CALCULATOR_PHASE, and 
    # UNKNOWN_PHASE. 
    phase: SymbolicConstant = None

    # An Int specifying the process ID of the analysis product. 
    processId: int = None

    # An Int specifying the thread ID of the analysis product. Threads are used for parallel 
    # or multiprocessing; in most cases *threadId* is set to zero. 
    threadId: int = None

    # An Int specifying the time the message was sent in seconds since 00:00:00 UTC, January 
    # 1, 1970. 
    timeStamp: int = None

    # An Int specifying the number of attempts made to reach equilibrium during this step. 
    attempts: int = None

    # An Int specifying the degree of freedom requested for monitoring the output. 
    dof: int = None

    # An Int specifying the number of equilibrium iterations made during this increment. 
    equilibrium: int = None

    # An Int specifying the increment of the analysis. 
    increment: int = None

    # An Int specifying the number of iterations in the step. 
    iterations: int = None

    # An Int specifying the node number requested for monitoring output. 
    node: int = None

    # An Int specifying the number of severe discontinuity iterations completed during this 
    # increment. 
    severe: int = None

    # An Int specifying the current step number. Step number 1 corresponds to the first step. 
    step: int = None

    # An Int specifying the ID of the step. 
    stepId: int = None

    # A Float specifying the step time corresponding to the current increment. 
    stepTime: float = None

    # A Float specifying the total time corresponding to the monitor data. 
    time: float = None

    # A Float specifying the time increment used in the current step. 
    timeIncrement: float = None

    # A Float specifying the total time completed in the analysis. 
    totalTime: float = None

    # A Float specifying the current value of the degree of freedom requested for monitoring. 
    value: float = None

    # A String specifying the host name of the machine that is running the analysis. 
    clientHost: str = ''

    # A String specifying the name of the client that responded to the callback function. 
    # Possible values are BatchPre, Packager, Standard, Explicit, and Calculator. 
    clientName: str = ''

    # A String specifying the full path of the output database. 
    file: str = ''

    # A String specifying the job heading. 
    heading: str = ''

    # A String specifying the job heading. 
    message: str = ''

    # A String specifying the node set specified for monitoring output. 
    nset: str = ''

    # A String specifying the name of the step. 
    stepName: str = ''
