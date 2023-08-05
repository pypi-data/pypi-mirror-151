from ..ConstrainedSketchBase import ConstrainedSketchBase


class ConstrainedSketchParameterModel(ConstrainedSketchBase):
    """A ConstrainedSketch object contains the entities that are used to create a sketch. The
    objects include ConstrainedSketchGeometry objects contained in the ConstrainedSketchGeometry Repository,
    such as Line, Arc, and Spline. ConstrainedSketchVertex, ConstrainedSketchDimension, ConstrainedSketchConstraint, and ConstrainedSketchParameter objects are
    contained in their respective repositories. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import sketch
        mdb.models[name].sketches[name]

    """

    def ConstrainedSketchParameter(self, name: str, path: str = '', expression: str = '', previousParameter: str = ''):
        """This method creates a parameter and optionally associates a dimension with this
        parameter.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].ConstrainedSketchParameter
        
        Parameters
        ----------
        name
            A String specifying the name of the ConstrainedSketchParameter object. No two parameters
            in the same ConstrainedSketch can have the same name.
        path
            A String specifying the ConstrainedSketchDimension object with which this parameter is
            associated.
        expression
            A String specifying the expression or value associated with the
            ConstrainedSketchParameter.
        previousParameter
            A String specifying the name of the previous ConstrainedSketchParameter, if it exists.
            The *previousParameter* argument implies an order among the parameters. No two
            parameters can reference the same parameter as the previous parameter.

        Returns
        -------
        obj: ConstrainedSketchParameter
            A ConstrainedSketchParameter object
        """
        pass
