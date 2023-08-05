from abaqusConstants import *
from .GeometryShellSection import GeometryShellSection
from .RebarLayers import RebarLayers
from .SectionLayerArray import SectionLayerArray
from .TransverseShearShell import TransverseShearShell


class CompositeShellSection(GeometryShellSection):
    """The CompositeShellSection object defines the properties of a composite shell section.
    The CompositeShellSection object is derived from the GeometryShellSection object. 

    Attributes
    ----------
    rebarLayers: RebarLayers
        A :py:class:`~abaqus.Section.RebarLayers.RebarLayers` object specifying reinforcement properties.
    transverseShear: TransverseShearShell
        A :py:class:`~abaqus.Section.TransverseShearShell.TransverseShearShell` object specifying the transverse shear stiffness properties.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import section
        mdb.models[name].parts[name].compositeLayups[i].section
        mdb.models[name].sections[name]
        import odbSection
        session.odbs[name].sections[name]

    The corresponding analysis keywords are:

    - SHELL SECTION
            - SHELL GENERAL SECTION

    """

    # A RebarLayers object specifying reinforcement properties. 
    rebarLayers: RebarLayers = None

    # A TransverseShearShell object specifying the transverse shear stiffness properties. 
    transverseShear: TransverseShearShell = None

    def __init__(self, name: str, layup: SectionLayerArray, symmetric: Boolean = OFF,
                 thicknessType: SymbolicConstant = UNIFORM, preIntegrate: Boolean = OFF,
                 poissonDefinition: SymbolicConstant = DEFAULT, poisson: float = 0,
                 integrationRule: SymbolicConstant = SIMPSON, temperature: SymbolicConstant = GRADIENT,
                 idealization: SymbolicConstant = NO_IDEALIZATION, nTemp: int = None,
                 thicknessModulus: float = None, useDensity: Boolean = OFF, density: float = 0,
                 layupName: str = '', thicknessField: str = '', nodalThicknessField: str = ''):
        """This method creates a CompositeShellSection object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].parts[name].compositeLayups[i].CompositeShellSection
            mdb.models[name].CompositeShellSection
            session.odbs[name].CompositeShellSection
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        layup
            A SectionLayerArray object specifying the shell cross-section. 
        symmetric
            A Boolean specifying whether or not the layup should be made symmetric by the analysis. 
            The default value is OFF. 
        thicknessType
            A SymbolicConstant specifying the distribution used for defining the thickness of the 
            elements. Possible values are UNIFORM, ANALYTICAL_FIELD, DISCRETE_FIELD, 
            NODAL_ANALYTICAL_FIELD, and NODAL_DISCRETE_FIELD. The default value is UNIFORM. 
        preIntegrate
            A Boolean specifying whether the shell section properties are specified by the user 
            prior to the analysis (ON) or integrated during the analysis (OFF). The default value is 
            OFF. 
        poissonDefinition
            A SymbolicConstant specifying whether to use the default value for the Poisson's ratio. 
            Possible values are:DEFAULT, specifying that the default value for the Poisson's ratio 
            is 0.5 in an Abaqus/Standard analysis and is obtained from the material definition in an 
            Abaqus/Explicit analysis.VALUE, specifying that the Poisson's ratio used in the analysis 
            is the value provided in *poisson*.The default value is DEFAULT. 
        poisson
            A Float specifying the Poisson's ratio. Possible values are −1.0 ≤≤ *poisson* ≤≤ 0.5. 
            This argument is valid only when *poissonDefinition*=VALUE. The default value is 0.5. 
        integrationRule
            A SymbolicConstant specifying the shell section integration rule. Possible values are 
            SIMPSON and GAUSS. The default value is SIMPSON. 
        temperature
            A SymbolicConstant specifying the mode used for temperature and field variable input 
            across the section thickness. Possible values are GRADIENT and POINTWISE. The default 
            value is GRADIENT. 
        idealization
            A SymbolicConstant specifying the mechanical idealization used for the section 
            calculations. This member is only applicable when *preIntegrate* is set to ON. Possible 
            values are NO_IDEALIZATION, SMEAR_ALL_LAYERS, MEMBRANE, and BENDING. The default value 
            is NO_IDEALIZATION. 
        nTemp
            None or an Int specifying the number of temperature points to be input. This argument is 
            valid only when *temperature*=POINTWISE. The default value is None. 
        thicknessModulus
            None or a Float specifying the effective thickness modulus. This argument is relevant 
            only for continuum shells and must be used in conjunction with the argument *poisson*. 
            The default value is None. 
        useDensity
            A Boolean specifying whether or not to use the value of *density*. The default value is 
            OFF. 
        density
            A Float specifying the value of density to apply to this section. The default value is 
            0.0. 
        layupName
            A String specifying the layup name for this section. The default value is an empty 
            string. 
        thicknessField
            A String specifying the name of the AnalyticalField or DiscreteField object used to 
            define the thickness of the shell elements. The *thicknessField* argument applies only 
            when *thicknessType*=ANALYTICAL_FIELD or *thicknessType*=DISCRETE_FIELD. The default 
            value is an empty string. 
        nodalThicknessField
            A String specifying the name of the AnalyticalField or DiscreteField object used to 
            define the thickness of the shell elements at each node. The *nodalThicknessField* 
            argument applies only when *thicknessType*=NODAL_ANALYTICAL_FIELD or 
            *thicknessType*=NODAL_DISCRETE_FIELD. The default value is an empty string. 

        Returns
        -------
            A CompositeShellSection object.
        """
        super().__init__()
        pass

    def setValues(self, symmetric: Boolean = OFF, thicknessType: SymbolicConstant = UNIFORM,
                  preIntegrate: Boolean = OFF, poissonDefinition: SymbolicConstant = DEFAULT,
                  poisson: float = 0, integrationRule: SymbolicConstant = SIMPSON,
                  temperature: SymbolicConstant = GRADIENT,
                  idealization: SymbolicConstant = NO_IDEALIZATION, nTemp: int = None,
                  thicknessModulus: float = None, useDensity: Boolean = OFF, density: float = 0,
                  layupName: str = '', thicknessField: str = '', nodalThicknessField: str = ''):
        """This method modifies the CompositeShellSection object.
        
        Parameters
        ----------
        symmetric
            A Boolean specifying whether or not the layup should be made symmetric by the analysis. 
            The default value is OFF. 
        thicknessType
            A SymbolicConstant specifying the distribution used for defining the thickness of the 
            elements. Possible values are UNIFORM, ANALYTICAL_FIELD, DISCRETE_FIELD, 
            NODAL_ANALYTICAL_FIELD, and NODAL_DISCRETE_FIELD. The default value is UNIFORM. 
        preIntegrate
            A Boolean specifying whether the shell section properties are specified by the user 
            prior to the analysis (ON) or integrated during the analysis (OFF). The default value is 
            OFF. 
        poissonDefinition
            A SymbolicConstant specifying whether to use the default value for the Poisson's ratio. 
            Possible values are:DEFAULT, specifying that the default value for the Poisson's ratio 
            is 0.5 in an Abaqus/Standard analysis and is obtained from the material definition in an 
            Abaqus/Explicit analysis.VALUE, specifying that the Poisson's ratio used in the analysis 
            is the value provided in *poisson*.The default value is DEFAULT. 
        poisson
            A Float specifying the Poisson's ratio. Possible values are −1.0 ≤≤ *poisson* ≤≤ 0.5. 
            This argument is valid only when *poissonDefinition*=VALUE. The default value is 0.5. 
        integrationRule
            A SymbolicConstant specifying the shell section integration rule. Possible values are 
            SIMPSON and GAUSS. The default value is SIMPSON. 
        temperature
            A SymbolicConstant specifying the mode used for temperature and field variable input 
            across the section thickness. Possible values are GRADIENT and POINTWISE. The default 
            value is GRADIENT. 
        idealization
            A SymbolicConstant specifying the mechanical idealization used for the section 
            calculations. This member is only applicable when *preIntegrate* is set to ON. Possible 
            values are NO_IDEALIZATION, SMEAR_ALL_LAYERS, MEMBRANE, and BENDING. The default value 
            is NO_IDEALIZATION. 
        nTemp
            None or an Int specifying the number of temperature points to be input. This argument is 
            valid only when *temperature*=POINTWISE. The default value is None. 
        thicknessModulus
            None or a Float specifying the effective thickness modulus. This argument is relevant 
            only for continuum shells and must be used in conjunction with the argument *poisson*. 
            The default value is None. 
        useDensity
            A Boolean specifying whether or not to use the value of *density*. The default value is 
            OFF. 
        density
            A Float specifying the value of density to apply to this section. The default value is 
            0.0. 
        layupName
            A String specifying the layup name for this section. The default value is an empty 
            string. 
        thicknessField
            A String specifying the name of the AnalyticalField or DiscreteField object used to 
            define the thickness of the shell elements. The *thicknessField* argument applies only 
            when *thicknessType*=ANALYTICAL_FIELD or *thicknessType*=DISCRETE_FIELD. The default 
            value is an empty string. 
        nodalThicknessField
            A String specifying the name of the AnalyticalField or DiscreteField object used to 
            define the thickness of the shell elements at each node. The *nodalThicknessField* 
            argument applies only when *thicknessType*=NODAL_ANALYTICAL_FIELD or 
            *thicknessType*=NODAL_DISCRETE_FIELD. The default value is an empty string. 
        """
        pass
