from abaqusConstants import *
from .RebarLayers import RebarLayers
from .ShellSection import ShellSection
from .TransverseShearShell import TransverseShearShell


class GeneralStiffnessSection(ShellSection):
    """The GeneralStiffnessSection object defines the properties of a shell section via the
    stiffness matrix. 
    The GeneralStiffnessSection object is derived from the ShellSection object. 

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
        mdb.models[name].sections[name]
        import odbSection
        session.odbs[name].sections[name]

    The corresponding analysis keywords are:

    - SHELL GENERAL SECTION

    """

    # A RebarLayers object specifying reinforcement properties. 
    rebarLayers: RebarLayers = None

    # A TransverseShearShell object specifying the transverse shear stiffness properties. 
    transverseShear: TransverseShearShell = None

    def __init__(self, name: str, stiffnessMatrix: tuple, referenceTemperature: float = None,
                 applyThermalStress: Boolean = OFF, temperatureDependency: Boolean = OFF,
                 dependencies: int = 0, poissonDefinition: SymbolicConstant = DEFAULT,
                 poisson: float = 0, useDensity: Boolean = OFF, density: float = 0,
                 thermalStresses: tuple = (), scalingData: tuple = ()):
        """This method creates a GeneralStiffnessSection object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].GeneralStiffnessSection
            session.odbs[name].GeneralStiffnessSection
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        stiffnessMatrix
            A sequence of Floats specifying the stiffness matrix for the section in the order D11, 
            D12, D22, D13, D23, D33, ...., D66. Twenty-one entries must be given. 
        referenceTemperature
            None or a Float specifying the reference temperature for thermal expansion. The default 
            value is None. 
        applyThermalStress
            A Boolean specifying whether or not the section stiffness varies with thermal stresses. 
            The default value is OFF. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        poissonDefinition
            A SymbolicConstant specifying whether to use the default value for the Poisson's ratio. 
            Possible values are:DEFAULT, specifying that the default value for the Poisson's ratio 
            is 0.5 in an Abaqus/Standard analysis and is obtained from the material definition in an 
            Abaqus/Explicit analysis.VALUE, specifying that the Poisson's ratio used in the analysis 
            is the value provided in *poisson*.The default value is DEFAULT. 
        poisson
            A Float specifying the Poisson's ratio. Possible values are −1.0 ≤≤ *poisson* ≤≤ 0.5. 
            This argument is valid only when *poissonDefinition*=VALUE. The default value is 0.5. 
        useDensity
            A Boolean specifying whether or not to use the value of *density*. The default value is 
            OFF. 
        density
            A Float specifying the value of density to apply to this section. The default value is 
            0.0. 
        thermalStresses
            A sequence of Floats specifying the generalized stress values caused by a unit 
            temperature rise. Six entries must be given if the value of *applyThermalStress* is set 
            to True. The default value is (""). 
        scalingData
            A sequence of sequences of Floats specifying the scaling factors for given temperatures 
            and/or field data. Each row should contain (Y, alpha, T, F1,...,Fn). The default value 
            is an empty sequence. 

        Returns
        -------
            A GeneralStiffnessSection object.
        """
        super().__init__()
        pass

    def setValues(self, referenceTemperature: float = None, applyThermalStress: Boolean = OFF,
                  temperatureDependency: Boolean = OFF, dependencies: int = 0,
                  poissonDefinition: SymbolicConstant = DEFAULT, poisson: float = 0,
                  useDensity: Boolean = OFF, density: float = 0, thermalStresses: tuple = (),
                  scalingData: tuple = ()):
        """This method modifies the GeneralStiffnessSection object.
        
        Parameters
        ----------
        referenceTemperature
            None or a Float specifying the reference temperature for thermal expansion. The default 
            value is None. 
        applyThermalStress
            A Boolean specifying whether or not the section stiffness varies with thermal stresses. 
            The default value is OFF. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        poissonDefinition
            A SymbolicConstant specifying whether to use the default value for the Poisson's ratio. 
            Possible values are:DEFAULT, specifying that the default value for the Poisson's ratio 
            is 0.5 in an Abaqus/Standard analysis and is obtained from the material definition in an 
            Abaqus/Explicit analysis.VALUE, specifying that the Poisson's ratio used in the analysis 
            is the value provided in *poisson*.The default value is DEFAULT. 
        poisson
            A Float specifying the Poisson's ratio. Possible values are −1.0 ≤≤ *poisson* ≤≤ 0.5. 
            This argument is valid only when *poissonDefinition*=VALUE. The default value is 0.5. 
        useDensity
            A Boolean specifying whether or not to use the value of *density*. The default value is 
            OFF. 
        density
            A Float specifying the value of density to apply to this section. The default value is 
            0.0. 
        thermalStresses
            A sequence of Floats specifying the generalized stress values caused by a unit 
            temperature rise. Six entries must be given if the value of *applyThermalStress* is set 
            to True. The default value is (""). 
        scalingData
            A sequence of sequences of Floats specifying the scaling factors for given temperatures 
            and/or field data. Each row should contain (Y, alpha, T, F1,...,Fn). The default value 
            is an empty sequence. 
        """
        pass
