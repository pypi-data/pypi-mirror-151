from abaqusConstants import *
from .QuantityType import QuantityType
from .XYCurveArray import XYCurveArray


class AxisData:
    """The AxisData object is used to store the data attributes of axes. An AxisData object is
    automatically created when creating an Axis object. 

    Attributes
    ----------
    dbReference: float
        A Float specifying the reference value for decibel computation. The default value is
        1.0.
    direction: SymbolicConstant
        A SymbolicConstant specifying the direction of the axis. Possible values are ABSCISSA
        and ORDINATE.
    labelFormat: SymbolicConstant
        A SymbolicConstant specifying how tick labels are formatted. Possible values are
        AUTOMATIC, DECIMAL, SCIENTIFIC, and ENGINEERING. The default value is AUTOMATIC.
    labelNumDigits: int
        An Int specifying the number of significant digits displayed for the labels. Possible
        values are 1 to 7. The default value is 2.
    maxAutoCompute: Boolean
        A Boolean specifying whether or not to use the automatically computed maximum value for
        the axis. The default value is ON.
    maxAutoValue: float
        A Float specifying the maximum value when **maxAutoCompute** is true.
    maxValue: float
        A Float specifying the maximum value when **maxAutoCompute** is false. By default,
        **maxValue** is set to **maxAutoValue**.
    maxShownValue: float
        A Float specifying the current maximum value displayed for this axis. This value is
        different from **maxAutoValue** or **maxValue** when the axis is being transformed (zoom or
        pan).
    minAutoCompute: Boolean
        A Boolean specifying whether or not to use the automatically computed minimum value for
        the axis. The default value is ON.
    minAutoValue: float
        A Float specifying the minimum value when **minAutoCompute** is true.
    minValue: float
        A Float specifying the minimum value when **minAutoCompute** is false. By default,
        **minValue** is set to **minAutoValue**.
    minShownValue: float
        A Float specifying the current minimum value displayed for this axis. This value is
        different from **minAutoValue** or **minValue** when the axis is being transformed (zoom or
        pan).
    minorTickCount: int
        An Int specifying the number the number of minor tick marks between major ticks.
        Possible values are 0 ≤≤ **minorTickCount** ≤≤ 20. When the **scale** is set to LOG, the
        minorTickCount is interpreted as the number of ticks per decade and limited to 0, 1, 4,
        8, and 17. The default value is 1.
    scale: SymbolicConstant
        A SymbolicConstant specifying the type of scale to use for the axis. Possible values
        are:LINEAR, specifying tickmarks and labels are linearly distributed.LOG, specifying
        tickmarks and labels are logarithmically distributed.DB, specifying tickmarks and labels
        are distributed on a decibel scale.DB2, specifying tickmarks and labels are distributed
        on a 2*decibel scale.The default value is LINEAR.
    tickMode: SymbolicConstant
        A SymbolicConstant specifying the type of scale to use for the axis. Possible values
        are:AUTOCOMPUTE, specifying tickmarks and labels are automatically computed.INCREMENT,
        specifying tickmarks and labels are defined by a given increment.TOTAL_NUMBER,
        specifying tickmarks and labels are defined by the total number of ticks.The default
        value is AUTOCOMPUTE.
    tickCount: int
        An Int specifying the number of major tick marks on the axis when **tickMode**
        =TOTAL_NUMBER. Possible values are 0 ≤≤ **tickCount** ≤≤ 30. The default value is computed
        based on the range of the axis. When the **scale** is set to LOG, the tickCount is
        interpreted as the number of ticks per decade and acceptable values are 1, 4, 8, and 17.
    tickCountShown: int
        An Int specifying the number of major ticks effectively shown. This value takes zoom,
        pan and rounding into account.
    tickIncrement: float
        A Float specifying the increment of the major tick marks on the axis when **tickMode** =
        INCREMENT. Valid values are 0 << **tickIncrement**. The default value is computed based on
        the results of the automatic method and the range being plotted. When the **scale** is set
        to LOG, the tickIncrement is interpreted as a value per decade and should be between
        0.05 and 1.
    tickIncrementShown: float
        A Float specifying the shown tick increment of the major ticks. This value takes
        zoom/pan into account.
    useSystemTitle: Boolean
        A Boolean specifying whether the title to use for the axis title is system defined or
        user defined. The default value is ON.
    curves: XYCurveArray
        An :py:class:`~abaqus.XY.XY:py:class:`~.Curve`Array.XY:py:class:`~.Curve`Array` object specifying a read-only sequence of :py:class:`~.Curve` objects associated to
        this axis.
    quantityType: QuantityType
        A :py:class:`~abaqus.XY.QuantityType.QuantityType` object specifying the quantity type: i.e. the physical dimension and
        associated label of the data represented by this axis.
    tickValues: float
        A tuple of Floats specifying the read-only major tick values shown.
    tickLabels: tuple
        A tuple of Strings specifying the read-only major tick labels shown.
    systemTitle: str
        A String specifying the system title. The system title is based on the **quantityType** of
        the axis and associated curves.
    title: str
        A String specifying the title of the axis. By default, the title is set to the
        **systemTitle**.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.charts[name].axes1[i].axisData
        session.charts[name].axes2[i].axisData
        session.defaultChartOptions.defaultAxis1Options.axisData
        session.defaultChartOptions.defaultAxis2Options.axisData
        session.xyPlots[name].charts[name].axes1[i].axisData
        session.xyPlots[name].charts[name].axes2[i].axisData

    """

    # A Float specifying the reference value for decibel computation. The default value is 
    # 1.0. 
    dbReference: float = 1

    # A SymbolicConstant specifying the direction of the axis. Possible values are ABSCISSA 
    # and ORDINATE. 
    direction: SymbolicConstant = None

    # A SymbolicConstant specifying how tick labels are formatted. Possible values are 
    # AUTOMATIC, DECIMAL, SCIENTIFIC, and ENGINEERING. The default value is AUTOMATIC. 
    labelFormat: SymbolicConstant = AUTOMATIC

    # An Int specifying the number of significant digits displayed for the labels. Possible 
    # values are 1 to 7. The default value is 2. 
    labelNumDigits: int = 2

    # A Boolean specifying whether or not to use the automatically computed maximum value for 
    # the axis. The default value is ON. 
    maxAutoCompute: Boolean = ON

    # A Float specifying the maximum value when *maxAutoCompute* is true. 
    maxAutoValue: float = None

    # A Float specifying the maximum value when *maxAutoCompute* is false. By default, 
    # *maxValue* is set to *maxAutoValue*. 
    maxValue: float = None

    # A Float specifying the current maximum value displayed for this axis. This value is 
    # different from *maxAutoValue* or *maxValue* when the axis is being transformed (zoom or 
    # pan). 
    maxShownValue: float = None

    # A Boolean specifying whether or not to use the automatically computed minimum value for 
    # the axis. The default value is ON. 
    minAutoCompute: Boolean = ON

    # A Float specifying the minimum value when *minAutoCompute* is true. 
    minAutoValue: float = None

    # A Float specifying the minimum value when *minAutoCompute* is false. By default, 
    # *minValue* is set to *minAutoValue*. 
    minValue: float = None

    # A Float specifying the current minimum value displayed for this axis. This value is 
    # different from *minAutoValue* or *minValue* when the axis is being transformed (zoom or 
    # pan). 
    minShownValue: float = None

    # An Int specifying the number the number of minor tick marks between major ticks. 
    # Possible values are 0 ≤≤ *minorTickCount* ≤≤ 20. When the *scale* is set to LOG, the 
    # minorTickCount is interpreted as the number of ticks per decade and limited to 0, 1, 4, 
    # 8, and 17. The default value is 1. 
    minorTickCount: int = 1

    # A SymbolicConstant specifying the type of scale to use for the axis. Possible values 
    # are:LINEAR, specifying tickmarks and labels are linearly distributed.LOG, specifying 
    # tickmarks and labels are logarithmically distributed.DB, specifying tickmarks and labels 
    # are distributed on a decibel scale.DB2, specifying tickmarks and labels are distributed 
    # on a 2*decibel scale.The default value is LINEAR. 
    scale: SymbolicConstant = LINEAR

    # A SymbolicConstant specifying the type of scale to use for the axis. Possible values 
    # are:AUTOCOMPUTE, specifying tickmarks and labels are automatically computed.INCREMENT, 
    # specifying tickmarks and labels are defined by a given increment.TOTAL_NUMBER, 
    # specifying tickmarks and labels are defined by the total number of ticks.The default 
    # value is AUTOCOMPUTE. 
    tickMode: SymbolicConstant = AUTOCOMPUTE

    # An Int specifying the number of major tick marks on the axis when *tickMode* 
    # =TOTAL_NUMBER. Possible values are 0 ≤≤ *tickCount* ≤≤ 30. The default value is computed 
    # based on the range of the axis. When the *scale* is set to LOG, the tickCount is 
    # interpreted as the number of ticks per decade and acceptable values are 1, 4, 8, and 17. 
    tickCount: int = None

    # An Int specifying the number of major ticks effectively shown. This value takes zoom, 
    # pan and rounding into account. 
    tickCountShown: int = None

    # A Float specifying the increment of the major tick marks on the axis when *tickMode* = 
    # INCREMENT. Valid values are 0 << *tickIncrement*. The default value is computed based on 
    # the results of the automatic method and the range being plotted. When the *scale* is set 
    # to LOG, the tickIncrement is interpreted as a value per decade and should be between 
    # 0.05 and 1. 
    tickIncrement: float = None

    # A Float specifying the shown tick increment of the major ticks. This value takes 
    # zoom/pan into account. 
    tickIncrementShown: float = None

    # A Boolean specifying whether the title to use for the axis title is system defined or 
    # user defined. The default value is ON. 
    useSystemTitle: Boolean = ON

    # An XYCurveArray object specifying a read-only sequence of Curve objects associated to 
    # this axis. 
    curves: XYCurveArray = XYCurveArray()

    # A QuantityType object specifying the quantity type: i.e. the physical dimension and 
    # associated label of the data represented by this axis. 
    quantityType: QuantityType = QuantityType()

    # A tuple of Floats specifying the read-only major tick values shown. 
    tickValues: float = None

    # A tuple of Strings specifying the read-only major tick labels shown. 
    tickLabels: tuple = ()

    # A String specifying the system title. The system title is based on the *quantityType* of 
    # the axis and associated curves. 
    systemTitle: str = ''

    # A String specifying the title of the axis. By default, the title is set to the 
    # *systemTitle*. 
    title: str = ''

    def setValues(self, axisData: 'AxisData' = None, labelFormat: SymbolicConstant = AUTOMATIC,
                  labelNumDigits: int = 2, scale: SymbolicConstant = LINEAR, dbReference: float = 1,
                  minAutoCompute: Boolean = ON, minValue: float = None, maxAutoCompute: Boolean = ON,
                  maxValue: float = None, tickMode: SymbolicConstant = AUTOCOMPUTE,
                  tickIncrement: float = None, tickCount: int = None, minorTickCount: int = 1,
                  title: str = '', useSystemTitle: Boolean = ON):
        """This method modifies the AxisData object.
        
        Parameters
        ----------
        axisData
            An AxisData object from which attributes are to be copied. 
        labelFormat
            A SymbolicConstant specifying how tick labels are formatted. Possible values are 
            AUTOMATIC, DECIMAL, SCIENTIFIC, and ENGINEERING. The default value is AUTOMATIC. 
        labelNumDigits
            An Int specifying the number of significant digits displayed for the labels. Possible 
            values are 1 to 7. The default value is 2. 
        scale
            A SymbolicConstant specifying the type of scale to use for the axis. Possible values 
            are:LINEAR, specifying tickmarks and labels are linearly distributed.LOG, specifying 
            tickmarks and labels are logarithmically distributed.DB, specifying tickmarks and labels 
            are distributed on a decibel scale.DB2, specifying tickmarks and labels are distributed 
            on a 2*decibel scale.The default value is LINEAR. 
        dbReference
            A Float specifying the reference value for decibel computation. The default value is 
            1.0. 
        minAutoCompute
            A Boolean specifying whether or not to use the automatically computed minimum value for 
            the axis. The default value is ON. 
        minValue
            A Float specifying the minimum value when *minAutoCompute* is false. By default, 
            *minValue* is set to *minAutoValue*. 
        maxAutoCompute
            A Boolean specifying whether or not to use the automatically computed maximum value for 
            the axis. The default value is ON. 
        maxValue
            A Float specifying the maximum value when *maxAutoCompute* is false. By default, 
            *maxValue* is set to *maxAutoValue*. 
        tickMode
            A SymbolicConstant specifying the type of scale to use for the axis. Possible values 
            are:AUTOCOMPUTE, specifying tickmarks and labels are automatically computed.INCREMENT, 
            specifying tickmarks and labels are defined by a given increment.TOTAL_NUMBER, 
            specifying tickmarks and labels are defined by the total number of ticks.The default 
            value is AUTOCOMPUTE. 
        tickIncrement
            A Float specifying the increment of the major tick marks on the axis when *tickMode* = 
            INCREMENT. Valid values are 0 << *tickIncrement*. The default value is computed based on 
            the results of the automatic method and the range being plotted. When the *scale* is set 
            to LOG, the tickIncrement is interpreted as a value per decade and should be between 
            0.05 and 1. 
        tickCount
            An Int specifying the number of major tick marks on the axis when *tickMode* 
            =TOTAL_NUMBER. Possible values are 0 ≤≤ *tickCount* ≤≤ 30. The default value is computed 
            based on the range of the axis. When the *scale* is set to LOG, the tickCount is 
            interpreted as the number of ticks per decade and acceptable values are 1, 4, 8, and 17. 
        minorTickCount
            An Int specifying the number the number of minor tick marks between major ticks. 
            Possible values are 0 ≤≤ *minorTickCount* ≤≤ 20. When the *scale* is set to LOG, the 
            minorTickCount is interpreted as the number of ticks per decade and limited to 0, 1, 4, 
            8, and 17. The default value is 1. 
        title
            A String specifying the title of the axis. By default, the title is set to the 
            *systemTitle*. 
        useSystemTitle
            A Boolean specifying whether the title to use for the axis title is system defined or 
            user defined. The default value is ON.

        Raises
        ------
        RangeError
        """
        pass
