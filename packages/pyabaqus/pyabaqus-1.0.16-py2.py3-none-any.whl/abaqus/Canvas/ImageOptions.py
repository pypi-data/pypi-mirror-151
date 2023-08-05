from abaqusConstants import *


class ImageOptions:
    """The ImageOptions object stores settings that control how an image is rendered in a
    particular viewport. ImageOptions objects are accessed from the image options associated 
    with a particular viewport. 
    The ImageOptions object has no constructor; Abaqus creates the *imageOptions* member for 
    a viewport when the viewport is created using the values in the *imageOptions* member of 
    the current viewport. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block::
    
        session.viewports[name].imageOptions

    """

    def setValues(self, imageName: str = '', showImage: Boolean = OFF,
                  positionMethod: SymbolicConstant = FIT_TO_VIEWPORT,
                  fitMethod: SymbolicConstant = BEST_FIT, alignment: SymbolicConstant = CENTER,
                  xScale: float = 1, yScale: float = 1, origin: tuple[float] = (),
                  translucency: float = 1, options: str = None):
        """This method modifies the ImageOptions object.
        
        Parameters
        ----------
        imageName
            A String specifying the name of the image. A list of valid image names is in the 
            *images* repository in the *session* object. 
        showImage
            A Boolean specifying whether an image should be displayed in the viewport background. 
            The default value is OFF. 
        positionMethod
            A SymbolicConstant specifying which positioning method is used to determine how the 
            image will be scaled and positioned in the viewport. Possible values 
            are:FIT_TO_VIEWPORT, specifying a display mode where the image is scaled to fit in the 
            viewport using the specified *fitMethod*.AUTO_ALIGN, specifying a display mode where the 
            image is scaled as specified by *xScale* and *yScale* and then positioned in the 
            viewport using the specified *alignment*.MANUAL, specifying a display mode where the 
            image is scaled as specified by *xScale* and *yScale* and then positioned in the 
            viewport using the specified *origin*.The default value is FIT_TO_VIEWPORT. 
        fitMethod
            A SymbolicConstant specifying which type of fit is performed to scale and position the 
            image in the viewport when *positionMethod* =FIT_TO_VIEWPORT. Possible values 
            are:BEST_FIT, specifying a mode where the image is scaled to completely fit within the 
            viewport.FIT_WIDTH, specifying a mode where the image width is scaled to match the 
            viewport width.FIT_HEIGHT, specifying a mode where the image height is scaled to match 
            the viewport height.The default value is BEST_FIT. 
        alignment
            A SymbolicConstant specifying the relative position of the image in the viewport when 
            *positionMethod* =AUTO_ALIGN. Possible values 
            are:BOTTOM_LEFTBOTTOM_CENTERBOTTOM_RIGHTCENTER_LEFTCENTERCENTER_RIGHTTOP_LEFTTOP_CENTERTOP_RIGHTThe 
            default value is CENTER. 
        xScale
            A Float specifying the scale applied to the image width. The *xScale* argument is 
            ignored when *positionMethod* =FIT_TO_VIEWPORT. The default value is 1.0.When *xScale* 
            is negative, the image is mirrored about its y-axis but its position is not affected. 
        yScale
            A Float specifying the scale applied to the image height. The *yScale* argument is 
            ignored when *positionMethod* =FIT_TO_VIEWPORT. The default value is 1.0.When *yScale* 
            is negative, the image is mirrored about its x-axis but its position is not affected. 
        origin
            A pair of Floats specifying the *X*- and *Y*-offsets in millimeters from the lower-left 
            corner of the viewport. The *origin* argument is ignored unless *positionMethod* 
            =MANUAL. The default value is (0, 0). 
        translucency
            A Float specifying the translucency factor to use when displaying the image. Possible 
            values are 0.0 ≤≤ *translucency* ≤≤ 1.0 with 0.0 being invisible and 1.0 being opaque. 
            The default value is 1.0. 
        options
            None or an ImageOptions object specifying the object from which values are to be copied. 
            If other arguments are also supplied to setValues, they will override the values in the 
            *options* member. The default value is None.

        Raises
        ------
        RangeError
        """
        pass
