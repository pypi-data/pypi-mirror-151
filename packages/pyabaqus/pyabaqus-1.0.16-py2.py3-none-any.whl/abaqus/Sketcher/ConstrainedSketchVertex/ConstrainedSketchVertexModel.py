from ..ConstrainedSketchBase import ConstrainedSketchBase


class ConstrainedSketchVertexModel(ConstrainedSketchBase):
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

    def Spot(self, point: tuple[float]):
        """This method creates a spot (construction point) located at the specified coordinates.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].Spot
        
        Parameters
        ----------
        point
            A pair of Floats specifying the coordinates of the construction point.

        Returns
        -------
        vertex: ConstrainedSketchVertex
            A ConstrainedSketchVertex object (None if the spot cannot be created)
        """
        pass
