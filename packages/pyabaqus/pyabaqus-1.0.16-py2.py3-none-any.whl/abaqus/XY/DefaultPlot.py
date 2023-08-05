from .Area import Area
from .Title import Title


class DefaultPlot:
    """The DefaultPlot object is used to hold on default plot attributes. The DefaultPlot
    object attributes are used whenever an XYPlot object is created. A DefaultPlot object is 
    automatically created when opening a session. 

    Attributes
    ----------
    area: Area
        An :py:class:`~abaqus.XY.Area.Area` object specifying an :py:class:`~abaqus.XY.Area.Area` used to hold on to the default display properties for
        the plot area.
    title: Title
        A :py:class:`~abaqus.XY.:py:class:`~abaqus.XY.Title.Title`.:py:class:`~abaqus.XY.Title.Title`` object specifying a :py:class:`~abaqus.XY.:py:class:`~abaqus.XY.Title.Title`.:py:class:`~abaqus.XY.Title.Title`` object used to hold on to the default properties of
        the XY-Plot title.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.defaultPlot

    """

    # An Area object specifying an Area used to hold on to the default display properties for 
    # the plot area. 
    area: Area = Area()

    # A Title object specifying a Title object used to hold on to the default properties of 
    # the XY-Plot title. 
    title: Title = Title()
