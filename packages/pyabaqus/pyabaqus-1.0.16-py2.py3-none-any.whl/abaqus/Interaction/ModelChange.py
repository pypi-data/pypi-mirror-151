from abaqusConstants import *
from .Interaction import Interaction
from ..Region.Region import Region


class ModelChange(Interaction):
    """The ModelChange object defines model change interactions for element removal and
    reactivation. 
    The ModelChange object is derived from the Interaction object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import interaction
        mdb.models[name].interactions[name]

    The corresponding analysis keywords are:

    - MODEL CHANGE

    """

    def __init__(self, name: str, createStepName: str, isRestart: Boolean = OFF,
                 regionType: SymbolicConstant = GEOMETRY, region: Region = Region(),
                 activeInStep: Boolean = OFF, includeStrain: Boolean = OFF):
        """This method creates a ModelChange object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].ModelChange
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        createStepName
            A String specifying the name of the step in which the ModelChange object is created. 
        isRestart
            A Boolean specifying whether this interaction is being used solely to indicate that 
            model change may be required in a subsequent restart analysis (either for elements or 
            contact pairs). The default value is OFF. 
        regionType
            A SymbolicConstant specifying the region selection type. This argument is valid only 
            when *isRestart*=False. Possible values are GEOMETRY, SKINS, STRINGERS, and ELEMENTS. 
            The default value is GEOMETRY. 
        region
            A Region object specifying the elements to be removed or reactivated. This argument is 
            valid only when *isRestart*=False. 
        activeInStep
            A Boolean specifying whether elements are being removed or reactivated. This argument is 
            valid only when *isRestart*=False. The default value is OFF. 
        includeStrain
            A Boolean specifying whether stress/displacement elements are reactivated with strain. 
            This argument is valid only when *isRestart*=False and when *activeInStep*=True. The 
            default value is OFF. 

        Returns
        -------
            A ModelChange object.
        """
        super().__init__()
        pass

    def setValues(self, isRestart: Boolean = OFF, regionType: SymbolicConstant = GEOMETRY,
                  region: Region = Region(), activeInStep: Boolean = OFF, includeStrain: Boolean = OFF):
        """This method modifies the data for an existing ModelChange object in the step where it is
        created.
        
        Parameters
        ----------
        isRestart
            A Boolean specifying whether this interaction is being used solely to indicate that 
            model change may be required in a subsequent restart analysis (either for elements or 
            contact pairs). The default value is OFF. 
        regionType
            A SymbolicConstant specifying the region selection type. This argument is valid only 
            when *isRestart*=False. Possible values are GEOMETRY, SKINS, STRINGERS, and ELEMENTS. 
            The default value is GEOMETRY. 
        region
            A Region object specifying the elements to be removed or reactivated. This argument is 
            valid only when *isRestart*=False. 
        activeInStep
            A Boolean specifying whether elements are being removed or reactivated. This argument is 
            valid only when *isRestart*=False. The default value is OFF. 
        includeStrain
            A Boolean specifying whether stress/displacement elements are reactivated with strain. 
            This argument is valid only when *isRestart*=False and when *activeInStep*=True. The 
            default value is OFF. 
        """
        pass

    def setValuesInStep(self, stepName: str, activeInStep: Boolean = OFF, includeStrain: Boolean = OFF):
        """This method modifies the propagating data of an existing ModelChange object in the
        specified step.
        
        Parameters
        ----------
        stepName
            A String specifying the name of the step in which the interaction is modified. 
        activeInStep
            A Boolean specifying whether elements are being removed or reactivated. This argument is 
            valid only when *isRestart*=False. The default value is OFF. 
        includeStrain
            A Boolean specifying whether stress/displacement elements are reactivated with strain. 
            This argument is valid only when *isRestart*=False and when *activeInStep*=True. The 
            default value is OFF. 
        """
        pass
