from abaqusConstants import *
from .Section import Section


class CohesiveSection(Section):
    """The CohesiveSection object defines the properties of a cohesive section.
    The CohesiveSection object is derived from the Section object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import section
        mdb.models[name].sections[name]
        import odbSection
        session.odbs[name].sections[name]

    The corresponding analysis keywords are:

    - COHESIVE SECTION

    """

    def __init__(self, name: str, response: SymbolicConstant, material: str,
                 initialThicknessType: SymbolicConstant = SOLVER_DEFAULT, initialThickness: float = 1,
                 outOfPlaneThickness: float = None):
        """This method creates a CohesiveSection object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].CohesiveSection
            session.odbs[name].CohesiveSection
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        response
            A SymbolicConstant specifying the geometric assumption that defines the constitutive 
            behavior of the cohesive elements. Possible values are TRACTION_SEPARATION, CONTINUUM, 
            and GASKET. 
        material
            A String specifying the name of the material. 
        initialThicknessType
            A SymbolicConstant specifying the method used to compute the initial thickness. Possible 
            values are:SOLVER_DEFAULT, specifying that Abaqus will use the analysis product 
            defaultGEOMETRY, specifying that Abaqus will compute the thickness from the nodal 
            coordinates of the elements.SPECIFY, specifying that Abaqus will use the value given for 
            *initialThickness*The default value is SOLVER_DEFAULT. 
        initialThickness
            A Float specifying the initial thickness for the section. The *initialThickness* 
            argument applies only when *initialThicknessType*=SPECIFY. The default value is 1.0. 
        outOfPlaneThickness
            None or a Float specifying the out-of-plane thickness for the section. The default value 
            is None. 

        Returns
        -------
            A CohesiveSection object. 

        Raises
        ------
            RangeError and InvalidNameError. 
        """
        super().__init__()
        pass

    def setValues(self, initialThicknessType: SymbolicConstant = SOLVER_DEFAULT, initialThickness: float = 1,
                  outOfPlaneThickness: float = None):
        """This method modifies the CohesiveSection object.
        
        Parameters
        ----------
        initialThicknessType
            A SymbolicConstant specifying the method used to compute the initial thickness. Possible 
            values are:SOLVER_DEFAULT, specifying that Abaqus will use the analysis product 
            defaultGEOMETRY, specifying that Abaqus will compute the thickness from the nodal 
            coordinates of the elements.SPECIFY, specifying that Abaqus will use the value given for 
            *initialThickness*The default value is SOLVER_DEFAULT. 
        initialThickness
            A Float specifying the initial thickness for the section. The *initialThickness* 
            argument applies only when *initialThicknessType*=SPECIFY. The default value is 1.0. 
        outOfPlaneThickness
            None or a Float specifying the out-of-plane thickness for the section. The default value 
            is None.

        Raises
        ------
        RangeError
        """
        pass
