from abaqusConstants import *
from .AxisData import AxisData
from .LineStyle import LineStyle
from .TextStyle import TextStyle


class Axis:
    """The Axis object is used to store the display attributes of axes. Axes objects are
    automatically created when adding XYCurve objects to a Chart object. 

    Attributes
    ----------
    labelFrequency: int
        An Int specifying the frequency of the labels with respect to the tick marks. The
        default value is 1.
    tickLength: float
        A Float specifying the length of the ticks in mm. The default value is 2.0.
    placement: SymbolicConstant
        A SymbolicConstant specifying the placement of the axis on the grid. Possible values
        are:MIN_EDGE, specifying that the axis is placed at the minimum edge - for an abscissa
        at the bottom, for an ordinate to the left.MAX_EDGE, specifying that the axis is placed
        at the maximum edge - for an abscissa at the top, for an ordinate at the
        right.MIN_MAX_EDGE, specifying that the axis is placed at the minimum edge - for an
        abscissa at the bottom, for an ordinate to the left - and repeated without labels and
        title at the maximum edge.CENTER, specifying that the axis is placed at the center of
        the grid.The default value is MIN_MAX_EDGE.
    tickPlacement: SymbolicConstant
        A SymbolicConstant specifying how tick marks are placed on the axis. Possible values
        are:NONE, specifying that no tick marks are displayed.INSIDE, specifying that the tick
        marcks are placed on the inside of the axis.OUTSIDE, specifying that the tick marcks are
        placed on the outside of the axis.ACROSS, specifying that the tick marcks are placed
        across the axis.The default value is INSIDE.
    labelPlacement: SymbolicConstant
        A SymbolicConstant specifying how labels are placed on the axis. Possible values
        are:NONE, specifying that no labels are displayed.INSIDE, specifying that the labels are
        placed on the inside of the axis.OUTSIDE, specifying that the labels are placed on the
        outside of the axis.The default value is INSIDE.
    axisData: AxisData
        An :py:class:`~abaqus.XY.AxisData.AxisData` object specifying the numerical data of the axis.
    lineStyle: LineStyle
        A :py:class:`~abaqus.XY.LineStyle.LineStyle` object specifying the line properties used to display the axis.
    labelStyle: TextStyle
        A :py:class:`~abaqus.XY.TextStyle.TextStyle` object specifying the text properties to be used when displaying axis
        labels.
    titleStyle: TextStyle
        A :py:class:`~abaqus.XY.TextStyle.TextStyle` object specifying the text properties to be used when displaying the axis
        title.
    tickStyle: LineStyle
        A :py:class:`~abaqus.XY.LineStyle.LineStyle` object specifying the line properties to be used when displaying axis ticks.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.charts[name].axes1[i]
        session.charts[name].axes2[i]
        session.defaultChartOptions.defaultAxis1Options
        session.defaultChartOptions.defaultAxis2Options
        session.xyPlots[name].charts[name].axes1[i]
        session.xyPlots[name].charts[name].axes2[i]

    """

    # An Int specifying the frequency of the labels with respect to the tick marks. The 
    # default value is 1. 
    labelFrequency: int = 1

    # A Float specifying the length of the ticks in mm. The default value is 2.0. 
    tickLength: float = 2

    # A SymbolicConstant specifying the placement of the axis on the grid. Possible values 
    # are:MIN_EDGE, specifying that the axis is placed at the minimum edge - for an abscissa 
    # at the bottom, for an ordinate to the left.MAX_EDGE, specifying that the axis is placed 
    # at the maximum edge - for an abscissa at the top, for an ordinate at the 
    # right.MIN_MAX_EDGE, specifying that the axis is placed at the minimum edge - for an 
    # abscissa at the bottom, for an ordinate to the left - and repeated without labels and 
    # title at the maximum edge.CENTER, specifying that the axis is placed at the center of 
    # the grid.The default value is MIN_MAX_EDGE. 
    placement: SymbolicConstant = MIN_MAX_EDGE

    # A SymbolicConstant specifying how tick marks are placed on the axis. Possible values 
    # are:NONE, specifying that no tick marks are displayed.INSIDE, specifying that the tick 
    # marcks are placed on the inside of the axis.OUTSIDE, specifying that the tick marcks are 
    # placed on the outside of the axis.ACROSS, specifying that the tick marcks are placed 
    # across the axis.The default value is INSIDE. 
    tickPlacement: SymbolicConstant = INSIDE

    # A SymbolicConstant specifying how labels are placed on the axis. Possible values 
    # are:NONE, specifying that no labels are displayed.INSIDE, specifying that the labels are 
    # placed on the inside of the axis.OUTSIDE, specifying that the labels are placed on the 
    # outside of the axis.The default value is INSIDE. 
    labelPlacement: SymbolicConstant = INSIDE

    # An AxisData object specifying the numerical data of the axis. 
    axisData: AxisData = AxisData()

    # A LineStyle object specifying the line properties used to display the axis. 
    lineStyle: LineStyle = LineStyle()

    # A TextStyle object specifying the text properties to be used when displaying axis 
    # labels. 
    labelStyle: TextStyle = TextStyle()

    # A TextStyle object specifying the text properties to be used when displaying the axis 
    # title. 
    titleStyle: TextStyle = TextStyle()

    # A LineStyle object specifying the line properties to be used when displaying axis ticks. 
    tickStyle: LineStyle = LineStyle()

    def setValues(self, axis: 'Axis' = None, labelFrequency: int = 1,
                  labelPlacement: SymbolicConstant = INSIDE, labelStyle: TextStyle = TextStyle(),
                  lineStyle: LineStyle = LineStyle(), placement: SymbolicConstant = MIN_MAX_EDGE,
                  tickLength: float = 2, tickPlacement: SymbolicConstant = INSIDE,
                  tickStyle: LineStyle = LineStyle(), titleStyle: TextStyle = TextStyle()):
        """This method modifies the Axis object.
        
        Parameters
        ----------
        axis
            An Axis object from which attributes are to be copied. 
        labelFrequency
            An Int specifying the frequency of the labels with respect to the tick marks. The 
            default value is 1. 
        labelPlacement
            A SymbolicConstant specifying how labels are placed on the axis. Possible values 
            are:NONE, specifying that no labels are displayed.INSIDE, specifying that the labels are 
            placed on the inside of the axis.OUTSIDE, specifying that the labels are placed on the 
            outside of the axis.The default value is INSIDE. 
        labelStyle
            A TextStyle object specifying the text properties to be used when displaying axis 
            labels. 
        lineStyle
            A LineStyle object specifying the line properties used to display the axis. 
        placement
            A SymbolicConstant specifying the placement of the axis on the grid. Possible values 
            are:MIN_EDGE, specifying that the axis is placed at the minimum edge - for an abscissa 
            at the bottom, for an ordinate to the left.MAX_EDGE, specifying that the axis is placed 
            at the maximum edge - for an abscissa at the top, for an ordinate at the 
            right.MIN_MAX_EDGE, specifying that the axis is placed at the minimum edge - for an 
            abscissa at the bottom, for an ordinate to the left - and repeated without labels and 
            title at the maximum edge.CENTER, specifying that the axis is placed at the center of 
            the grid.The default value is MIN_MAX_EDGE. 
        tickLength
            A Float specifying the length of the ticks in mm. The default value is 2.0. 
        tickPlacement
            A SymbolicConstant specifying how tick marks are placed on the axis. Possible values 
            are:NONE, specifying that no tick marks are displayed.INSIDE, specifying that the tick 
            marcks are placed on the inside of the axis.OUTSIDE, specifying that the tick marcks are 
            placed on the outside of the axis.ACROSS, specifying that the tick marcks are placed 
            across the axis.The default value is INSIDE. 
        tickStyle
            A LineStyle object specifying the line properties to be used when displaying axis ticks. 
        titleStyle
            A TextStyle object specifying the text properties to be used when displaying the axis 
            title. 
        """
        pass
