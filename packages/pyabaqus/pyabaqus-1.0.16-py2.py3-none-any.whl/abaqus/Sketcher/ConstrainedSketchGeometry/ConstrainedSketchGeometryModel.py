from abaqusConstants import *
from ..ConstrainedSketchBase import ConstrainedSketchBase


class ConstrainedSketchGeometryModel(ConstrainedSketchBase):
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

    def Arc3Points(self, point1: tuple[float], point2: tuple[float], point3: tuple[float]):
        """This method constructs an arc using a two endpoints and an intermediate third point on
        the arc.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].Arc3Points
        
        Parameters
        ----------
        point1
            A pair of Floats specifying the first endpoint of the arc.
        point2
            A pair of Floats specifying the second endpoint of the arc.
        point3
            A pair of Floats specifying the third point on the arc.

        Returns
        -------
        geometry: ConstrainedSketchGeometry
            A ConstrainedSketchGeometry object
        """
        pass

    def ArcByCenterEnds(self, center: tuple[float], point1: tuple[float], point2: tuple[float],
                        direction: SymbolicConstant):
        """This method constructs an arc using a center point and two vertices. The Arc object is
        added to the geometry repository of the ConstrainedSketch object. The arc is created in
        a clockwise fashion from *point1* to *point2*.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].ArcByCenterEnds
        
        Parameters
        ----------
        center
            A pair of Floats specifying the center point of the arc.
        point1
            A pair of Floats specifying the first endpoint of the arc.
        point2
            A pair of Floats specifying the second endpoint of the arc.
        direction
            A SymbolicConstant specifying the direction of the arc. Possible values are CLOCKWISE
            and COUNTERCLOCKWISE.

        Returns
        -------
        geometry: ConstrainedSketchGeometry
            A ConstrainedSketchGeometry object

        Raises
        ------
            If incompatible data are given, the second endpoint is ignored
        """
        pass

    def ArcByStartEndTangent(self, point1: tuple[float], point2: tuple[float], vector: tuple):
        """This method constructs an arc using two vertices. The Arc object is added to the
        geometry repository of the ConstrainedSketch object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].ArcByStartEndTangent
        
        Parameters
        ----------
        point1
            A pair of Floats specifying the first endpoint of the arc.
        point2
            A pair of Floats specifying the second endpoint of the arc.
        vector
            A sequence of two Floats specifying the start direction for constructing the arc.

        Returns
        -------
        geometry: ConstrainedSketchGeometry
            A ConstrainedSketchGeometry object
        """
        pass

    def CircleByCenterPerimeter(self, center: tuple[float], point1: tuple[float]):
        """This method constructs a circle using a center point and a point on the perimeter. The
        circle is added to the geometry repository of the ConstrainedSketch object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].CircleByCenterPerimeter
        
        Parameters
        ----------
        center
            A pair of Floats specifying the center point of the circle.
        point1
            A pair of Floats specifying a point on the perimeter of the circle.

        Returns
        -------
        geometry: ConstrainedSketchGeometry
            A ConstrainedSketchGeometry object
        """
        pass

    def ConstructionCircleByCenterPerimeter(self, center: tuple[float], point1: tuple[float]):
        """This method constructs a construction circle using a center point and a point on the
        perimeter. The circle is added to the geometry repository of the ConstrainedSketch
        object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].ConstructionCircleByCenterPerimeter
        
        Parameters
        ----------
        center
            A pair of Floats specifying the center point of the construction circle.
        point1
            A pair of Floats specifying a point on the perimeter of the construction circle.

        Returns
        -------
        geometry: ConstrainedSketchGeometry
            A ConstrainedSketchGeometry object
        """
        pass

    def EllipseByCenterPerimeter(self, center: tuple[float], axisPoint1: tuple[float], axisPoint2: tuple[float]):
        """This method constructs an ellipse using a center point, a major axis point, and a minor
        axis point. The ellipse is added to the geometry repository of the ConstrainedSketch
        object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].EllipseByCenterPerimeter
        
        Parameters
        ----------
        center
            A pair of Floats specifying the center point of the ellipse.
        axisPoint1
            A pair of Floats specifying the major or minor axis point of the ellipse.
        axisPoint2
            A pair of Floats specifying the minor or major axis point of the ellipse.

        Returns
        -------
        geometry: ConstrainedSketchGeometry
            A ConstrainedSketchGeometry object
        """
        pass

    def FilletByRadius(self, radius: float, curve1: 'ConstrainedSketchGeometryModel', nearPoint1: tuple[float],
                       curve2: 'ConstrainedSketchGeometryModel', nearPoint2: tuple[float]):
        """This method constructs a fillet arc of a given radius between two curves. The fillet is
        added to the geometry repository of the ConstrainedSketch object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].FilletByRadius
        
        Parameters
        ----------
        radius
            A Float specifying the radius of the fillet arc. Possible values are Floats > 0.
        curve1
            A ConstrainedSketchGeometry object specifying the first curve.
        nearPoint1
            A pair of Floats specifying a point on the sketch near where the user wishes the fillet
            to intersect with *curve1*. This point does not need to be on*curve1*; it is used as a
            hint to draw the fillet.
        curve2
            A ConstrainedSketchGeometry object specifying the second curve.
        nearPoint2
            A pair of Floats specifying a point on the sketch near where the user wishes the fillet
            to intersect with *curve2*. This point does not need to be on *curve2*; it is used as a
            hint to draw the fillet.

        Returns
        -------
        geometry: ConstrainedSketchGeometry
            A ConstrainedSketchGeometry object

        Raises
        ------
            - If the radius given cannot be used to create a fillet between the two curves given:
              Range Error: cannot construct the Fillet specified
        """
        pass

    def Line(self, point1: tuple[float], point2: tuple[float]):
        """This method creates a line between two given points.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].Line
        
        Parameters
        ----------
        point1
            A pair of Floats specifying the first endpoint.
        point2
            A pair of Floats specifying the second endpoint.

        Returns
        -------
        geometry: ConstrainedSketchGeometry
            A ConstrainedSketchGeometry object
        """
        pass

    def ConstructionLine(self, point1: tuple[float], point2: tuple[float]):
        """This method creates an oblique construction line that runs between two given points.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].ConstructionLine
        
        Parameters
        ----------
        point1
            A pair of Floats specifying the first endpoint.
        point2
            A pair of Floats specifying the second endpoint.

        Returns
        -------
        geometry: ConstrainedSketchGeometry
            A ConstrainedSketchGeometry object
        """
        pass

    def Spline(self, points: tuple, constrainPoints: Boolean = True):
        """This method creates a spline curve running through a sequence of points.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].Spline
        
        Parameters
        ----------
        points
            A sequence of pairs of Floats specifying the points through which the spline passes.
        constrainPoints
            A Boolean that determines whether the points given are to constrained to always remain
            on the Spline. The default is True. For a large sequence of *points*, significant
            performance gains may be achieved by setting the value to False.

        Returns
        -------
        geometry: ConstrainedSketchGeometry
            A ConstrainedSketchGeometry object
        """
        pass

    def Spot(self, point: tuple[float]):
        """This method creates a spot construction point located at the specified coordinates. The
        spot is added to the vertex repository of the ConstrainedSketch object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].sketches[name].Spot
        
        Parameters
        ----------
        point
            A pair of Floats specifying the coordinates of the spot construction point.

        Returns
        -------
        geometry: ConstrainedSketchGeometry
            A ConstrainedSketchGeometry object
        """
        pass

    def getVertices(self):
        """This method returns an list of ConstrainedSketchVertex objects which are a part of the
        given ConstrainedSketchGeometry object.

        Returns
        -------
        vertices: list[ConstrainedSketchVertex]
            A list of ConstrainedSketchVertex objects
        """
        pass

    def getSize(self):
        """This method returns the length of the given ConstrainedSketchGeometry object.

        Returns
        -------
        length: int
            The length of the given ConstrainedSketchGeometry
        """
        pass

    def getPointAtDistance(self, point: tuple[float], distance: str, percentage: Boolean = OFF):
        """This method returns a point offset along the given ConstrainedSketchGeometry from the
        given end by a specified arc length distance or a percentage of the total length of the
        ConstrainedSketchGeometry object.
        
        Parameters
        ----------
        point
            A pair of Floats specifying the point from which the distance is to be measured.
        distance
            A float specifying the arc length distance along the ConstrainedSketchGeometry from the
            *point* at which the required point is situated.
        percentage
            A Boolean that specifies if the *distance* is an absolute distance or is a fraction
            relative to the length of the ConstrainedSketchGeometry object.

        Returns
        -------
        points: tuple[float]
            A pair of floats representing the point along the edge
        """
        pass
