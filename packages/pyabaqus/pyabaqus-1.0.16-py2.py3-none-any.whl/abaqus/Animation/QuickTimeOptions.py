from abaqusConstants import *


class QuickTimeOptions:
    """The QuickTimeOptions object is used to store values and attributes to be used in
    generating QuickTime animation. The QuickTimeOptions object has no constructor. Abaqus 
    creates the *quickTimeOptions* member when the animation module is imported. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import animation
        session.quickTimeOptions

    """

    def setValues(self, compressionMethod: SymbolicConstant = RLE24,
                  sizeDefinition: SymbolicConstant = SIZE_ON_SCREEN, imageSize: int = None):
        """This method modifies the QuickTimeOptions object.
        
        Parameters
        ----------
        compressionMethod
            A SymbolicConstant specifying the compression method for the QuickTime format. Possible 
            values are: 
            - RAW24, specifying an uncompressed format of 24 bits per pixel. 
            - RLE24, specifying a run length encoded format of 24 bits per pixel. 
            The default value is RLE24. 
        sizeDefinition
            A SymbolicConstant specifying how the width and height of the image are specified. 
            Possible values are SIZE_ON_SCREEN and USER_DEFINED. The default value is 
            SIZE_ON_SCREEN. 
        imageSize
            A pair of Ints specifying the width and height of the image in pixels when 
            *sizeDefinition*=USER_DEFINED. Possible values are Ints in the range (*minWidth*, 
            *minHeight*) ≤≤ (width, height) ≤≤ (*maxWidth*, *maxHeight*). The default value is the 
            screen size. 
            Note:The values of the minimum width (*minWidth*) and height (*minHeight*) depend on the 
            following:viewport font size,whether decorations are printed,decoration size, andscreen 
            resolution.The minimum width and height are normally < 50 pixels. The values of the 
            maximum width (*maxWidth*) and height (*maxHeight*) depend on the graphics capabilities 
            of the system. The maximum width and height will be at least as large as the screen 
            dimensions. 
        """
        pass
