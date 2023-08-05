import typing

from abaqusConstants import *
from .Section import Section


class GasketSection(Section):
    """The GasketSection object defines the properties of a gasket section.
    The GasketSection object is derived from the Section object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import section
        mdb.models[name].sections[name]
        import odbSection
        session.odbs[name].sections[name]

    The corresponding analysis keywords are:

    - GASKET SECTION

    """

    def __init__(self, name: str, material: str, crossSection: float = 1, initialGap: float = 0,
                 initialThickness: typing.Union[SymbolicConstant, float] = DEFAULT,
                 initialVoid: float = 0,
                 stabilizationStiffness: typing.Union[SymbolicConstant, float] = DEFAULT):
        """This method creates a GasketSection object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].GasketSection
            session.odbs[name].GasketSection
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        material
            A String specifying the name of the material of which the gasket is made or material 
            that defines gasket behavior. 
        crossSection
            A Float specifying the cross-sectional area, width, or out-of-plane thickness, if 
            applicable, depending on the gasket element type. The default value is 1.0. 
        initialGap
            A Float specifying the initial gap. The default value is 0.0. 
        initialThickness
            The SymbolicConstant DEFAULT or a Float specifying the initial gasket thickness. If 
            DEFAULT is specified, the initial thickness is determined using nodal coordinates. The 
            default value is DEFAULT. 
        initialVoid
            A Float specifying the initial void. The default value is 0.0. 
        stabilizationStiffness
            The SymbolicConstant DEFAULT or a Float specifying the default stabilization stiffness 
            used in all but link elements to stabilize gasket elements that are not supported at all 
            nodes, such as those that extend outside neighboring components. If DEFAULT is 
            specified, a value is used equal to 10–9 times the initial compressive stiffness in the 
            thickness direction. The default value is DEFAULT. 

        Returns
        -------
            A GasketSection object.  and ValueError. 
        """
        super().__init__()
        pass

    def setValues(self, crossSection: float = 1, initialGap: float = 0,
                  initialThickness: typing.Union[SymbolicConstant, float] = DEFAULT,
                  initialVoid: float = 0,
                  stabilizationStiffness: typing.Union[SymbolicConstant, float] = DEFAULT):
        """This method modifies the GasketSection object.
        
        Parameters
        ----------
        crossSection
            A Float specifying the cross-sectional area, width, or out-of-plane thickness, if 
            applicable, depending on the gasket element type. The default value is 1.0. 
        initialGap
            A Float specifying the initial gap. The default value is 0.0. 
        initialThickness
            The SymbolicConstant DEFAULT or a Float specifying the initial gasket thickness. If 
            DEFAULT is specified, the initial thickness is determined using nodal coordinates. The 
            default value is DEFAULT. 
        initialVoid
            A Float specifying the initial void. The default value is 0.0. 
        stabilizationStiffness
            The SymbolicConstant DEFAULT or a Float specifying the default stabilization stiffness 
            used in all but link elements to stabilize gasket elements that are not supported at all 
            nodes, such as those that extend outside neighboring components. If DEFAULT is 
            specified, a value is used equal to 10–9 times the initial compressive stiffness in the 
            thickness direction. The default value is DEFAULT.

        Raises
        ------
            ValueError. 
        """
        pass
