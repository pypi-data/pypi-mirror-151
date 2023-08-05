

class Annotation:
    """The Annotation object is the abstract base type for other Annotation objects. The
    Annotation object has no explicit constructor. The methods and members of the Annotation 
    object are common to all objects derived from Annotation. 

    Attributes
    ----------
    name: str
        A String specifying the annotation repository key.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import annotationToolset
        mdb.annotations[name]
        session.odbs[name].userData.annotations[name]
        session.viewports[name].annotationsToPlot[i]

    """

    # A String specifying the annotation repository key. 
    name: str = ''

    def bringToFront(self):
        """This method brings the Annotation object to the top of the annotation stack.
        """
        pass

    def sendToBack(self):
        """This method sends the Annotation object to the bottom of the annotation stack.
        """
        pass

    def bringForward(self):
        """This method brings the Annotation object one position up in the annotation stack.
        """
        pass

    def sendBackward(self):
        """This method sends the Annotation object one position down in the annotation stack.
        """
        pass

    def moveBefore(self, name: str):
        """This method moves the Annotation object before another object in the same repository.
        
        Parameters
        ----------
        name
            A String specifying the name of the other Annotation object.
        """
        pass

    def moveAfter(self, name: str):
        """This method moves the Annotation object after another object in the same repository.
        
        Parameters
        ----------
        name
            A String specifying the name of the other Annotation object. 
        """
        pass

    def translate(self, x: float = None, y: float = None):
        """This method translates the Annotation object on the viewport plane.
        
        Parameters
        ----------
        x
            A Float specifying the *X* translation amount in millimeters. 
        y
            A Float specifying the *Y* translation amount in millimeters. 
        """
        pass
