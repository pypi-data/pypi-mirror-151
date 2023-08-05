from abaqusConstants import *


class AnimationOptions:
    """The AnimationOptions object is used to store values and attributes associated with an
    AnimationController object. 
    The AnimationOptions object has no constructor command. Abaqus creates the 
    *animationOptions* member when it creates the AnimationController object. 

    Attributes
    ----------
    mode: SymbolicConstant
        A SymbolicConstant specifying the animation mode. Possible values are PLAY_ONCE, LOOP,
        LOOP_BACKWARD, and SWING. The default value is LOOP.
    frameRate: int
        An Int specifying the animation rate in frames/second. Possible values are 1 ≤≤
        **frameRate** ≤≤ 100. The default value is 50.
    frameCounter: Boolean
        A Boolean specifying whether to show the frame counter. The default value is ON.
    relativeScaling: SymbolicConstant
        A SymbolicConstant specifying the relative scaling when the :py:class:`~abaqus.Animation.AnimationController.AnimationController` object's
        **animationType=SCALE_FACTOR** or HARMONIC. Possible values are FULL_CYCLE and HALF_CYCLE.
        The default value is HALF_CYCLE.
    numScaleFactorFrames: int
        An Int specifying the number of frames to be used when the :py:class:`~abaqus.Animation.AnimationController.AnimationController` object's
        **animationType=SCALE_FACTOR** or HARMONIC. The default value is 7.
    timeHistoryMode: SymbolicConstant
        A SymbolicConstant specifying whether the time history animation is time based or frame
        based. Possible values are FRAME_BASED and TIME_BASED. The default value is FRAME_BASED.
    maxTime: float
        A Float specifying the maximum time for time based time history animation when
        **maxTimeAutoCompute** = False.
    maxTimeAutoCompute: Boolean
        A Boolean specifying whether the animation maximum time value should be computed from
        the active frames when **timeHistoryMode** is set to TIME_BASED. The default value is ON.
    maxTimeAutoValue: float
        A Float specifying the maximum time when **timeHistoryMode** is set to TIME_BASED and the
        **maxTimeAutoCompute** value is True. This value is computed as the maximum time of all
        active frames displayed in viewports where the animation is active.
    minTime: float
        A Float specifying the minimum time for time based time history animation when
        **minTimeAutoCompute** = False.
    minTimeAutoCompute: Boolean
        A Boolean specifying whether the animation minimum time value should be computed from
        the active frames when **timeHistoryMode** is set to TIME_BASED. The default value is ON.
    minTimeAutoValue: float
        A Float specifying the minimum time when **timeHistoryMode** is set to TIME_BASED and the
        **minTimeAutoCompute** value is True. This value is computed as the minimum time of all
        active frames displayed in viewports where the animation is active.
    timeIncrement: float
        A Float specifying the time increment for frame selection when **timeHistoryMode** is set
        to TIME_BASED.
    xyUseHighlightMethod: Boolean
        A Boolean specifying whether to use the highlight method to draw the time tracker line
        and symbols. The default value is ON.
    xyShowLine: Boolean
        A Boolean specifying whether to show the time tracker line. The default value is ON.
    xyLineStyle: SymbolicConstant
        A SymbolicConstant specifying the *X–Y* time tracker line style. Possible values are
        SOLID, DASHED, DOTTED, and DOT_DASH. The default value is SOLID.
    xyLineThickness: SymbolicConstant
        A SymbolicConstant specifying the *X–Y* time tracker line thickness. Possible values are
        VERY_THIN, THIN, MEDIUM, and THICK. The default value is MEDIUM.
    xyShowSymbol: Boolean
        A Boolean specifying whether to show the time tracker symbols. The default value is ON.
    xySymbolMarker: SymbolicConstant
        A SymbolicConstant specifying the marker type to be used for all animation capable *X–Y*
        curve or the SymbolicConstant DEFAULT specifying that the system will take the marker
        associated to each curve Possible values are:
            - FILLED_CIRCLE
            - FILLED_SQUARE
            - FILLED_DIAMOND
            - FILLED_TRI
            - HOLLOW_CIRCLE
            - HOLLOW_SQUARE
            - HOLLOW_DIAMOND
            - HOLLOW_TRI
            - CROSS
            - XMARKER
            - DEFAULT
        The default value is DEFAULT.
    xySymbolSize: SymbolicConstant
        A SymbolicConstant specifying the size of the markers. Possible values are SMALL,
        MEDIUM, and LARGE. The default value is MEDIUM.
    xyLineColor: str
        A String specifying the color used to plot the *X–Y* time tracker line when
        **xyUseHighlightMethod** = False. The default value is "Yellow".
    xySymbolColor: str
        A String specifying the color used to plot *X–Y* time tracker symbols when
        **xyUseHighlightMethod** = False. When setting the color to 'Default' the system will take
        the color associated to each curve. The default value is "Default".

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import animation
        session.animationOptions

    """

    # A SymbolicConstant specifying the animation mode. Possible values are PLAY_ONCE, LOOP, 
    # LOOP_BACKWARD, and SWING. The default value is LOOP. 
    mode: SymbolicConstant = LOOP

    # An Int specifying the animation rate in frames/second. Possible values are 1 ≤≤ 
    # *frameRate* ≤≤ 100. The default value is 50. 
    frameRate: int = 50

    # A Boolean specifying whether to show the frame counter. The default value is ON. 
    frameCounter: Boolean = ON

    # A SymbolicConstant specifying the relative scaling when the AnimationController object's 
    # *animationType*=SCALE_FACTOR or HARMONIC. Possible values are FULL_CYCLE and HALF_CYCLE. 
    # The default value is HALF_CYCLE. 
    relativeScaling: SymbolicConstant = HALF_CYCLE

    # An Int specifying the number of frames to be used when the AnimationController object's 
    # *animationType*=SCALE_FACTOR or HARMONIC. The default value is 7. 
    numScaleFactorFrames: int = 7

    # A SymbolicConstant specifying whether the time history animation is time based or frame 
    # based. Possible values are FRAME_BASED and TIME_BASED. The default value is FRAME_BASED. 
    timeHistoryMode: SymbolicConstant = FRAME_BASED

    # A Float specifying the maximum time for time based time history animation when 
    # *maxTimeAutoCompute* = False. 
    maxTime: float = None

    # A Boolean specifying whether the animation maximum time value should be computed from 
    # the active frames when *timeHistoryMode* is set to TIME_BASED. The default value is ON. 
    maxTimeAutoCompute: Boolean = ON

    # A Float specifying the maximum time when *timeHistoryMode* is set to TIME_BASED and the 
    # *maxTimeAutoCompute* value is True. This value is computed as the maximum time of all 
    # active frames displayed in viewports where the animation is active. 
    maxTimeAutoValue: float = None

    # A Float specifying the minimum time for time based time history animation when 
    # *minTimeAutoCompute* = False. 
    minTime: float = None

    # A Boolean specifying whether the animation minimum time value should be computed from 
    # the active frames when *timeHistoryMode* is set to TIME_BASED. The default value is ON. 
    minTimeAutoCompute: Boolean = ON

    # A Float specifying the minimum time when *timeHistoryMode* is set to TIME_BASED and the 
    # *minTimeAutoCompute* value is True. This value is computed as the minimum time of all 
    # active frames displayed in viewports where the animation is active. 
    minTimeAutoValue: float = None

    # A Float specifying the time increment for frame selection when *timeHistoryMode* is set 
    # to TIME_BASED. 
    timeIncrement: float = None

    # A Boolean specifying whether to use the highlight method to draw the time tracker line 
    # and symbols. The default value is ON. 
    xyUseHighlightMethod: Boolean = ON

    # A Boolean specifying whether to show the time tracker line. The default value is ON. 
    xyShowLine: Boolean = ON

    # A SymbolicConstant specifying the *X–Y* time tracker line style. Possible values are 
    # SOLID, DASHED, DOTTED, and DOT_DASH. The default value is SOLID. 
    xyLineStyle: SymbolicConstant = SOLID

    # A SymbolicConstant specifying the *X–Y* time tracker line thickness. Possible values are 
    # VERY_THIN, THIN, MEDIUM, and THICK. The default value is MEDIUM. 
    xyLineThickness: SymbolicConstant = MEDIUM

    # A Boolean specifying whether to show the time tracker symbols. The default value is ON. 
    xyShowSymbol: Boolean = ON

    # A SymbolicConstant specifying the marker type to be used for all animation capable *X–Y* 
    # curve or the SymbolicConstant DEFAULT specifying that the system will take the marker 
    # associated to each curve Possible values are: 
    # - FILLED_CIRCLE 
    # - FILLED_SQUARE 
    # - FILLED_DIAMOND 
    # - FILLED_TRI 
    # - HOLLOW_CIRCLE 
    # - HOLLOW_SQUARE 
    # - HOLLOW_DIAMOND 
    # - HOLLOW_TRI 
    # - CROSS 
    # - XMARKER 
    # - DEFAULT 
    # The default value is DEFAULT. 
    xySymbolMarker: SymbolicConstant = DEFAULT

    # A SymbolicConstant specifying the size of the markers. Possible values are SMALL, 
    # MEDIUM, and LARGE. The default value is MEDIUM. 
    xySymbolSize: SymbolicConstant = MEDIUM

    # A String specifying the color used to plot the *X–Y* time tracker line when 
    # *xyUseHighlightMethod* = False. The default value is "Yellow". 
    xyLineColor: str = ''

    # A String specifying the color used to plot *X–Y* time tracker symbols when 
    # *xyUseHighlightMethod* = False. When setting the color to 'Default' the system will take 
    # the color associated to each curve. The default value is "Default". 
    xySymbolColor: str = ''

    def setValues(self, mode: SymbolicConstant = LOOP, frameRate: int = 50, frameCounter: Boolean = ON,
                  relativeScaling: SymbolicConstant = HALF_CYCLE, numScaleFactorFrames: int = 7,
                  timeHistoryMode: SymbolicConstant = FRAME_BASED, maxTime: float = None,
                  maxTimeAutoCompute: Boolean = ON, minTime: float = None,
                  minTimeAutoCompute: Boolean = ON, timeIncrement: float = None,
                  xyUseHighlightMethod: Boolean = ON, xyShowLine: Boolean = ON,
                  xyLineStyle: SymbolicConstant = SOLID, xyLineThickness: SymbolicConstant = MEDIUM,
                  xyLineColor: str = '', xyShowSymbol: Boolean = ON,
                  xySymbolMarker: SymbolicConstant = DEFAULT, xySymbolSize: SymbolicConstant = MEDIUM,
                  xySymbolColor: str = ''):
        """This method modifies the AnimationOptions object.
        
        Parameters
        ----------
        mode
            A SymbolicConstant specifying the animation mode. Possible values are PLAY_ONCE, LOOP, 
            LOOP_BACKWARD, and SWING. The default value is LOOP. 
        frameRate
            An Int specifying the animation rate in frames/second. Possible values are 1 ≤≤ 
            *frameRate* ≤≤ 100. The default value is 50. 
        frameCounter
            A Boolean specifying whether to show the frame counter. The default value is ON. 
        relativeScaling
            A SymbolicConstant specifying the relative scaling when the AnimationController object's 
            *animationType*=SCALE_FACTOR or HARMONIC. Possible values are FULL_CYCLE and HALF_CYCLE. 
            The default value is HALF_CYCLE. 
        numScaleFactorFrames
            An Int specifying the number of frames to be used when the AnimationController object's 
            *animationType*=SCALE_FACTOR or HARMONIC. The default value is 7. 
        timeHistoryMode
            A SymbolicConstant specifying whether the time history animation is time based or frame 
            based. Possible values are FRAME_BASED and TIME_BASED. The default value is FRAME_BASED. 
        maxTime
            A Float specifying the maximum time for time based time history animation when 
            *maxTimeAutoCompute* = False. 
        maxTimeAutoCompute
            A Boolean specifying whether the animation maximum time value should be computed from 
            the active frames when *timeHistoryMode* is set to TIME_BASED. The default value is ON. 
        minTime
            A Float specifying the minimum time for time based time history animation when 
            *minTimeAutoCompute* = False. 
        minTimeAutoCompute
            A Boolean specifying whether the animation minimum time value should be computed from 
            the active frames when *timeHistoryMode* is set to TIME_BASED. The default value is ON. 
        timeIncrement
            A Float specifying the time increment for frame selection when *timeHistoryMode* is set 
            to TIME_BASED. 
        xyUseHighlightMethod
            A Boolean specifying whether to use the highlight method to draw the time tracker line 
            and symbols. The default value is ON. 
        xyShowLine
            A Boolean specifying whether to show the time tracker line. The default value is ON. 
        xyLineStyle
            A SymbolicConstant specifying the *X–Y* time tracker line style. Possible values are 
            SOLID, DASHED, DOTTED, and DOT_DASH. The default value is SOLID. 
        xyLineThickness
            A SymbolicConstant specifying the *X–Y* time tracker line thickness. Possible values are 
            VERY_THIN, THIN, MEDIUM, and THICK. The default value is MEDIUM. 
        xyLineColor
            A String specifying the color used to plot the *X–Y* time tracker line when 
            *xyUseHighlightMethod* = False. The default value is "Yellow". 
        xyShowSymbol
            A Boolean specifying whether to show the time tracker symbols. The default value is ON. 
        xySymbolMarker
            A SymbolicConstant specifying the marker type to be used for all animation capable *X–Y* 
            curve or the SymbolicConstant DEFAULT specifying that the system will take the marker 
            associated to each curve Possible values are: 
            
            - FILLED_CIRCLE 
            - FILLED_SQUARE 
            - FILLED_DIAMOND 
            - FILLED_TRI 
            - HOLLOW_CIRCLE 
            - HOLLOW_SQUARE 
            - HOLLOW_DIAMOND 
            - HOLLOW_TRI 
            - CROSS 
            - XMARKER 
            - DEFAULT 
            The default value is DEFAULT. 
        xySymbolSize
            A SymbolicConstant specifying the size of the markers. Possible values are SMALL, 
            MEDIUM, and LARGE. The default value is MEDIUM. 
        xySymbolColor
            A String specifying the color used to plot *X–Y* time tracker symbols when 
            *xyUseHighlightMethod* = False. When setting the color to 'Default' the system will take 
            the color associated to each curve. The default value is "Default". 
        """
        pass
