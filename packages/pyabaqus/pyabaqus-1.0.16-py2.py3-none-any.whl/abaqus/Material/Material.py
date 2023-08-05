import typing

from abaqusConstants import *
from .Density.Density import Density
from .Elastic.HyperElastic.HyperFoam.Hyperfoam import Hyperfoam
from .Elastic.HyperElastic.Hyperelastic import Hyperelastic
from .Elastic.HyperElastic.ViscoElastic.Viscoelastic import Viscoelastic
from .Elastic.HypoElastic.Hypoelastic import Hypoelastic
from .Elastic.Linear.Elastic import Elastic
from .Elastic.LowDensityFoam.LowDensityFoam import LowDensityFoam
from .Elastic.Porous.PorousElastic import PorousElastic
from .Eos.Eos import Eos
from .Gap.GapFlow import GapFlow
from .Gasket.GasketMembraneElastic import GasketMembraneElastic
from .Gasket.GasketThicknessBehavior import GasketThicknessBehavior
from .Gasket.GasketTransverseShearElastic import GasketTransverseShearElastic
from .MaterialBase import MaterialBase
from .Others.Acoustic.AcousticMedium import AcousticMedium
from .Others.Electromagnetic.Dielectric import Dielectric
from .Others.Electromagnetic.ElectricalConductivity import ElectricalConductivity
from .Others.Electromagnetic.MagneticPermeability import MagneticPermeability
from .Others.Electromagnetic.Piezoelectric import Piezoelectric
from .Others.HeatTransfer.Conductivity import Conductivity
from .Others.HeatTransfer.InelasticHeatFraction import InelasticHeatFraction
from .Others.HeatTransfer.JouleHeatFraction import JouleHeatFraction
from .Others.HeatTransfer.LatentHeat import LatentHeat
from .Others.HeatTransfer.SpecificHeat import SpecificHeat
from .Others.MassDiffusion.Diffusivity import Diffusivity
from .Others.MassDiffusion.Solubility import Solubility
from .Others.Mechanical.Damping import Damping
from .Others.Mechanical.Expansion import Expansion
from .Others.Mechanical.PoreFluidExpansion import PoreFluidExpansion
from .Others.Mechanical.Viscosity.Viscosity import Viscosity
from .Others.PoreFluidFlow.FluidLeakoff import FluidLeakoff
from .Others.PoreFluidFlow.Gel import Gel
from .Others.PoreFluidFlow.MoistureSwelling.MoistureSwelling import MoistureSwelling
from .Others.PoreFluidFlow.Permeability.Permeability import Permeability
from .Others.PoreFluidFlow.PorousBulkModuli import PorousBulkModuli
from .Others.PoreFluidFlow.Sorption import Sorption
from .Others.User.Depvar import Depvar
from .Others.User.UserMaterial import UserMaterial
from .Others.User.UserOutputVariables import UserOutputVariables
from .Plastic.Concrete.BrittleCracking import BrittleCracking
from .Plastic.Concrete.Concrete import Concrete
from .Plastic.Concrete.ConcreteDamagedPlasticity import ConcreteDamagedPlasticity
from .Plastic.Creep.Creep import Creep
from .Plastic.CriticalStateClay.ClayPlasticity import ClayPlasticity
from .Plastic.CrushableFoam.CrushableFoam import CrushableFoam
from .Plastic.DruckerPrager.Extended.DruckerPrager import DruckerPrager
from .Plastic.DruckerPrager.ModifiedCap.CapPlasticity import CapPlasticity
from .Plastic.Metal.CastIron.CastIronPlasticity import CastIronPlasticity
from .Plastic.Metal.Deformation.DeformationPlasticity import DeformationPlasticity
from .Plastic.Metal.Porous.PorousMetalPlasticity import PorousMetalPlasticity
from .Plastic.Metal.TwoLayerViscoPlasticity.Viscous import Viscous
from .Plastic.MohrCoulomb.MohrCoulombPlasticity import MohrCoulombPlasticity
from .Plastic.Plastic import Plastic
from .Plastic.Swelling.Swelling import Swelling
from .Regularization import Regularization


