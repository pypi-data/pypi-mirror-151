from abaqusConstants import *


class Filter:
    """The Filter object is the abstract base type for other Filter objects. The Filter object
    has no explicit constructor. The methods and members of the Filter object are common to 
    all objects derived from the Filter. 

    Attributes
    ----------
    name: str
        A String specifying the repository key. This name ANTIALIASING is reserved for filters
        generated internally by the program.
    cutoffFrequency: float
        A Float specifying the attenuation point of the filter. Possible values are non-negative
        numbers. Order is not available for OperatorFilter.
    order: int
        An Int specifying the highest power of the filter transfer function. Possible values are
        non-negative numbers less than or equal to 20. Order is not available for
        OperatorFilter. The default value is 2.
    operation: SymbolicConstant
        A SymbolicConstant specifying the filter operator. Possible values are NONE, MIN, MAX,
        and ABS. The default value is NONE.
    halt: Boolean
        A Boolean specifying whether to stop the analysis if the specified limit is reached. The
        default value is OFF.
    limit: float
        None or a Float specifying the threshold limit, an upper or lower bound for output
        values depending on the operation, or a bound for stopping the analysis when Halt is
        used. The default value is None.
    invariant: SymbolicConstant
        A SymbolicConstant specifying the invariant to which filtering is applied. Possible
        values are NONE, FIRST, and SECOND. The default value is NONE.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import filter
        mdb.models[name].filters[name]
        import odbFilter
        session.odbs[name].filters[name]

    """

    # A String specifying the repository key. This name ANTIALIASING is reserved for filters 
    # generated internally by the program. 
    name: str = ''

    # A Float specifying the attenuation point of the filter. Possible values are non-negative 
    # numbers. Order is not available for OperatorFilter. 
    cutoffFrequency: float = None

    # An Int specifying the highest power of the filter transfer function. Possible values are 
    # non-negative numbers less than or equal to 20. Order is not available for 
    # OperatorFilter. The default value is 2. 
    order: int = 2

    # A SymbolicConstant specifying the filter operator. Possible values are NONE, MIN, MAX, 
    # and ABS. The default value is NONE. 
    operation: SymbolicConstant = NONE

    # A Boolean specifying whether to stop the analysis if the specified limit is reached. The 
    # default value is OFF. 
    halt: Boolean = OFF

    # None or a Float specifying the threshold limit, an upper or lower bound for output 
    # values depending on the operation, or a bound for stopping the analysis when Halt is 
    # used. The default value is None. 
    limit: float = None

    # A SymbolicConstant specifying the invariant to which filtering is applied. Possible 
    # values are NONE, FIRST, and SECOND. The default value is NONE. 
    invariant: SymbolicConstant = NONE
