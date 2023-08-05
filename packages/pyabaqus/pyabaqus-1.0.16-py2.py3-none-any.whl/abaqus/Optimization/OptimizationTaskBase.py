from abaqusConstants import *
from .DesignResponse import DesignResponse
from .GeometricRestriction import GeometricRestriction
from .ObjectiveFunction import ObjectiveFunction
from .OptimizationConstraint import OptimizationConstraint
from .StopCondition import StopCondition


class OptimizationTaskBase:
    """The OptimizationTask object is the abstract base type for other OptimizationTask
    objects. The OptimizationTask object has no explicit constructor. The methods and 
    members of the OptimizationTask object are common to all objects derived from 
    OptimizationTask. 

    Attributes
    ----------
    name: str
        A String specifying the optimization task repository key.
    region: SymbolicConstant
        The SymbolicConstant MODEL or a :py:class:`~abaqus.Region.Region.Region` object specifying the region to which the
        optimization task is applied. The default value is MODEL.
    designResponses: dict[str, DesignResponse]
        A repository of :py:class:`~abaqus.Optimization.DesignResponse.DesignResponse` objects.
    objectiveFunctions: dict[str, ObjectiveFunction]
        A repository of :py:class:`~abaqus.Optimization.ObjectiveFunction.ObjectiveFunction` objects.
    optimizationConstraints: dict[str, OptimizationConstraint]
        A repository of :py:class:`~abaqus.Optimization.OptimizationConstraint.OptimizationConstraint` objects.
    geometricRestrictions: dict[str, GeometricRestriction]
        A repository of :py:class:`~abaqus.Optimization.GeometricRestriction.GeometricRestriction` objects.
    stopConditions: dict[str, StopCondition]
        A repository of :py:class:`~abaqus.Optimization.StopCondition.StopCondition` objects.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import optimization
        mdb.models[name].optimizationTasks[name]

    """

    # A String specifying the optimization task repository key. 
    name: str = ''

    # The SymbolicConstant MODEL or a Region object specifying the region to which the 
    # optimization task is applied. The default value is MODEL. 
    region: SymbolicConstant = MODEL

    # A repository of DesignResponse objects. 
    designResponses: dict[str, DesignResponse] = dict[str, DesignResponse]()

    # A repository of ObjectiveFunction objects. 
    objectiveFunctions: dict[str, ObjectiveFunction] = dict[str, ObjectiveFunction]()

    # A repository of OptimizationConstraint objects. 
    optimizationConstraints: dict[str, OptimizationConstraint] = dict[str, OptimizationConstraint]()

    # A repository of GeometricRestriction objects. 
    geometricRestrictions: dict[str, GeometricRestriction] = dict[str, GeometricRestriction]()

    # A repository of StopCondition objects. 
    stopConditions: dict[str, StopCondition] = dict[str, StopCondition]()
