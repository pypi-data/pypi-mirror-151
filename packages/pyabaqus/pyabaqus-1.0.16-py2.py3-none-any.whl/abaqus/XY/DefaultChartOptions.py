from abaqusConstants import *
from .Area import Area
from .AreaStyle import AreaStyle
from .Axis import Axis
from .Legend import Legend
from .LineStyle import LineStyle
from .TextStyle import TextStyle


class DefaultChartOptions:
    """The DefaultChartOptions object is used to hold on default chart and axis attributes. The
    DefaultChartOptions object attributes are used whenever Chart or Axis are created. A 
    DefaultChartOptions object is automatically created when opening a session. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.defaultChartOptions

    """
    areaStyle: AreaStyle = AreaStyle()

    def setValues(self, areaStyle: AreaStyle = AreaStyle(), aspectRatio: float = None,
                  defaultAxis1Options: Axis = Axis(), defaultAxis2Options: Axis = Axis(),
                  gridArea: Area = Area(), legend: Legend = Legend(),
                  majorAxis1GridStyle: LineStyle = LineStyle(),
                  majorAxis2GridStyle: LineStyle = LineStyle(),
                  minorAxis1GridStyle: LineStyle = LineStyle(),
                  minorAxis2GridStyle: LineStyle = LineStyle(), tagAreaStyle: AreaStyle = AreaStyle(),
                  tagBorder: LineStyle = LineStyle(), tagTextStyle: TextStyle = TextStyle(),
                  useQuantityType: Boolean = ON):
        """This method modifies the DefaultChartOptions object.
        
        Parameters
        ----------
        areaStyle
            An AreaStyle object specifying an AreaStyle used to hold on to the default display 
            properties for the chart area. 
        aspectRatio
            A Float specifying the default aspect ratio of the grid area. A value of -1 specifies 
            that the gridArea will take up all available space. The default value is −1. 
        defaultAxis1Options
            An Axis object specifying an Axis object used to hold on to the default properties for 
            direction 1 axes—the abscissa for a Cartesian chart. 
        defaultAxis2Options
            An Axis object specifying an Axis object used to hold on to the default properties for 
            direction 2 axes—the ordinate for a Cartesian chart. 
        gridArea
            An Area object specifying how to display the grid area by default. 
        legend
            A Legend object specifying the default attributes for the legend of the chart. 
        majorAxis1GridStyle
            A LineStyle object specifying the default line properties to be used when drawing major 
            gridlines along axis 1. 
        majorAxis2GridStyle
            A LineStyle object specifying the default line properties to be used when drawing major 
            gridlines along axis 2. 
        minorAxis1GridStyle
            A LineStyle object specifying the default line properties to be used when drawing minor 
            gridlines along axis 1. 
        minorAxis2GridStyle
            A LineStyle object specifying the default line properties to be used when drawing minor 
            gridlines along axis 2. 
        tagAreaStyle
            An AreaStyle object specifying the default area properties to be used when creating 
            tags. 
        tagBorder
            A LineStyle object specifying the default tag area border properties to be used when 
            creating tags. 
        tagTextStyle
            A TextStyle object specifying the default text properties to be used when creating tags. 
        useQuantityType
            A Boolean specifying whether to use the QuantityType to associate curves with axes. The 
            default value is ON. 
        """
        pass
