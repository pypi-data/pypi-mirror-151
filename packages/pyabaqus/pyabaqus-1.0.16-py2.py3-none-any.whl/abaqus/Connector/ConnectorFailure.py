from abaqusConstants import *
from .ConnectorBehaviorOption import ConnectorBehaviorOption


class ConnectorFailure(ConnectorBehaviorOption):
    """The ConnectorFailure object defines failure criteria for one or more components of a
    connector's relative motion. 
    The ConnectorFailure object is derived from the ConnectorBehaviorOption object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import section
        mdb.models[name].sections[name].behaviorOptions[i]
        import odbSection
        session.odbs[name].sections[name].behaviorOptions[i]

    The corresponding analysis keywords are:

    - CONNECTOR FAILURE

    """

    def __init__(self, releaseComponent: SymbolicConstant = ALL, minMotion: float = None,
                 maxMotion: float = None, minForce: float = None, maxForce: float = None,
                 components: tuple = ()):
        """This method creates a connector failure behavior option for a ConnectorSection object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

                      import connectorBehavior
                      connectorBehavior.ConnectorFailure
                      import odbConnectorBehavior
                      odbConnectorBehavior.ConnectorFailure
        
        Parameters
        ----------
        releaseComponent
            The SymbolicConstant ALL or an Int specifying the motion components that fail. If an Int 
            is specified, only that motion component fails when the failure criteria are satisfied. 
            If *releaseComponent*=ALL, all motion components fail. The default value is ALL. 
        minMotion
            None or a Float specifying the lower bound for the connector's relative position for all 
            specified components, or no lower bound. The default value is None. 
        maxMotion
            None or a Float specifying the upper bound for the connector's relative position for all 
            specified components, or no upper bound. The default value is None. 
        minForce
            None or a Float specifying the lower bound of the force or moment in the directions of 
            the specified components at which locking occurs, or no lower bound. The default value 
            is None. 
        maxForce
            None or a Float specifying the upper bound of the force or moment in the directions of 
            the specified components at which locking occurs, or no upper bound. The default value 
            is None. 
        components
            A sequence of Ints specifying the components of relative motion for which the behavior 
            is defined. Possible values are 1 ≤≤ *components* ≤≤ 6. Only available components can be 
            specified. The default value is an empty sequence. 

        Returns
        -------
            A ConnectorFailure object. 

        Raises
        ------
            ValueError and TextError. 
        """
        super().__init__()
        pass

    def setValues(self):
        """This method modifies the ConnectorFailure object.

        Raises
        ------
            ValueError. 
        """
        pass