class Material(MaterialBase):
    """A Material object is the object used to specify a material. The Material object stores
    the various settings that determine how a material behaves. 
    A material is created by combining one or more individual material options and sub 
    options. A particular material option is associated with the Material object through a 
    member. For example: the *acousticMedium* member may contain an AcousticMedium object. 
    The alternative of having a MaterialOption abstract base class and a container of 
    MaterialOptions was rejected because it would make it more difficult to enforce the fact 
    that one Material object cannot contain two AcousticMedium objects, for example. 

    Attributes
    ----------
    acousticMedium: AcousticMedium
        An :py:class:`~abaqus.Material.Others.Acoustic.AcousticMedium.AcousticMedium` object.
    brittleCracking: BrittleCracking
        A :py:class:`~abaqus.Material.Plastic.Concrete.BrittleCracking.BrittleCracking` object.
    capPlasticity: CapPlasticity
        A :py:class:`~abaqus.Material.Plastic.DruckerPrager.ModifiedCap.CapPlasticity.CapPlasticity` object.
    castIronPlasticity: CastIronPlasticity
        A :py:class:`~abaqus.Material.Plastic.Metal.CastIron.CastIronPlasticity.CastIronPlasticity` object.
    clayPlasticity: ClayPlasticity
        A :py:class:`~abaqus.Material.Plastic.CriticalStateClay.ClayPlasticity.ClayPlasticity` object.
    concrete: Concrete
        A :py:class:`~abaqus.Material.Plastic.Concrete.Concrete.Concrete` object.
    concreteDamagedPlasticity: ConcreteDamagedPlasticity
        A :py:class:`~abaqus.Material.Plastic.Concrete.ConcreteDamagedPlasticity.ConcreteDamagedPlasticity` object.
    conductivity: Conductivity
        A :py:class:`~abaqus.Material.Others.HeatTransfer.Conductivity.Conductivity` object.
    creep: Creep
        A :py:class:`~abaqus.Material.Plastic.Creep.Creep.Creep` object.
    crushableFoam: CrushableFoam
        A :py:class:`~abaqus.Material.Plastic.CrushableFoam.CrushableFoam.CrushableFoam` object.
    ductileDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    fldDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    flsdDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    johnsonCookDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    maxeDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    maxsDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    maxpeDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    maxpsDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    mkDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    msfldDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    quadeDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    quadsDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    shearDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    hashinDamageInitiation: DamageInitiation
        A :py:class:`~abaqus.Material.ProgressiveDamageFailure.DamageInitiation.DamageInitiation` object.
    damping: Damping
        A :py:class:`~abaqus.Material.Others.Mechanical.Damping.Damping` object.
    deformationPlasticity: DeformationPlasticity
        A :py:class:`~abaqus.Material.Plastic.Metal.Deformation.DeformationPlasticity.DeformationPlasticity` object.
    density: Density
        A :py:class:`~abaqus.Material.Density.Density.Density` object.
    depvar: Depvar
        A :py:class:`~abaqus.Material.Others.User.Depvar.Depvar` object.
    dielectric: Dielectric
        A :py:class:`~abaqus.Material.Others.Electromagnetic.Dielectric.Dielectric` object.
    diffusivity: Diffusivity
        A :py:class:`~abaqus.Material.Others.MassDiffusion.Diffusivity.Diffusivity` object.
    druckerPrager: DruckerPrager
        A :py:class:`~abaqus.Material.Plastic.DruckerPrager.Extended.DruckerPrager.DruckerPrager` object.
    elastic: Elastic
        An :py:class:`~abaqus.Material.Elastic.Linear.Elastic.Elastic` object.
    electricalConductivity: ElectricalConductivity
        An :py:class:`~abaqus.Material.Others.Electromagnetic.ElectricalConductivity.ElectricalConductivity` object.
    eos: Eos
        An :py:class:`~abaqus.Material.Eos.Eos.Eos` object.
    expansion: Expansion
        An :py:class:`~abaqus.Material.Others.Mechanical.Expansion.Expansion` object.
    fluidLeakoff: FluidLeakoff
        A :py:class:`~abaqus.Material.Others.PoreFluidFlow.FluidLeakoff.FluidLeakoff` object.
    gapFlow: GapFlow
        A :py:class:`~abaqus.Material.Gap.GapFlow.GapFlow` object.
    gasketThicknessBehavior: GasketThicknessBehavior
        A :py:class:`~abaqus.Material.Gasket.GasketThicknessBehavior.GasketThicknessBehavior` object.
    gasketTransverseShearElastic: GasketTransverseShearElastic
        A :py:class:`~abaqus.Material.Gasket.GasketTransverseShearElastic.GasketTransverseShearElastic` object.
    gasketMembraneElastic: GasketMembraneElastic
        A :py:class:`~abaqus.Material.Gasket.GasketMembraneElastic.GasketMembraneElastic` object.
    gel: Gel
        A :py:class:`~abaqus.Material.Others.PoreFluidFlow.Gel.Gel` object.
    heatGeneration: HeatGeneration
        A :py:class:`~abaqus.Material.Others.HeatTransfer.HeatGeneration.HeatGeneration` object.
    hyperelastic: Hyperelastic
        A :py:class:`~abaqus.Material.Elastic.HyperElastic.Hyperelastic.Hyperelastic` object.
    hyperfoam: Hyperfoam
        A :py:class:`~abaqus.Material.Elastic.HyperElastic.HyperFoam.Hyperfoam.Hyperfoam` object.
    hypoelastic: Hypoelastic
        A :py:class:`~abaqus.Material.Elastic.HypoElastic.Hypoelastic.Hypoelastic` object.
    inelasticHeatFraction: InelasticHeatFraction
        An :py:class:`~abaqus.Material.Others.HeatTransfer.InelasticHeatFraction.InelasticHeatFraction` object.
    jouleHeatFraction: JouleHeatFraction
        A :py:class:`~abaqus.Material.Others.HeatTransfer.JouleHeatFraction.JouleHeatFraction` object.
    latentHeat: LatentHeat
        A :py:class:`~abaqus.Material.Others.HeatTransfer.LatentHeat.LatentHeat` object.
    lowDensityFoam: LowDensityFoam
        A :py:class:`~abaqus.Material.Elastic.LowDensityFoam.LowDensityFoam.LowDensityFoam` object.
    magneticPermeability: MagneticPermeability
        A :py:class:`~abaqus.Material.Others.Electromagnetic.MagneticPermeability.MagneticPermeability` object.
    mohrCoulombPlasticity: MohrCoulombPlasticity
        A :py:class:`~abaqus.Material.Plastic.MohrCoulomb.MohrCoulombPlasticity.MohrCoulombPlasticity` object.
    moistureSwelling: MoistureSwelling
        A :py:class:`~abaqus.Material.Others.PoreFluidFlow.MoistureSwelling.MoistureSwelling.MoistureSwelling` object.
    mullinsEffect: MullinsEffect
        A :py:class:`~abaqus.Material.TestData.MullinsEffect.MullinsEffect` object.
    permeability: Permeability
        A :py:class:`~abaqus.Material.Others.PoreFluidFlow.Permeability.Permeability.Permeability` object.
    piezoelectric: Piezoelectric
        A :py:class:`~abaqus.Material.Others.Electromagnetic.Piezoelectric.Piezoelectric` object.
    plastic: Plastic
        A :py:class:`~abaqus.Material.Plastic.Plastic.Plastic` object.
    poreFluidExpansion: PoreFluidExpansion
        A :py:class:`~abaqus.Material.Others.Mechanical.PoreFluidExpansion.PoreFluidExpansion` object.
    porousBulkModuli: PorousBulkModuli
        A :py:class:`~abaqus.Material.Others.PoreFluidFlow.PorousBulkModuli.PorousBulkModuli` object.
    porousElastic: PorousElastic
        A :py:class:`~abaqus.Material.Elastic.Porous.PorousElastic.PorousElastic` object.
    porousMetalPlasticity: PorousMetalPlasticity
        A :py:class:`~abaqus.Material.Plastic.Metal.Porous.PorousMetalPlasticity.PorousMetalPlasticity` object.
    regularization: Regularization
        A :py:class:`~abaqus.Material.Regularization.Regularization` object.
    solubility: Solubility
        A :py:class:`~abaqus.Material.Others.MassDiffusion.Solubility.Solubility` object.
    sorption: Sorption
        A :py:class:`~abaqus.Material.Others.PoreFluidFlow.Sorption.Sorption` object.
    specificHeat: SpecificHeat
        A :py:class:`~abaqus.Material.Others.HeatTransfer.SpecificHeat.SpecificHeat` object.
    swelling: Swelling
        A :py:class:`~abaqus.Material.Plastic.Swelling.Swelling.Swelling` object.
    userDefinedField: UserDefinedField
        A :py:class:`~abaqus.Material.Others.User.UserDefinedField.UserDefinedField` object.
    userMaterial: UserMaterial
        A :py:class:`~abaqus.Material.Others.User.UserMaterial.UserMaterial` object.
    userOutputVariables: UserOutputVariables
        A :py:class:`~abaqus.Material.Others.User.UserOutputVariables.UserOutputVariables` object.
    viscoelastic: Viscoelastic
        A :py:class:`~abaqus.Material.Elastic.HyperElastic.ViscoElastic.Viscoelastic.Viscoelastic` object.
    viscosity: Viscosity
        A :py:class:`~abaqus.Material.Others.Mechanical.Viscosity.Viscosity.Viscosity` object.
    viscous: Viscous
        A :py:class:`~abaqus.Material.Plastic.Metal.TwoLayerViscoPlasticity.Viscous.Viscous` object.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name]
        import odbMaterial
        session.odbs[name].materials[name]

    The corresponding analysis keywords are:

    - MATERIAL

    """

    def AcousticMedium(self, acousticVolumetricDrag: Boolean = OFF, temperatureDependencyB: Boolean = OFF,
                       temperatureDependencyV: Boolean = OFF, dependenciesB: int = 0, dependenciesV: int = 0,
                       bulkTable: tuple = (), volumetricTable: tuple = ()) -> AcousticMedium:
        """This method creates an AcousticMedium object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].AcousticMedium
                session.odbs[name].materials[name].AcousticMedium
        
        Parameters
        ----------
        acousticVolumetricDrag
            A Boolean specifying whether the volumetricTable data is specified. The default value is 
            OFF. 
        temperatureDependencyB
            A Boolean specifying whether the data in *bulkTable* depend on temperature. The default 
            value is OFF. 
        temperatureDependencyV
            A Boolean specifying whether the data in *volumetricTable* depend on temperature. The 
            default value is OFF. 
        dependenciesB
            An Int specifying the number of field variable dependencies for the data in *bulkTable*. 
            The default value is 0. 
        dependenciesV
            An Int specifying the number of field variable dependencies for the data in 
            *volumetricTable*. The default value is 0. 
        bulkTable
            A sequence of sequences of Floats specifying the following: 
            - Bulk modulus. 
            - Temperature, if the data depend on temperature. 
            - Value of the first field variable, if the data depend on field variables. 
            - Value of the second field variable. 
            - Etc. 
        volumetricTable
            A sequence of sequences of Floats specifying the following: 
            - Volumetric drag. 
            - Frequency. 
            - Temperature, if the data depend on temperature. 
            - Value of the first field variable, if the data depend on field variables. 
            - Value of the second field variable. 
            - Etc. 
            The default value is an empty sequence. 

        Returns
        -------
            An AcousticMedium object. 

        Raises
        ------
        RangeError
        """
        self.acousticMedium = AcousticMedium(acousticVolumetricDrag, temperatureDependencyB, temperatureDependencyV,
                                             dependenciesB, dependenciesV, bulkTable, volumetricTable)
        return self.acousticMedium

    def BrittleCracking(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0,
                        type: SymbolicConstant = STRAIN) -> BrittleCracking:
        """This method creates a BrittleCracking object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].BrittleCracking
                session.odbs[name].materials[name].BrittleCracking
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        type
            A SymbolicConstant specifying the type of postcracking behavior. Possible values are 
            STRAIN, DISPLACEMENT, and GFI. The default value is STRAIN. 

        Returns
        -------
            A BrittleCracking object.
        """
        self.brittleCracking = BrittleCracking(table, temperatureDependency, dependencies, type)
        return self.brittleCracking

    def CapPlasticity(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0) -> CapPlasticity:
        """This method creates a CapPlasticity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].CapPlasticity
                session.odbs[name].materials[name].CapPlasticity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A CapPlasticity object. 

        Raises
        ------
        RangeError
        """
        self.capPlasticity = CapPlasticity(table, temperatureDependency, dependencies)
        return self.capPlasticity

    def CastIronPlasticity(self, table: tuple, temperatureDependency: Boolean = OFF,
                           dependencies: int = 0) -> CastIronPlasticity:
        """This method creates a CastIronPlasticity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].CastIronPlasticity
                session.odbs[name].materials[name].CastIronPlasticity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A CastIronPlasticity object. 

        Raises
        ------
        RangeError
        """
        self.castIronPlasticity = CastIronPlasticity(table, temperatureDependency, dependencies)
        return self.castIronPlasticity

    def ClayPlasticity(self, table: tuple, intercept: float = None, hardening: SymbolicConstant = EXPONENTIAL,
                       temperatureDependency: Boolean = OFF, dependencies: int = 0) -> ClayPlasticity:
        """This method creates a ClayPlasticity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].ClayPlasticity
                session.odbs[name].materials[name].ClayPlasticity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        intercept
            None or a Float specifying e1e1, the intercept of the virgin consolidation line with the 
            void ratio axis in a plot of void ratio versus the logarithm of pressure stress. The 
            default value is None.This argument is valid only if *hardening*=EXPONENTIAL. 
        hardening
            A SymbolicConstant specifying the type of hardening/softening definition. Possible 
            values are EXPONENTIAL and TABULAR. The default value is EXPONENTIAL. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A ClayPlasticity object. 

        Raises
        ------
        RangeError
        """
        self.clayPlasticity = ClayPlasticity(table, intercept, hardening, temperatureDependency, dependencies)
        return self.clayPlasticity

    def Concrete(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0) -> Concrete:
        """This method creates a Concrete object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Concrete
                session.odbs[name].materials[name].Concrete
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Concrete object. 

        Raises
        ------
        RangeError
        """
        self.concrete = Concrete(table, temperatureDependency, dependencies)
        return self.concrete

    def ConcreteDamagedPlasticity(self, table: tuple, temperatureDependency: Boolean = OFF,
                                  dependencies: int = 0) -> ConcreteDamagedPlasticity:
        """This method creates a ConcreteDamagedPlasticity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].ConcreteDamagedPlasticity
                session.odbs[name].materials[name].ConcreteDamagedPlasticity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A ConcreteDamagedPlasticity object. 

        Raises
        ------
        RangeError
        """
        self.concreteDamagedPlasticity = ConcreteDamagedPlasticity(table, temperatureDependency, dependencies)
        return self.concreteDamagedPlasticity

    def Conductivity(self, table: tuple, type: SymbolicConstant = ISOTROPIC, temperatureDependency: Boolean = OFF,
                     dependencies: int = 0) -> Conductivity:
        """This method creates a Conductivity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Conductivity
                session.odbs[name].materials[name].Conductivity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        type
            A SymbolicConstant specifying the type of conductivity. Possible values are ISOTROPIC, 
            ORTHOTROPIC, and ANISOTROPIC. The default value is ISOTROPIC. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Conductivity object. 

        Raises
        ------
        RangeError
        """
        self.conductivity = Conductivity(table, type, temperatureDependency, dependencies)
        return self.conductivity

    def Creep(self, table: tuple, law: SymbolicConstant = STRAIN, temperatureDependency: Boolean = OFF,
              dependencies: int = 0, time: SymbolicConstant = TOTAL) -> Creep:
        """This method creates a Creep object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Creep
                session.odbs[name].materials[name].Creep
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        law
            A SymbolicConstant specifying the strain-hardening law. Possible values are STRAIN, 
            TIME, HYPERBOLIC_SINE, USER, ANAND, DARVEAUX,DOUBLE_POWER, POWER_LAW, and 
            TIME_POWER_LAW. The default value is STRAIN. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        time
            A SymbolicConstant specifying the time interval for relevant laws. Possible values are 
            CREEP and TOTAL. The default value is TOTAL. 

        Returns
        -------
            A Creep object. 

        Raises
        ------
        RangeError
        """
        self.creep = Creep(table, law, temperatureDependency, dependencies, time)
        return self.creep

    def CrushableFoam(self, table: tuple, hardening: SymbolicConstant = VOLUMETRIC,
                      temperatureDependency: Boolean = OFF, dependencies: int = 0) -> CrushableFoam:
        """This method creates a CrushableFoam object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].CrushableFoam
                session.odbs[name].materials[name].CrushableFoam
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        hardening
            A SymbolicConstant specifying the type of hardening/softening definition. Possible 
            values are VOLUMETRIC and ISOTROPIC. The default value is VOLUMETRIC. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A CrushableFoam object. 

        Raises
        ------
        RangeError
        """
        self.crushableFoam = CrushableFoam(table, hardening, temperatureDependency, dependencies)
        return self.crushableFoam

    def Damping(self, alpha: float = 0, beta: float = 0, composite: float = 0, structural: float = 0) -> Damping:
        """This method creates a Damping object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Damping
                session.odbs[name].materials[name].Damping
        
        Parameters
        ----------
        alpha
            A Float specifying the αRαR factor to create mass proportional damping in 
            direct-integration and explicit dynamics. The default value is 0.0. 
        beta
            A Float specifying the βRβR factor to create stiffness proportional damping in 
            direct-integration and explicit dynamics. The default value is 0.0. 
        composite
            A Float specifying the fraction of critical damping to be used with this material in 
            calculating composite damping factors for the modes (for use in modal dynamics). The 
            default value is 0.0.This argument applies only to Abaqus/Standard analyses. 
        structural
            A Float specifying the structural factor to create material damping in 
            direct-integration and explicit dynamics. The default value is 0.0. 

        Returns
        -------
            A Damping object. 

        Raises
        ------
        RangeError
        """
        self.damping = Damping(alpha, beta, composite, structural)
        return self.damping

    def DeformationPlasticity(self, table: tuple, temperatureDependency: Boolean = OFF) -> DeformationPlasticity:
        """This method creates a DeformationPlasticity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].DeformationPlasticity
                session.odbs[name].materials[name].DeformationPlasticity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 

        Returns
        -------
            A DeformationPlasticity object. 

        Raises
        ------
        RangeError
        """
        self.deformationPlasticity = DeformationPlasticity(table, temperatureDependency)
        return self.deformationPlasticity

    def Density(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0,
                distributionType: SymbolicConstant = UNIFORM, fieldName: str = '') -> Density:
        """This method creates a Density object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Density
                session.odbs[name].materials[name].Density

        The table data for this object are:
        - The mass density.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        distributionType
            A SymbolicConstant specifying how the density is distributed spatially. Possible values 
            are UNIFORM, ANALYTICAL_FIELD, and DISCRETE_FIELD. The default value is UNIFORM. 
        fieldName
            A String specifying the name of the AnalyticalField or DiscreteField object associated 
            with this material option. The *fieldName* argument applies only when 
            *distributionType*=ANALYTICAL_FIELD or *distributionType*=DISCRETE_FIELD. The default 
            value is an empty string. 

        Returns
        -------
            A Density object. 

        Raises
        ------
        RangeError
        """
        self.density = Density(table, temperatureDependency, dependencies, distributionType, fieldName)
        return self.density

    def Depvar(self, deleteVar: int = 0, n: int = 0) -> Depvar:
        """This method creates a Depvar object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Depvar
                session.odbs[name].materials[name].Depvar
        
        Parameters
        ----------
        deleteVar
            An Int specifying the state variable number controlling the element deletion flag. The 
            default value is 0.This argument applies only to Abaqus/Explicit analyses. 
        n
            An Int specifying the number of solution-dependent state variables required at each 
            integration point. The default value is 0. 

        Returns
        -------
            A Depvar object. 

        Raises
        ------
        RangeError
        """
        self.depvar = Depvar(deleteVar, n)
        return self.depvar

    def Dielectric(self, table: tuple, type: SymbolicConstant = ISOTROPIC, frequencyDependency: Boolean = OFF,
                   temperatureDependency: Boolean = OFF, dependencies: int = 0) -> Dielectric:
        """This method creates a Dielectric object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Dielectric
                session.odbs[name].materials[name].Dielectric
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        type
            A SymbolicConstant specifying the dielectric behavior. Possible values are ISOTROPIC, 
            ORTHOTROPIC, and ANISOTROPIC. The default value is ISOTROPIC. 
        frequencyDependency
            A Boolean specifying whether the data depend on frequency. The default value is OFF. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Dielectric object.
        """
        self.dielectric = Dielectric(table, type, frequencyDependency, temperatureDependency, dependencies)
        return self.dielectric

    def Diffusivity(self, table: tuple, type: SymbolicConstant = ISOTROPIC, law: SymbolicConstant = GENERAL,
                    temperatureDependency: Boolean = OFF, dependencies: int = 0) -> Diffusivity:
        """This method creates a Diffusivity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Diffusivity
                session.odbs[name].materials[name].Diffusivity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        type
            A SymbolicConstant specifying the type of diffusivity. Possible values are ISOTROPIC, 
            ORTHOTROPIC, and ANISOTROPIC. The default value is ISOTROPIC. 
        law
            A SymbolicConstant specifying the diffusion behavior. Possible values are GENERAL and 
            FICK. The default value is GENERAL. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Diffusivity object. 

        Raises
        ------
        RangeError
        """
        self.diffusivity = Diffusivity(table, type, law, temperatureDependency, dependencies)
        return self.diffusivity

    def DruckerPrager(self, table: tuple, shearCriterion: SymbolicConstant = LINEAR, eccentricity: float = 0,
                      testData: Boolean = OFF, temperatureDependency: Boolean = OFF,
                      dependencies: int = 0) -> DruckerPrager:
        """This method creates a DruckerPrager object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].DruckerPrager
                session.odbs[name].materials[name].DruckerPrager
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        shearCriterion
            A SymbolicConstant specifying the yield criterion. Possible values are LINEAR, 
            HYPERBOLIC, and EXPONENTIAL. The default value is LINEAR.This argument applies only to 
            Abaqus/Standard analyses. Only the linear Drucker-Prager model is available in 
            Abaqus/Explicit analyses. 
        eccentricity
            A Float specifying the flow potential eccentricity, ϵϵ, a small positive number that 
            defines the rate at which the hyperbolic flow potential approaches its asymptote. The 
            default value is 0.1.This argument applies only to Abaqus/Standard analyses. 
        testData
            A Boolean specifying whether the material constants for the exponent model are to be 
            computed by Abaqus/Standard from triaxial test data at different levels of confining 
            pressure. The default value is OFF.This argument is valid only if 
            *shearCriterion*=EXPONENTIAL. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A DruckerPrager object. 

        Raises
        ------
        RangeError
        """
        self.druckerPrager = DruckerPrager(table, shearCriterion, eccentricity, testData, temperatureDependency,
                                           dependencies)
        return self.druckerPrager

    def Elastic(self, table: tuple, type: SymbolicConstant = ISOTROPIC, noCompression: Boolean = OFF,
                noTension: Boolean = OFF, temperatureDependency: Boolean = OFF, dependencies: int = 0,
                moduli: SymbolicConstant = LONG_TERM) -> Elastic:
        """This method creates an Elastic object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Elastic
                session.odbs[name].materials[name].Elastic

        The table data for this object are:
        - If **type**=ISOTROPIC, the table data specify the following:
            - The Young's modulus, E.
            - The Poisson's ratio, v.
            - Temperature, if the data depend on temperature.
            - Value of the first field variable, if the data depend on field variables.
            - Value of the second field variable.
            - Etc.
        - If **type**=SHEAR, the table data specify the following:
            - The shear modulus,G.
            - Temperature, if the data depend on temperature.
            - Value of the first field variable, if the data depend on field variables.
            - Value of the second field variable.
            - Etc.
        - If **type**=ENGINEERING_CONSTANTS, the table data specify the following:
            - E1.
            - E2.
            - E3.
            - v12.
            - v13.
            - v23.
            - G12.
            - G13.
            - G23.
            - Temperature, if the data depend on temperature.
            - Value of the first field variable, if the data depend on field variables.
            - Value of the second field variable.
            - Etc.
        - If **type**=LAMINA, the table data specify the following:
            - E1.
            - E2.
            - v12.
            - G12.
            - G13. This shear modulus is needed to define transverse shear behavior in shells.
            - G23. This shear modulus is needed to define transverse shear behavior in shells.
            - Temperature, if the data depend on temperature.
            - Value of the first field variable, if the data depend on field variables.
            - Value of the second field variable.
            - Etc.
        - If **type**=ORTHOTROPIC, the table data specify the following:
            - D1111.
            - D1122.
            - D2222.
            - D1133.
            - D2233.
            - D3333.
            - D1212.
            - D1313.
            - D2323.
            - Temperature, if the data depend on temperature.
            - Value of the first field variable, if the data depend on field variables.
            - Value of the second field variable.
            - Etc.
        - If **type**=ANISOTROPIC, the table data specify the following:
            - D1111.
            - D1122.
            - D2222.
            - D1133.
            - D2233.
            - D3333.
            - D1112.
            - D2212.
            - D3312.
            - D1212.
            - D1113.
            - D2213.
            - D3313.
            - D1213.
            - D1313.
            - D1123.
            - D2223.
            - D3323.
            - D1223.
            - D1323.
            - D2323.
            - Temperature, if the data depend on temperature.
            - Value of the first field variable, if the data depend on field variables.
            - Value of the second field variable.
            - Etc.
        - If **type**=TRACTION, the table data specify the following:
            - EE for warping elements; En⁢n for cohesive elements.
            - G1 for warping elements; Es⁢s for cohesive elements.
            - G2 for warping elements; Et⁢t for cohesive elements.
            - Temperature, if the data depend on temperature.
            - Value of the first field variable, if the data depend on field variables.
            - Value of the second field variable.
            - Etc.
        - If **type**=BILAMINA, the table data specify the following:
            - E1+.
            - E2+.
            - v12+.
            - G12.
            - E1-.
            - E2-.
            - v112-.
            - Temperature, if the data depend on temperature.
            - Value of the first field variable, if the data depend on field variables.
            - Value of the second field variable.
            - Etc.
        - If **type**=SHORT_FIBER, there is no table data.
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        type
            A SymbolicConstant specifying the type of elasticity data provided. Possible values are: 
            
            - ISOTROPIC 
            - ORTHOTROPIC 
            - ANISOTROPIC 
            - ENGINEERING_CONSTANTS 
            - LAMINA 
            - TRACTION 
            - COUPLED_TRACTION 
            - SHORT_FIBER 
            - SHEAR 
            - BILAMINA 
            The default value is ISOTROPIC. 
        noCompression
            A Boolean specifying whether compressive stress is allowed. The default value is OFF. 
        noTension
            A Boolean specifying whether tensile stress is allowed. The default value is OFF. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        moduli
            A SymbolicConstant specifying the time-dependence of the elastic material constants. 
            Possible values are INSTANTANEOUS and LONG_TERM. The default value is LONG_TERM. 

        Returns
        -------
            An Elastic object. 

        Raises
        ------
        RangeError
        """
        self.elastic = Elastic(table, type, noCompression, noTension, temperatureDependency, dependencies, moduli)
        return self.elastic

    def ElectricalConductivity(self, table: tuple, type: SymbolicConstant = ISOTROPIC,
                               frequencyDependency: Boolean = OFF,
                               temperatureDependency: Boolean = OFF, dependencies: int = 0) -> ElectricalConductivity:
        """This method creates an ElectricalConductivity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].ElectricalConductivity
                session.odbs[name].materials[name].ElectricalConductivity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        type
            A SymbolicConstant specifying the type of electrical conductivity. Possible values are 
            ISOTROPIC, ORTHOTROPIC, and ANISOTROPIC. The default value is ISOTROPIC. 
        frequencyDependency
            A Boolean specifying whether the data depend on frequency. The default value is OFF. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            An ElectricalConductivity object. 

        Raises
        ------
        RangeError
        """
        self.electricalConductivity = ElectricalConductivity(table, type, frequencyDependency, temperatureDependency,
                                                             dependencies)
        return self.electricalConductivity

    def Eos(self, type: SymbolicConstant = IDEALGAS, temperatureDependency: Boolean = OFF,
            dependencies: int = 0, detonationEnergy: float = 0, solidTable: tuple = (),
            gasTable: tuple = (), reactionTable: tuple = (), gasSpecificTable: tuple = (),
            table: tuple = ()) -> Eos:
        """This method creates an Eos object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Eos
                session.odbs[name].materials[name].Eos
        
        Parameters
        ----------
        type
            A SymbolicConstant specifying the equation of state. Possible values are USUP, JWL, 
            IDEALGAS, TABULAR, and IGNITIONANDGROWTH. The default value is IDEALGAS. 
        temperatureDependency
            A Boolean specifying whether the data in *gasSpecificTable* depend on temperature. The 
            default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies for the data in 
            *gasSpecificTable*. The default value is 0. 
        detonationEnergy
            A Float specifying the detonation energy text field. The default value is 0.0. 
        solidTable
            A sequence of sequences of Floats specifying the following: 
            - $A_{s}$. 
            - $B_{s}$. 
            - ${\omega}_{s}$. 
            - $R_{1s}$. 
            - $R_{2s}$. 
            The default value is an empty sequence. 
        gasTable
            A sequence of sequences of Floats specifying the following: 
            - $A_{g}$. 
            - $B_{g}$. 
            - ${\omega}_{g}$. 
            - $R_{1g}$. 
            - $R_{2g}$. 
            The default value is an empty sequence. 
        reactionTable
            A sequence of sequences of Floats specifying the following: 
            - Initial Pressure, $I$. 
            - Product co-volume, $a$. 
            - Exponent on the unreacted fraction (ignition term), $x$. 
            - First burn rate coefficient, $G_{1}$ 
            - Exponent on the unreacted fraction (growth term), $c$. 
            - Exponent on the reacted fraction (growth term), $d$. 
            - Pressure exponent (growth term), $y$. 
            - Second burn rate coefficient, $G_{2}$. 
            - Exponent on the unreacted fraction (completion term), $e$. 
            - Exponent on the reacted fraction (completion term), $g$. 
            - Pressure exponent (completion term), $z$. 
            - Initial reacted fraction, ${F^{max}}_{ig}$. 
            - Maximum reacted fraction for the growth term, ${F^{max}}_{G1}$. 
            - Minimum reacted fraction, ${F^{min}}_{G2}$. 
            The default value is an empty sequence. 
        gasSpecificTable
            A sequence of sequences of Floats specifying the following: 
            - Specific Heat per unit mass. 
            - Temperature dependent data. 
            - Value of first field variable. 
            - Value of second field variable. 
            - Etc. 
            The default value is an empty sequence. 
        table
            A sequence of sequences of Floats specifying the items described below. The default 
            value is an empty sequence. 

        Returns
        -------

        Raises
        ------
        """
        self.eos = Eos(type, temperatureDependency, dependencies, detonationEnergy, solidTable, gasTable, reactionTable,
                       gasSpecificTable, table)
        return self.eos

    def Expansion(self, type: SymbolicConstant = ISOTROPIC, userSubroutine: Boolean = OFF, zero: float = 0,
                  temperatureDependency: Boolean = OFF, dependencies: int = 0, table: tuple = ()) -> Expansion:
        """This method creates an Expansion object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Expansion
                session.odbs[name].materials[name].Expansion
        
        Parameters
        ----------
        type
            A SymbolicConstant specifying the type of expansion. Possible values are ISOTROPIC, 
            ORTHOTROPIC, ANISOTROPIC, and SHORT_FIBER. The default value is ISOTROPIC. 
        userSubroutine
            A Boolean specifying whether a user subroutine is used to define the increments of 
            thermal strain. The default value is OFF. 
        zero
            A Float specifying the value of θ0 if the thermal expansion is temperature-dependent or 
            field-variable-dependent. The default value is 0.0. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        table
            A sequence of sequences of Floats specifying the items described below. The default 
            value is an empty sequence.This argument is required only if **type** is not USER. 

        Returns
        -------
            An Expansion object. 

        Raises
        ------
        RangeError
        """
        self.expansion = Expansion(type, userSubroutine, zero, temperatureDependency, dependencies, table)
        return self.expansion

    def FluidLeakoff(self, temperatureDependency: Boolean = OFF, dependencies: int = 0,
                     type: SymbolicConstant = COEFFICIENTS, table: tuple = ()) -> FluidLeakoff:
        """This method creates a FluidLeakoff object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].FluidLeakoff
                session.odbs[name].materials[name].FluidLeakoff
        
        Parameters
        ----------
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        type
            A SymbolicConstant specifying the type of fluid leak-off. Possible values are 
            COEFFICIENTS and USER. The default value is COEFFICIENTS. 
        table
            A sequence of sequences of Floats specifying the items described below. The default 
            value is an empty sequence. 

        Returns
        -------
            A FluidLeakoff object.
        """
        self.fluidLeakoff = FluidLeakoff(temperatureDependency, dependencies, type, table)
        return self.fluidLeakoff

    def GapFlow(self, table: tuple, kmax: float = None, temperatureDependency: Boolean = OFF,
                dependencies: int = 0, type: SymbolicConstant = NEWTONIAN) -> GapFlow:
        """This method creates a GapFlow object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].GapFlow
                session.odbs[name].materials[name].GapFlow
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        kmax
            None or a Float specifying the maximum permeability value that should be used. If 
            *kmax*=None, Abaqus assumes that the permeability is not bounded. This value is 
            meaningful only when **type**=NEWTONIAN. The default value is None. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        type
            A SymbolicConstant specifying the type of gap flow. Possible values are NEWTONIAN, 
            POWER_LAW, BINGHAM_PLASTIC, and HERSCHEL-BULKLEY. The default value is NEWTONIAN. 

        Returns
        -------
            A GapFlow object.
        """
        self.gapFlow = GapFlow(table, kmax, temperatureDependency, dependencies, type)
        return self.gapFlow

    def GasketMembraneElastic(self, table: tuple, temperatureDependency: Boolean = OFF,
                              dependencies: int = 0) -> GasketMembraneElastic:
        """This method creates a GasketMembraneElastic object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].GasketMembraneElastic
                session.odbs[name].materials[name].GasketMembraneElastic
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A GasketMembraneElastic object. 

        Raises
        ------
        RangeError
        """
        self.gasketMembraneElastic = GasketMembraneElastic(table, temperatureDependency, dependencies)
        return self.gasketMembraneElastic

    def GasketThicknessBehavior(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0,
                                tensileStiffnessFactor: float = None, type: SymbolicConstant = ELASTIC_PLASTIC,
                                unloadingDependencies: int = 0, unloadingTemperatureDependency: Boolean = OFF,
                                variableUnits: SymbolicConstant = STRESS, yieldOnset: float = 0,
                                yieldOnsetMethod: SymbolicConstant = RELATIVE_SLOPE_DROP,
                                unloadingTable: tuple = ()) -> GasketThicknessBehavior:
        """This method creates a GasketThicknessBehavior object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].GasketThicknessBehavior
                session.odbs[name].materials[name].GasketThicknessBehavior
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying loading data. The first sequence must 
            contain only 0. At least two sequences must be specified if **type**=DAMAGE, and at least 
            3 sequences must be specified if **type**=ELASTIC_PLASTIC. The items in the table data are 
            described below. 
        temperatureDependency
            A Boolean specifying whether the loading data depend on temperature. The default value 
            is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies included in the definition 
            of the loading data, in addition to temperature. The default value is 0. 
        tensileStiffnessFactor
            A Float specifying the fraction of the initial compressive stiffness that defines the 
            stiffness in tension. The default value is 10–3. 
        type
            A SymbolicConstant specifying a damage elasticity model or an elastic-Plastic model for
            gasket thickness-direction behavior. Possible values are ELASTIC_PLASTIC and DAMAGE. The 
            default value is ELASTIC_PLASTIC. 
        unloadingDependencies
            An Int specifying the number of field variable dependencies included in the definition 
            of the unloading data, in addition to temperature. The default value is 0. 
        unloadingTemperatureDependency
            A Boolean specifying whether unloading data depends on temperature. The default value is 
            OFF. 
        variableUnits
            A SymbolicConstant specifying the behavior in terms of units of force (or force in unit 
            length) versus closure or pressure versus closure. Possible values are STRESS and FORCE. 
            The default value is STRESS. 
        yieldOnset
            A Float specifying the closure value at which the onset of yield occurs or the relative 
            drop in slope on the loading curve that defines the onset of Plastic deformation
            (depending on the value of *yieldOnsetMethod*). The default value is 0.1. 
        yieldOnsetMethod
            A SymbolicConstant specifying the method used to determine yield onset. Possible values 
            are RELATIVE_SLOPE_DROP and CLOSURE_VALUE. The default value is RELATIVE_SLOPE_DROP. 
        unloadingTable
            A sequence of sequences of Floats specifying unloading data. The items in the table data 
            are described below. The default value is an empty sequence. 

        Returns
        -------
            A GasketThicknessBehavior object. 

        Raises
        ------
        RangeError
        """
        self.gasketThicknessBehavior = GasketThicknessBehavior(table, temperatureDependency, dependencies,
                                                               tensileStiffnessFactor, type, unloadingDependencies,
                                                               unloadingTemperatureDependency, variableUnits,
                                                               yieldOnset, yieldOnsetMethod, unloadingTable)
        return self.gasketThicknessBehavior

    def GasketTransverseShearElastic(self, table: tuple, variableUnits: SymbolicConstant = STRESS,
                                     temperatureDependency: Boolean = OFF,
                                     dependencies: int = 0) -> GasketTransverseShearElastic:
        """This method creates a GasketTransverseShearElastic object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].GasketTransverseShearElastic
                session.odbs[name].materials[name].GasketTransverseShearElastic
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        variableUnits
            A SymbolicConstant specifying the unit system in which the transverse shear behavior 
            will be defined. Possible values are STRESS and FORCE. The default value is STRESS. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A GasketTransverseShearElastic object. 

        Raises
        ------
        RangeError
        """
        self.gasketTransverseShearElastic = GasketTransverseShearElastic(table, variableUnits, temperatureDependency,
                                                                         dependencies)
        return self.gasketTransverseShearElastic

    def Gel(self, table: tuple) -> Gel:
        """This method creates a Gel object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Gel
                session.odbs[name].materials[name].Gel
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 

        Returns
        -------
            A Gel object.
        """
        self.gel = Gel(table)
        return self.gel

    def Hyperelastic(self, table: tuple, type: SymbolicConstant = UNKNOWN,
                     moduliTimeScale: SymbolicConstant = LONG_TERM, temperatureDependency: Boolean = OFF,
                     n: int = 1, beta: typing.Union[SymbolicConstant, float] = FITTED_VALUE,
                     testData: Boolean = ON, compressible: Boolean = OFF, properties: int = 0,
                     deviatoricResponse: SymbolicConstant = UNIAXIAL,
                     volumetricResponse: SymbolicConstant = DEFAULT, poissonRatio: float = 0,
                     materialType: SymbolicConstant = ISOTROPIC,
                     anisotropicType: SymbolicConstant = FUNG_ANISOTROPIC,
                     formulation: SymbolicConstant = STRAIN, behaviorType: SymbolicConstant = INCOMPRESSIBLE,
                     dependencies: int = 0, localDirections: int = 0) -> Hyperelastic:
        """This method creates a Hyperelastic object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Hyperelastic
                session.odbs[name].materials[name].Hyperelastic
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. This argument is 
            valid only if *testData*=OFF. 
        type
            A SymbolicConstant specifying the type of strain energy potential. Possible values 
            are:ARRUDA_BOYCEMARLOWMOONEY_RIVLINNEO_HOOKEOGDENPOLYNOMIALREDUCED_POLYNOMIALUSERVAN_DER_WAALSYEOHUNKNOWNThe 
            default value is UNKNOWN. 
        moduliTimeScale
            A SymbolicConstant specifying the nature of the time response. Possible values are 
            INSTANTANEOUS and LONG_TERM. The default value is LONG_TERM. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        n
            An Int specifying the order of the strain energy potential. The default value is 1.If 
            *testData*=ON and **type**=POLYNOMIAL, *n* can take only the values 1 or 2.If 
            *testData*=ON and **type**=OGDEN or if *testData*=OFF for either type, 1 ≤n≤≤n≤ 6.If 
            **type**=USER, this argument cannot be used. 
        beta
            The SymbolicConstant FITTED_VALUE or a Float specifying the invariant mixture parameter. 
            This argument is valid only if *testData*=ON and **type**=VAN_DER_WAALS. The default value 
            is FITTED_VALUE. 
        testData
            A Boolean specifying whether test data are supplied. The default value is ON. 
        compressible
            A Boolean specifying whether the hyperelastic material is compressible. This parameter 
            is applicable only to user-defined hyperelastic materials. The default value is OFF. 
        properties
            An Int specifying the number of property values needed as data for the user-defined 
            hyperelastic material. The default value is 0. 
        deviatoricResponse
            A SymbolicConstant specifying which test data to use. Possible values are UNIAXIAL, 
            BIAXIAL, and PLANAR. The default value is UNIAXIAL. 
        volumetricResponse
            A SymbolicConstant specifying the volumetric response. Possible values are DEFAULT, 
            VOLUMETRIC_DATA, POISSON_RATIO, and LATERAL_NOMINAL_STRAIN. The default value is 
            DEFAULT. 
        poissonRatio
            A Float specifying the poisson ratio. This argument is valid only if 
            *volumetricResponse*=POISSON_RATIO. The default value is 0.0. 
        materialType
            A SymbolicConstant specifying the type of material. Possible values are ISOTROPIC and 
            ANISOTROPIC. The default value is ISOTROPIC. 
        anisotropicType
            A SymbolicConstant specifying the type of strain energy potential. Possible values are 
            FUNG_ANISOTROPIC, FUNG_ORTHOTROPIC, HOLZAPFEL, and USER_DEFINED. The default value is 
            FUNG_ANISOTROPIC. 
        formulation
            A SymbolicConstant specifying the type of formulation. Possible values are STRAIN and 
            INVARIANT. The default value is STRAIN. 
        behaviorType
            A SymbolicConstant specifying the type of anisotropic hyperelastic material behavior. 
            Possible values are INCOMPRESSIBLE and COMPRESSIBLE. The default value is 
            INCOMPRESSIBLE. 
        dependencies
            An Int specifying the number of field variable dependencies for the data 
            in*volumetricTable* . The default value is 0. 
        localDirections
            An Int specifying the number of local directions for the data in*volumetricTable* . The 
            default value is 0. 

        Returns
        -------
            A Hyperelastic object. 
            
        Raises
        ------
        InvalidNameError
        RangeError 
        """
        self.hyperelastic = Hyperelastic(table, type, moduliTimeScale, temperatureDependency, n, beta, testData,
                                         compressible, properties, deviatoricResponse, volumetricResponse, poissonRatio,
                                         materialType, anisotropicType, formulation, behaviorType, dependencies,
                                         localDirections)
        return self.hyperelastic

    def Hyperfoam(self, testData: Boolean = OFF, poisson: float = None, n: int = 1,
                  temperatureDependency: Boolean = OFF, moduli: SymbolicConstant = LONG_TERM,
                  table: tuple = ()) -> Hyperfoam:
        """This method creates a Hyperfoam object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Hyperfoam
                session.odbs[name].materials[name].Hyperfoam
        
        Parameters
        ----------
        testData
            A Boolean specifying whether test data are supplied. The default value is OFF. 
        poisson
            None or a Float specifying the effective Poisson's ratio, νν, of the material. This 
            argument is valid only when *testData*=ON. The default value is None. 
        n
            An Int specifying the order of the strain energy potential. Possible values are 1 ≤n≤≤n≤ 
            6. The default value is 1. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        moduli
            A SymbolicConstant specifying the time-dependence of the material constants. Possible 
            values are INSTANTANEOUS and LONG_TERM. The default value is LONG_TERM. 
        table
            A sequence of sequences of Floats specifying the items described below. This argument is 
            valid only when *testData*=OFF. The default value is an empty sequence. 

        Returns
        -------
            A Hyperfoam object. 

        Raises
        ------
        RangeError
        """
        self.hyperfoam = Hyperfoam(testData, poisson, n, temperatureDependency, moduli, table)
        return self.hyperfoam

    def Hypoelastic(self, table: tuple, user: Boolean = OFF) -> Hypoelastic:
        """This method creates a Hypoelastic object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Hypoelastic
                session.odbs[name].materials[name].Hypoelastic
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        user
            A Boolean specifying that hypoelasticity is defined by user subroutine UHYPEL. The 
            default value is OFF. 

        Returns
        -------
            A Hypoelastic object.
        """
        self.hypoelastic = Hypoelastic(table, user)
        return self.hypoelastic

    def InelasticHeatFraction(self, fraction: float = 0) -> InelasticHeatFraction:
        """This method creates an InelasticHeatFraction object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].InelasticHeatFraction
                session.odbs[name].materials[name].InelasticHeatFraction
        
        Parameters
        ----------
        fraction
            A Float specifying the fraction of inelastic dissipation rate that appears as a heat 
            flux per unit volume. The fraction may include a unit conversion factor if required. 
            Possible values are 0.0 ≤≤ *fraction* ≤≤ 1.0. The default value is 0.9. 

        Returns
        -------
            An InelasticHeatFraction object. 

        Raises
        ------
        RangeError
        """
        self.inelasticHeatFraction = InelasticHeatFraction(fraction)
        return self.inelasticHeatFraction

    def JouleHeatFraction(self, fraction: float = 1) -> JouleHeatFraction:
        """This method creates a JouleHeatFraction object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].JouleHeatFraction
                session.odbs[name].materials[name].JouleHeatFraction
        
        Parameters
        ----------
        fraction
            A Float specifying the fraction of electrical energy released as heat, including any 
            unit conversion factor. The default value is 1.0. 

        Returns
        -------
            A JouleHeatFraction object. 

        Raises
        ------
        RangeError
        """
        self.jouleHeatFraction = JouleHeatFraction(fraction)
        return self.jouleHeatFraction

    def LatentHeat(self, table: tuple) -> LatentHeat:
        """This method creates a LatentHeat object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].LatentHeat
                session.odbs[name].materials[name].LatentHeat
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 

        Returns
        -------
            A LatentHeat object. 

        Raises
        ------
        RangeError
        """
        self.latentHeat = LatentHeat(table)
        return self.latentHeat

    def LowDensityFoam(self, elementRemoval: Boolean = OFF, maxAllowablePrincipalStress: float = None,
                       extrapolateStressStrainCurve: Boolean = OFF,
                       strainRateType: SymbolicConstant = VOLUMETRIC, mu0: float = None, mu1: float = 0,
                       alpha: float = 2) -> LowDensityFoam:
        """This method creates a LowDensityFoam object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].LowDensityFoam
                session.odbs[name].materials[name].LowDensityFoam
        
        Parameters
        ----------
        elementRemoval
            A Boolean specifying whether elements are removed if exceeding maximum principal tensile 
            stress. This argument is valid only when *maxAllowablePrincipalStress* is defined. The 
            default value is OFF. 
        maxAllowablePrincipalStress
            None or a Float specifying the maximum allowable principal tensile stress. The default 
            value is None. 
        extrapolateStressStrainCurve
            A Boolean specifying whether the stress-strain curve is extrapolated if exceeding 
            maximum strain rate. The default value is OFF. 
        strainRateType
            A SymbolicConstant specifying strain rate measure used for constitutive calculations. 
            Possible values are PRINCIPAL and VOLUMETRIC. The default value is VOLUMETRIC. 
        mu0
            A Float specifying the relaxation coefficient μ0. The default value is 10–4. 
        mu1
            A Float specifying the relaxation coefficient μ1. The default value is 0.5×10–2. 
        alpha
            A Float specifying the relaxation coefficient α. The default value is 2.0. 

        Returns
        -------
            A LowDensityFoam object. 

        Raises
        ------
        RangeError
        """
        self.lowDensityFoam = LowDensityFoam(elementRemoval, maxAllowablePrincipalStress, extrapolateStressStrainCurve,
                                             strainRateType, mu0, mu1, alpha)
        return self.lowDensityFoam

    def MagneticPermeability(self, table: tuple, table2: tuple, table3: tuple, type: SymbolicConstant = ISOTROPIC,
                             frequencyDependency: Boolean = OFF, temperatureDependency: Boolean = OFF,
                             dependencies: int = 0, nonlinearBH: Boolean = OFF) -> MagneticPermeability:
        """This method creates a MagneticPermeability object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].MagneticPermeability
                session.odbs[name].materials[name].MagneticPermeability
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below in “Table data.” 
            If **type**=ORTHOTROPIC and nonlinearBH=ON, the data specified in the *table* is for the 
            first direction and *table2* and *table3* must be specified. 
        table2
            A sequence of sequences of Floats specifying the items described below in “Table data” 
            in the second direction. *table2* must be specified only if **type**=ORTHOTROPIC and 
            nonlinearBH=ON. 
        table3
            A sequence of sequences of Floats specifying the items described below in “Table data” 
            in the third direction. *table3* must be specified only if **type**=ORTHOTROPIC and 
            nonlinearBH=ON. 
        type
            A SymbolicConstant specifying the type of magnetic permeability. Possible values are 
            ISOTROPIC, ORTHOTROPIC, and ANISOTROPIC. The default value is ISOTROPIC. 
        frequencyDependency
            A Boolean specifying whether the data depend on frequency. The default value is OFF. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        nonlinearBH
            A Boolean specifying whether the magnetic behavior is nonlinear and available in tabular 
            form of magnetic flux density versus magnetic field values. The default value is OFF. 

        Returns
        -------
            A MagneticPermeability object. 

        Raises
        ------
        RangeError
        """
        self.magneticPermeability = MagneticPermeability(table, table2, table3, type, frequencyDependency,
                                                         temperatureDependency, dependencies, nonlinearBH)
        return self.magneticPermeability

    def MohrCoulombPlasticity(self, table: tuple, deviatoricEccentricity: float = None,
                              meridionalEccentricity: float = 0,
                              temperatureDependency: Boolean = OFF, dependencies: int = 0,
                              useTensionCutoff: Boolean = OFF) -> MohrCoulombPlasticity:
        """This method creates a MohrCoulombPlasticity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].MohrCoulombPlasticity
                session.odbs[name].materials[name].MohrCoulombPlasticity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        deviatoricEccentricity
            None or a Float specifying the flow potential eccentricity in the deviatoric plane, e; 
            1/2 ≤ 1.0. If *deviatoricEccentricity*=None, Abaqus calculates the value using the 
            specified Mohr-Coulomb angle of friction. The default value is None. 
        meridionalEccentricity
            A Float specifying the flow potential eccentricity in the meridional plane, ϵϵ. The 
            default value is 0.1. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        useTensionCutoff
            A Boolean specifying whether tension cutoff specification is needed. The default value 
            is OFF. 

        Returns
        -------
            A MohrCoulombPlasticity object. 

        Raises
        ------
        RangeError
        """
        self.mohrCoulombPlasticity = MohrCoulombPlasticity(table, deviatoricEccentricity, meridionalEccentricity,
                                                           temperatureDependency, dependencies, useTensionCutoff)
        return self.mohrCoulombPlasticity

    def MoistureSwelling(self, table: tuple) -> MoistureSwelling:
        """This method creates a MoistureSwelling object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].MoistureSwelling
                session.odbs[name].materials[name].MoistureSwelling
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 

        Returns
        -------
            A MoistureSwelling object.
        """
        self.moistureSwelling = MoistureSwelling(table)
        return self.moistureSwelling

    def Permeability(self, specificWeight: float, inertialDragCoefficient: float, table: tuple,
                     type: SymbolicConstant = ISOTROPIC, temperatureDependency: Boolean = OFF,
                     dependencies: int = 0) -> Permeability:
        """This method creates a Permeability object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Permeability
                session.odbs[name].materials[name].Permeability
        
        Parameters
        ----------
        specificWeight
            A Float specifying the specific weight of the wetting liquid, γwγw. 
        inertialDragCoefficient
            A Float specifying The inertial drag coefficient of the wetting liquid, γwγw. 
        table
            A sequence of sequences of Floats specifying the items described below. 
        type
            A SymbolicConstant specifying the type of permeability. Possible values are ISOTROPIC, 
            ORTHOTROPIC, and ANISOTROPIC. The default value is ISOTROPIC. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Permeability object. 

        Raises
        ------
        RangeError
        """
        self.permeability = Permeability(specificWeight, inertialDragCoefficient, table, type, temperatureDependency,
                                         dependencies)
        return self.permeability

    def Piezoelectric(self, table: tuple, type: SymbolicConstant = STRESS, temperatureDependency: Boolean = OFF,
                      dependencies: int = 0) -> Piezoelectric:
        """This method creates a Piezoelectric object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Piezoelectric
                session.odbs[name].materials[name].Piezoelectric
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        type
            A SymbolicConstant specifying the type of material coefficients for the piezoelectric 
            property. Possible values are STRAIN and STRESS. The default value is STRESS. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Piezoelectric object.
        """
        self.piezoelectric = Piezoelectric(table, type, temperatureDependency, dependencies)
        return self.piezoelectric

    def Plastic(self, table: tuple, hardening: SymbolicConstant = ISOTROPIC, rate: Boolean = OFF,
                dataType: SymbolicConstant = HALF_CYCLE, strainRangeDependency: Boolean = OFF,
                numBackstresses: int = 1, temperatureDependency: Boolean = OFF, dependencies: int = 0) -> Plastic:
        """This method creates a Plastic object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Plastic
                session.odbs[name].materials[name].Plastic
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        hardening
            A SymbolicConstant specifying the type of hardening. Possible values are ISOTROPIC, 
            KINEMATIC, COMBINED, JOHNSON_COOK, and USER. The default value is ISOTROPIC. 
        rate
            A Boolean specifying whether the data depend on rate. The default value is OFF. 
        dataType
            A SymbolicConstant specifying the type of combined hardening. This argument is only 
            valid if *hardening*=COMBINED. Possible values are HALF_CYCLE, PARAMETERS, and 
            STABILIZED. The default value is HALF_CYCLE. 
        strainRangeDependency
            A Boolean specifying whether the data depend on strain range. This argument is only 
            valid if *hardening*=COMBINED and *dataType*=STABILIZED. The default value is OFF. 
        numBackstresses
            An Int specifying the number of backstresses. This argument is only valid if 
            *hardening*=COMBINED. The default value is 1. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Plastic object. 

        Raises
        ------
        RangeError
        """
        self.plastic = Plastic(table, hardening, rate, dataType, strainRangeDependency, numBackstresses,
                               temperatureDependency, dependencies)
        return self.plastic

    def PoreFluidExpansion(self, table: tuple, zero: float = 0, temperatureDependency: Boolean = OFF,
                           dependencies: int = 0) -> PoreFluidExpansion:
        """This method creates a PoreFluidExpansion object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].PoreFluidExpansion
                session.odbs[name].materials[name].PoreFluidExpansion
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        zero
            A Float specifying the value of θ0. The default value is 0.0. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A PoreFluidExpansion object. 

        Raises
        ------
        RangeError
        """
        self.poreFluidExpansion = PoreFluidExpansion(table, zero, temperatureDependency, dependencies)
        return self.poreFluidExpansion

    def PorousBulkModuli(self, table: tuple, temperatureDependency: Boolean = OFF) -> PorousBulkModuli:
        """This method creates a PorousBulkModuli object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].PorousBulkModuli
                session.odbs[name].materials[name].PorousBulkModuli
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 

        Returns
        -------
            A PorousBulkModuli object.
        """
        self.porousBulkModuli = PorousBulkModuli(table, temperatureDependency)
        return self.porousBulkModuli

    def PorousElastic(self, table: tuple, shear: SymbolicConstant = POISSON, temperatureDependency: Boolean = OFF,
                      dependencies: int = 0) -> PorousElastic:
        """This method creates a PorousElastic object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].PorousElastic
                session.odbs[name].materials[name].PorousElastic
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        shear
            A SymbolicConstant specifying the shear definition form. Possible values are G and 
            POISSON. The default value is POISSON. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A PorousElastic object. 

        Raises
        ------
        RangeError
        """
        self.porousElastic = PorousElastic(table, shear, temperatureDependency, dependencies)
        return self.porousElastic

    def PorousMetalPlasticity(self, table: tuple, relativeDensity: float = None, temperatureDependency: Boolean = OFF,
                              dependencies: int = 0) -> PorousMetalPlasticity:
        """This method creates a PorousMetalPlasticity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].PorousMetalPlasticity
                session.odbs[name].materials[name].PorousMetalPlasticity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        relativeDensity
            None or a Float specifying the initial relative density of the material, r0. The default 
            value is None. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A PorousMetalPlasticity object. 

        Raises
        ------
        RangeError
        """
        self.porousMetalPlasticity = PorousMetalPlasticity(table, relativeDensity, temperatureDependency, dependencies)
        return self.porousMetalPlasticity

    def Regularization(self, rtol: float = 0,
                       strainRateRegularization: SymbolicConstant = LOGARITHMIC) -> Regularization:
        """This method creates a Regularization object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Regularization
                session.odbs[name].materials[name].Regularization
        
        Parameters
        ----------
        rtol
            A Float specifying the tolerance to be used for regularizing material data. The default 
            value is 0.03. 
        strainRateRegularization
            A SymbolicConstant specifying the form of regularization of strain-rate-dependent 
            material data. Possible values are LOGARITHMIC and LINEAR. The default value is 
            LOGARITHMIC. 

        Returns
        -------
            A Regularization object. 

        Raises
        ------
        RangeError
        """
        self.regularization = Regularization(rtol, strainRateRegularization)
        return self.regularization

    def Solubility(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0) -> Solubility:
        """This method creates a Solubility object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Solubility
                session.odbs[name].materials[name].Solubility
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Solubility object. 

        Raises
        ------
        RangeError
        """
        self.solubility = Solubility(table, temperatureDependency, dependencies)
        return self.solubility

    def Sorption(self, absorptionTable: tuple, lawAbsorption: SymbolicConstant = TABULAR,
                 exsorption: Boolean = OFF, lawExsorption: SymbolicConstant = TABULAR,
                 scanning: float = 0, exsorptionTable: tuple = ()) -> Sorption:
        """This method creates a Sorption object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Sorption
                session.odbs[name].materials[name].Sorption
        
        Parameters
        ----------
        absorptionTable
            A sequence of sequences of Floats specifying the items described below. 
        lawAbsorption
            A SymbolicConstant specifying absorption behavior. Possible values are LOG and TABULAR. 
            The default value is TABULAR. 
        exsorption
            A Boolean specifying whether the exsorption data is specified. The default value is OFF. 
        lawExsorption
            A SymbolicConstant specifying exsorption behavior. Possible values are LOG and TABULAR. 
            The default value is TABULAR. 
        scanning
            A Float specifying the slope of the scanning line, (duw/ds)|s. This slope must be 
            positive and larger than the slope of the absorption or exsorption behaviors. The 
            default value is 0.0. 
        exsorptionTable
            A sequence of sequences of Floats specifying the items described below. The default 
            value is an empty sequence. 

        Returns
        -------
            A Sorption object. 

        Raises
        ------
        RangeError
        """
        self.sorption = Sorption(absorptionTable, lawAbsorption, exsorption, lawExsorption, scanning, exsorptionTable)
        return self.sorption

    def SpecificHeat(self, table: tuple, law: SymbolicConstant = CONSTANTVOLUME,
                     temperatureDependency: Boolean = OFF, dependencies: int = 0) -> SpecificHeat:
        """This method creates a SpecificHeat object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].SpecificHeat
                session.odbs[name].materials[name].SpecificHeat
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        law
            A SymbolicConstant specifying the specific heat behavior. Possible values are 
            CONSTANTVOLUME and CONSTANTPRESSURE. The default value is CONSTANTVOLUME. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A SpecificHeat object. 

        Raises
        ------
        RangeError
        """
        self.specificHeat = SpecificHeat(table, law, temperatureDependency, dependencies)
        return self.specificHeat

    def Swelling(self, table: tuple, law: SymbolicConstant = INPUT, temperatureDependency: Boolean = OFF,
                 dependencies: int = 0) -> Swelling:
        """This method creates a Swelling object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Swelling
                session.odbs[name].materials[name].Swelling
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below.This argument is 
            valid only when *law*=INPUT. 
        law
            A SymbolicConstant specifying the type of data defining the swelling behavior. Possible 
            values are INPUT and USER. The default value is INPUT. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Swelling object. 

        Raises
        ------
        RangeError
        """
        self.swelling = Swelling(table, law, temperatureDependency, dependencies)
        return self.swelling

    def UserMaterial(self, type: SymbolicConstant = MECHANICAL, unsymm: Boolean = OFF,
                     mechanicalConstants: tuple = (), thermalConstants: tuple = (), effmod: Boolean = OFF,
                     hybridFormulation: SymbolicConstant = INCREMENTAL) -> UserMaterial:
        """This method creates a UserMaterial object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].UserMaterial
                session.odbs[name].materials[name].UserMaterial
        
        Parameters
        ----------
        type
            A SymbolicConstant specifying the type of material behavior defined by the command. 
            Possible values are MECHANICAL, THERMAL, and THERMOMECHANICAL. The default value is 
            MECHANICAL. 
        unsymm
            A Boolean specifying if the material stiffness matrix, ∂Δσ/∂Δε, is not symmetric or, 
            when a thermal constitutive model is used, if ∂f/∂(∂θ/∂x) is not symmetric. The default 
            value is OFF. This argument is valid only for an Abaqus/Standard analysis. 
        mechanicalConstants
            A sequence of Floats specifying the mechanical constants of the material. This argument 
            is valid only when **type**=MECHANICAL or THERMOMECHANICAL. The default value is an empty 
            sequence. 
        thermalConstants
            A sequence of Floats specifying the thermal constants of the material. This argument is 
            valid only when **type**=THERMAL or THERMOMECHANICAL. The default value is an empty 
            sequence. 
        effmod
            A Boolean specifying if effective bulk modulus and shear modulus are returned by user 
            subroutine VUMAT. The default value is OFF. This argument is valid only in an 
            Abaqus/Explicit analysis. 
        hybridFormulation
            A SymbolicConstant to specify the formulation of the hybrid element with user subroutine 
            UMAT. Possible values are TOTAL, INCREMENTAL, and INCOMPRESSIBLE. The default value is 
            INCREMENTAL. This argument is valid only in an Abaqus/Standard analysis. 

        Returns
        -------
            A UserMaterial object. 

        Raises
        ------
        RangeError
        """
        self.userMaterial = UserMaterial(type, unsymm, mechanicalConstants, thermalConstants, effmod, hybridFormulation)
        return self.userMaterial

    def UserOutputVariables(self, n: int = 0) -> UserOutputVariables:
        """This method creates a UserOutputVariables object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].UserOutputVariables
                session.odbs[name].materials[name].UserOutputVariables
        
        Parameters
        ----------
        n
            An Int specifying the number of user-defined variables required at each material point. 
            The default value is 0. 

        Returns
        -------
            A UserOutputVariables object. 

        Raises
        ------
        RangeError
        """
        self.userOutputVariables = UserOutputVariables(n)
        return self.userOutputVariables

    def Viscoelastic(self, domain: SymbolicConstant, table: tuple, frequency: SymbolicConstant = FORMULA,
                     type: SymbolicConstant = ISOTROPIC, preload: SymbolicConstant = NONE,
                     time: SymbolicConstant = PRONY, errtol: float = 0, nmax: int = 13,
                     volumetricTable: tuple = ()) -> Viscoelastic:
        """This method creates a Viscoelastic object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Viscoelastic
                session.odbs[name].materials[name].Viscoelastic
        
        Parameters
        ----------
        domain
            A SymbolicConstant specifying the domain definition. Possible values are:
            - FREQUENCY, specifying a frequency domain. This domain is only available for an Abaqus/Standard analysis.
            - TIME, specifying a time domain.
        table
            A sequence of sequences of Floats specifying the items described below. 
        frequency
            A SymbolicConstant specifying the frequency domain definition. This argument is required 
            only when *domain*=FREQUENCY. Possible values are FORMULA, TABULAR, PRONY, 
            CREEP_TEST_DATA, and RELAXATION_TEST_DATA. The default value is FORMULA. 
        type
            A SymbolicConstant specifying the type. This argument is required only when 
            *domain*=FREQUENCY and *frequency*=TABULAR. Possible values are ISOTROPIC and TRACTION. 
            The default value is ISOTROPIC. 
        preload
            A SymbolicConstant specifying the preload. This argument is required only when 
            *domain*=FREQUENCY and *frequency*=TABULAR. Possible values are NONE, UNIAXIAL, 
            VOLUMETRIC, and UNIAXIAL_VOLUMETRIC. The default value is NONE. 
        time
            A SymbolicConstant specifying the time domain definition. This argument is required only 
            when *domain*=TIME. Possible values are PRONY, CREEP_TEST_DATA, RELAXATION_TEST_DATA, 
            and FREQUENCY_DATA. The default value is PRONY. 
        errtol
            A Float specifying the allowable average root-mean-square error of the data points in 
            the least-squares fit. The Float values correspond to percentages; for example, 0.01 is 
            1%. The default value is 0.01.This argument is valid only when *time*=CREEP_TEST_DATA, 
            RELAXATION_TEST_DATA or FREQUENCY_DATA; or only when *frequency*=CREEP_TEST_DATA or 
            RELAXATION_TEST_DATA. 
        nmax
            An Int specifying the maximum number of terms NN in the Prony series. The maximum value 
            is 13. The default value is 13.This argument is valid only when *time*=CREEP_TEST_DATA, 
            RELAXATION_TEST_DATA or FREQUENCY_DATA; or only when *frequency*=CREEP_TEST_DATA or 
            RELAXATION_TEST_DATA. 
        volumetricTable
            A sequence of sequences of Floats specifying the items described below. The default 
            value is an empty sequence. 

        Returns
        -------
            A Viscoelastic object. 

        Raises
        ------
        RangeError
        """
        self.viscoelastic = Viscoelastic(domain, table, frequency, type, preload, time, errtol, nmax, volumetricTable)
        return self.viscoelastic

    def Viscosity(self, table: tuple, type: SymbolicConstant = NEWTONIAN, temperatureDependency: Boolean = OFF,
                  dependencies: int = 0) -> Viscosity:
        """This method creates a Viscosity object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Viscosity
                session.odbs[name].materials[name].Viscosity
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        type
            A SymbolicConstant specifying the type of viscosity. The default value is NEWTONIAN. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            A Viscosity object. 

        Raises
        ------
        RangeError
        """
        self.viscosity = Viscosity(table, type, temperatureDependency, dependencies)
        return self.viscosity

    def Viscous(self, table: tuple, law: SymbolicConstant = STRAIN, temperatureDependency: Boolean = OFF,
                dependencies: int = 0, time: SymbolicConstant = TOTAL) -> Viscous:
        """This method creates a Viscous object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Viscous
                session.odbs[name].materials[name].Viscous
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        law
            A SymbolicConstant specifying the creep law. Possible values are STRAIN, TIME, USER, 
            ANAND, DARVEAUX, DOUBLE_POWER, POWER_LAW, and TIME_POWER_LAW. The default value is 
            STRAIN. 
        temperatureDependency
            A Boolean specifying whether the data depend on temperature. The default value is OFF. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        time
            A SymbolicConstant specifying the time interval for relevant laws. Possible values are 
            CREEP and TOTAL. The default value is TOTAL. 

        Returns
        -------
            A Viscous object.
        """
        self.viscous = Viscous(table, law, temperatureDependency, dependencies, time)
        return self.viscous
