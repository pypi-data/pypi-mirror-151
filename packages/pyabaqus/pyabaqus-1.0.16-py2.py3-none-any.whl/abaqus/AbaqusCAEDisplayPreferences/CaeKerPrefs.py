from abaqusConstants import *


class CaeKerPrefs:
    """The CaeKerPrefs object contains the details of the sessionOptions.

    Attributes
    ----------
    fileName: str
        A String specifying the path to the preferences file that the :py:class:`~abaqus.AbaqusCAEDisplayPreferences.CaeKerPrefs.CaeKerPrefs` object
        represents.

    Notes
    -----
    This object can be accessed by:
        
    .. code-block:: python

        import caePrefsAccess
        caePrefsAccess.openSessionOptions(...)

    """

    # A String specifying the path to the preferences file that the CaeKerPrefs object 
    # represents. 
    fileName: str = ''

    def save(self, backupFile: Boolean = OFF):
        """This method saves the sessionOptions in the current *fileName*.
        
        Parameters
        ----------
        backupFile
            A Boolean specifying whether save a numbered backup copy of the preferences file, 
            *fileName*. Default is True. 
        """
        pass

    def saveAs(self, fileName: str, directory: SymbolicConstant):
        """This method saves the sessionOptions to the specified location.
        
        Parameters
        ----------
        fileName
            A String specifying the path to the preferences file. 
        directory
            A SymbolicConstant specifying the location of the preferences file. Possible values 
            are:CURRENT to open the preferences file in the current directory 
            (caePrefsAccess.CURRENT)HOME to open the preferences file in your home directory 
            (caePrefsAccess.HOME)The default value is HOME. Either *fileName* or *directory* must be 
            supplied. The *fileName* or *directory* arguments are mutually exclusive. 
        """
        pass
