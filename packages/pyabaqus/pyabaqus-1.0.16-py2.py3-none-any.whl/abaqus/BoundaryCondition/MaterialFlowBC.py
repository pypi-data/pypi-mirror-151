import typing

from abaqusConstants import *
from .BoundaryCondition import BoundaryCondition
from ..Region.Region import Region


class MaterialFlowBC(BoundaryCondition):
    """The MaterialFlowBC object stores the data for a connector material flow boundary
    condition. 
    The MaterialFlowBC object is derived from the BoundaryCondition object. 

    Attributes
    ----------
    name: str
        A String specifying the boundary condition repository key.
    distributionType: SymbolicConstant
        A SymbolicConstant specifying how the boundary condition is distributed spatially.
        Possible values are UNIFORM, USER_DEFINED, and FIELD. The default value is UNIFORM.
    fieldName: str
        A String specifying the name of the :py:class:`~abaqus.Field.AnalyticalField.AnalyticalField` object associated with this boundary
        condition. The **fieldName** argument applies only when **distributionType=FIELD**. The
        default value is an empty string.
    category: SymbolicConstant
        A SymbolicConstant specifying the category of the boundary condition. Possible values
        are MECHANICAL and THERMAL.
    region: Region
        A :py:class:`~abaqus.Region.Region.Region` object specifying the region to which the boundary condition is applied.
    localCsys: str
        None or a :py:class:`~abaqus.Datum.DatumCsys.DatumCsys` object specifying the local coordinate system of the boundary
        condition's degrees of freedom. If **localCsys=None**, the degrees of freedom are defined
        in the global coordinate system. The default value is None.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import load
        mdb.models[name].boundaryConditions[name]

    """

    # A String specifying the boundary condition repository key. 
    name: str = ''

    # A SymbolicConstant specifying how the boundary condition is distributed spatially. 
    # Possible values are UNIFORM, USER_DEFINED, and FIELD. The default value is UNIFORM. 
    distributionType: SymbolicConstant = UNIFORM

    # A String specifying the name of the AnalyticalField object associated with this boundary 
    # condition. The *fieldName* argument applies only when *distributionType*=FIELD. The 
    # default value is an empty string. 
    fieldName: str = ''

    # A SymbolicConstant specifying the category of the boundary condition. Possible values 
    # are MECHANICAL and THERMAL. 
    category: SymbolicConstant = None

    # A Region object specifying the region to which the boundary condition is applied. 
    region: Region = Region()

    # None or a DatumCsys object specifying the local coordinate system of the boundary 
    # condition's degrees of freedom. If *localCsys*=None, the degrees of freedom are defined 
    # in the global coordinate system. The default value is None. 
    localCsys: str = None

    def __init__(self, name: str, createStepName: str, region: Region, fieldName: str = '',
                 magnitude: float = 0, distributionType: SymbolicConstant = UNIFORM,
                 amplitude: str = UNSET, fixed: Boolean = OFF):
        """This method creates a MaterialFlowBC object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].MaterialFlowBC
        
        Parameters
        ----------
        name
            A String specifying the boundary condition repository key. 
        createStepName
            A String specifying the name of the step in which the boundary condition is created. 
        region
            A Region object specifying the region to which the boundary condition is applied. 
        fieldName
            A String specifying the name of the AnalyticalField object associated with this boundary 
            condition. The *fieldName* argument applies only when *distributionType*=FIELD. The 
            default value is an empty string. 
        magnitude
            A Float specifying the material flow magnitude. The default value is 0. The *magnitude* 
            argument is optional if *distributionType*=USER_DEFINED. 
        distributionType
            A SymbolicConstant specifying how the boundary condition is distributed spatially. 
            Possible values are UNIFORM, USER_DEFINED, and FIELD. The default value is UNIFORM. 
        amplitude
            A String or the SymbolicConstant UNSET specifying the name of the amplitude reference. 
            UNSET should be used if the boundary condition has no amplitude reference. The default 
            value is UNSET. You should provide the *amplitude* argument only if it is valid for the 
            specified step. 
        fixed
            A Boolean specifying whether the boundary condition should remain fixed at the current 
            values at the start of the step. The default value is OFF. 

        Returns
        -------
            A MaterialFlowBC object.
        """
        super().__init__()
        pass

    def setValues(self, fieldName: str = '', magnitude: float = 0, distributionType: SymbolicConstant = UNIFORM,
                  amplitude: str = UNSET, fixed: Boolean = OFF):
        """This method modifies the data for an existing MaterialFlowBC object in the step where it
        is created.
        
        Parameters
        ----------
        fieldName
            A String specifying the name of the AnalyticalField object associated with this boundary 
            condition. The *fieldName* argument applies only when *distributionType*=FIELD. The 
            default value is an empty string. 
        magnitude
            A Float specifying the material flow magnitude. The default value is 0. The *magnitude* 
            argument is optional if *distributionType*=USER_DEFINED. 
        distributionType
            A SymbolicConstant specifying how the boundary condition is distributed spatially. 
            Possible values are UNIFORM, USER_DEFINED, and FIELD. The default value is UNIFORM. 
        amplitude
            A String or the SymbolicConstant UNSET specifying the name of the amplitude reference. 
            UNSET should be used if the boundary condition has no amplitude reference. The default 
            value is UNSET. You should provide the *amplitude* argument only if it is valid for the 
            specified step. 
        fixed
            A Boolean specifying whether the boundary condition should remain fixed at the current 
            values at the start of the step. The default value is OFF. 
        """
        pass

    def setValuesInStep(self, stepName: str,
                        magnitude: typing.Union[SymbolicConstant, float] = UNCHANGED,
                        amplitude: str = ''):
        """This method modifies the propagating data for an existing MaterialFlowBC object in the
        specified step.
        
        Parameters
        ----------
        stepName
            A String specifying the name of the step in which the boundary condition is modified. 
        magnitude
            A Float or the SymbolicConstant FREED specifying the material flow magnitude. 
        amplitude
            A String or a SymbolicConstant specifying the name of the amplitude reference. Possible 
            values for the SymbolicConstant are UNCHANGED and FREED. UNCHANGED should be used if the 
            amplitude is propagated from the previous analysis step. FREED should be used if the 
            boundary condition is changed to have no amplitude reference. You should provide the 
            *amplitude* argument only if it is valid for the specified step. 
        """
        pass
