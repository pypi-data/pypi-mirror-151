from abaqusConstants import *


class Message:
    """The Message object contains information about a given phase of the simulation. Job
    messages are not returned if a script is run without the Abaqus/CAE GUI (using the noGUI 
    option). 

    Attributes
    ----------
    type: SymbolicConstant
        A SymbolicConstant specifying the type of message. Possible values are:
            - ABORTED
            - ANY_JOB
            - ANY_MESSAGE_TYPE
            - COMPLETED
            - END_STEP
            - ERROR
            - HEADING
            - HEALER_JOB
            - HEALER_TYPE
            - INTERRUPTED
            - ITERATION
            - JOB_ABORTED
            - JOB_COMPLETED
            - JOB_INTERRUPTED
            - JOB_SUBMITTED
            - MONITOR_DATA
            - ODB_FILE
            - ODB_FRAME
            - STARTED
            - STATE_FRAME
            - STATUS
            - STEP
            - WARNING
    data: dict
        A :py:class:`~.Dictionary` object specifying the data returned by the analysis product. The value
        depends on the message returned. For a list of the possible entries, see the members of
        DataObject.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import job
        mdb.coexecutions[name].jobs[name].messages[i]
        mdb.jobs[name].messages[i]

    """

    # A SymbolicConstant specifying the type of message. Possible values are: 
    # - ABORTED 
    # - ANY_JOB 
    # - ANY_MESSAGE_TYPE 
    # - COMPLETED 
    # - END_STEP 
    # - ERROR 
    # - HEADING 
    # - HEALER_JOB 
    # - HEALER_TYPE 
    # - INTERRUPTED 
    # - ITERATION 
    # - JOB_ABORTED 
    # - JOB_COMPLETED 
    # - JOB_INTERRUPTED 
    # - JOB_SUBMITTED 
    # - MONITOR_DATA 
    # - ODB_FILE 
    # - ODB_FRAME 
    # - STARTED 
    # - STATE_FRAME 
    # - STATUS 
    # - STEP 
    # - WARNING 
    type: SymbolicConstant = None

    # A Dictionary object specifying the data returned by the analysis product. The value 
    # depends on the message returned. For a list of the possible entries, see the members of 
    # DataObject. 
    data: dict = None
