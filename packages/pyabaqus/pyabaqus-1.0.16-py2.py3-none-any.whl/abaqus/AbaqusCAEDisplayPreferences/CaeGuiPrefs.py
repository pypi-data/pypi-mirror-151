from abaqusConstants import *


class CaeGuiPrefs:
    """The CaeGuiPrefs object contains the details of the graphical preferences in a
    guiPreferences section of the abaqus_2021.gpr file. 

    Attributes
    ----------
    fileName: str
        A String specifying the path to the preferences file.

    Notes
    -----
    This object can be accessed by:
        
    .. code-block:: python

        import caePrefsAccess
        caePrefsAccess.openGuiPreferences(...)

    """

    # A String specifying the path to the preferences file. 
    fileName: str = ''

    def save(self, backupFile: Boolean = OFF):
        """This method saves the guiPreferences section specified in the current *fileName*.
        
        Parameters
        ----------
        backupFile
            A Boolean specifying whether Abaqus should save a numbered backup copy of the 
            preferences file, *fileName*. Default is True. 
        """
        pass

    def saveAs(self, fileName: str):
        """This method saves the guiPreferences settings to the specified location.
        
        Parameters
        ----------
        fileName
            A String specifying the path to the preferences file. 
        """
        pass
