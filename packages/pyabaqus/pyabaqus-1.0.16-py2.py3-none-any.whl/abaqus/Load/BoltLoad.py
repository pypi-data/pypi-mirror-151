from abaqusConstants import *
from .Load import Load
from ..Datum.DatumAxis import DatumAxis
from ..Region.Region import Region


class BoltLoad(Load):
    """The BoltLoad object defines a bolt load.
    The BoltLoad object is derived from the Load object. 

    Attributes
    ----------
    name: str
        A String specifying the load repository key.
    datumAxis: DatumAxis
        A :py:class:`~abaqus.Datum.DatumAxis.DatumAxis` object specifying the orientation of the pre-tension section
        normal.Note:**datumAxis** is required only for Solid and Shell regions; it has no meaning
        for Wire regions.
    region: Region
        A :py:class:`~abaqus.Region.Region.Region` object specifying the region to which the load is applied.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import load
        mdb.models[name].loads[name]

    The corresponding analysis keywords are:

    - PRE-TENSION SECTION
            - NODE
            - NSET

    """

    # A String specifying the load repository key. 
    name: str = ''

    # A DatumAxis object specifying the orientation of the pre-tension section 
    # normal.Note:*datumAxis* is required only for Solid and Shell regions; it has no meaning 
    # for Wire regions. 
    datumAxis: DatumAxis = DatumAxis()

    # A Region object specifying the region to which the load is applied. 
    region: Region = Region()

    def __init__(self, name: str, createStepName: str, region: Region, magnitude: float,
                 boltMethod: SymbolicConstant = APPLY_FORCE, datumAxis: DatumAxis = DatumAxis(),
                 amplitude: str = UNSET, preTenSecPartLevel: Boolean = False):
        """This method creates a BoltLoad object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].BoltLoad
        
        Parameters
        ----------
        name
            A String specifying the load repository key. 
        createStepName
            A String specifying the name of the step in which the load is created. This must be the 
            first analysis step name. 
        region
            A Region object specifying the region to which the load is applied. 
        magnitude
            A Float specifying the bolt load magnitude. 
        boltMethod
            A SymbolicConstant specifying the method of applying the bolt load. Possible values are 
            APPLY_FORCE and ADJUST_LENGTH. The default value is APPLY_FORCE. 
        datumAxis
            A DatumAxis object specifying the orientation of the pre-tension section normal.Note: 
            *datumAxis* is applicable only for Solid and Shell regions; it has no meaning for Wire 
            regions. 
        amplitude
            A String or the SymbolicConstant UNSET specifying the name of the amplitude reference. 
            UNSET should be used if the load has no amplitude reference. The default value is UNSET. 
            You should provide the *amplitude* argument only if it is valid for the specified step. 
        preTenSecPartLevel
            A Boolean specifying whether the pre-tension section is to be defined at the part level. 
            The default value is False. You should provide the *preTenSecPartLevel* argument only if 
            the selected region belongs to a dependent part instance. A pre-tension section cannot 
            be defined at the part level for independent and model instances. 

        Returns
        -------
            A BoltLoad object. 

        Raises
        ------
            TextError. 
        """
        super().__init__()
        pass

    def setValues(self, boltMethod: SymbolicConstant = APPLY_FORCE, datumAxis: DatumAxis = DatumAxis(),
                  amplitude: str = UNSET, preTenSecPartLevel: Boolean = False):
        """This method modifies the data for an existing BoltLoad object in the step where it is
        created.
        
        Parameters
        ----------
        boltMethod
            A SymbolicConstant specifying the method of applying the bolt load. Possible values are 
            APPLY_FORCE and ADJUST_LENGTH. The default value is APPLY_FORCE. 
        datumAxis
            A DatumAxis object specifying the orientation of the pre-tension section normal.Note: 
            *datumAxis* is applicable only for Solid and Shell regions; it has no meaning for Wire 
            regions. 
        amplitude
            A String or the SymbolicConstant UNSET specifying the name of the amplitude reference. 
            UNSET should be used if the load has no amplitude reference. The default value is UNSET. 
            You should provide the *amplitude* argument only if it is valid for the specified step. 
        preTenSecPartLevel
            A Boolean specifying whether the pre-tension section is to be defined at the part level. 
            The default value is False. You should provide the *preTenSecPartLevel* argument only if 
            the selected region belongs to a dependent part instance. A pre-tension section cannot 
            be defined at the part level for independent and model instances. 
        """
        pass

    def setValuesInStep(self, stepName: str, boltMethod: SymbolicConstant = APPLY_FORCE, magnitude: float = None,
                        amplitude: str = ''):
        """This method modifies the propagating data for an existing BoltLoad object in the
        specified step.
        
        Parameters
        ----------
        stepName
            A String specifying the name of the step in which the load is modified. 
        boltMethod
            A SymbolicConstant specifying the type of bolt load. Possible values are APPLY_FORCE, 
            ADJUST_LENGTH, and FIX_LENGTH. The default is APPLY_FORCE. 
        magnitude
            A Float specifying the bolt load magnitude. 
        amplitude
            A String or a SymbolicConstant specifying the name of the amplitude reference. Possible 
            values for the SymbolicConstant are UNCHANGED and FREED. UNCHANGED should be used if the 
            amplitude is propagated from the previous analysis step. FREED should be used if the 
            load is changed to have no amplitude reference. You should provide the *amplitude* 
            argument only if it is valid for the specified step. 
        """
        pass
