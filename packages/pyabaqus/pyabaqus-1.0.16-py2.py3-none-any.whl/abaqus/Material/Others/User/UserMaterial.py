from abaqusConstants import *


class UserMaterial:
    """The UserMaterial object defines material constants for use in subroutines UMAT, UMATHT,
    or VUMAT. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].userMaterial
        import odbMaterial
        session.odbs[name].materials[name].userMaterial

    The corresponding analysis keywords are:

    - USER MATERIAL

    """

    def __init__(self, type: SymbolicConstant = MECHANICAL, unsymm: Boolean = OFF,
                 mechanicalConstants: tuple = (), thermalConstants: tuple = (), effmod: Boolean = OFF,
                 hybridFormulation: SymbolicConstant = INCREMENTAL):
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
            is valid only when *type*=MECHANICAL or THERMOMECHANICAL. The default value is an empty 
            sequence. 
        thermalConstants
            A sequence of Floats specifying the thermal constants of the material. This argument is 
            valid only when *type*=THERMAL or THERMOMECHANICAL. The default value is an empty 
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
        pass

    def setValues(self):
        """This method modifies the UserMaterial object.

        Raises
        ------
        RangeError
        """
        pass
