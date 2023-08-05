from abaqusConstants import *
from .Inertia import Inertia
from ..Region.Region import Region


class PointMassInertia(Inertia):
    """The PointMassInertia object defines point masses and point rotary inertia on a part or
    an assembly region. 
    The PointMassInertia object is derived from the Inertia object. 

    Attributes
    ----------
    suppressed: Boolean
        A Boolean specifying whether the inertia is suppressed or not. The default value is OFF.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import part
        mdb.models[name].parts[name].engineeringFeatures.inertias[name]
        import assembly
        mdb.models[name].rootAssembly.engineeringFeatures.inertias[name]

    The corresponding analysis keywords are:

    - MASS

    """

    # A Boolean specifying whether the inertia is suppressed or not. The default value is OFF. 
    suppressed: Boolean = OFF

    def __init__(self, name: str, region: Region, mass: float = 0, mass1: float = 0, mass2: float = 0,
                 mass3: float = 0, i11: float = 0, i22: float = 0, i33: float = 0, i12: float = 0,
                 i13: float = 0, i23: float = 0, localCsys: str = None, alpha: float = 0,
                 composite: float = 0):
        """This method creates a PointMassInertia object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].parts[name].engineeringFeatures.PointMassInertia
            mdb.models[name].rootAssembly.engineeringFeatures.PointMassInertia
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        region
            A Region object specifying the region to which the mass or rotary inertia is applied. 
        mass
            A Float specifying the mass magnitude for isotropic mass. This parameter cannot be 
            specified when anisotropic mass terms are specified. The default value is 0.0. 
        mass1
            A Float specifying the mass in the 1-direction for anisotropic mass. This parameter 
            cannot be specified when isotropic mass is also specified. The default value is 0.0. 
        mass2
            A Float specifying the mass in the 2-direction for anisotropic mass. This parameter 
            cannot be specified when isotropic mass is also specified. The default value is 0.0. 
        mass3
            A Float specifying the mass in the 3-direction for anisotropic mass. This parameter 
            cannot be specified when isotropic mass is also specified. The default value is 0.0. 
        i11
            A Float specifying the rotary inertia about the local 1-axis, I11I11. The default value 
            is 0.0. 
        i22
            A Float specifying the rotary inertia about the local 2-axis, I22I22. The default value 
            is 0.0. 
        i33
            A Float specifying the rotary inertia about the local 3-axis, I33I33. The default value 
            is 0.0. 
        i12
            A Float specifying the product of inertia, I12I12. The default value is 0.0. 
        i13
            A Float specifying the product of inertia, I13I13. The default value is 0.0. 
        i23
            A Float specifying the product of inertia, I23I23. The default value is 0.0. 
        localCsys
            None or a DatumCsys object specifying the local coordinate system for the anisotropic 
            mass terms (when specified), and the rotary inertia (when specified). If 
            *localCsys*=None, the anisotropic mass and rotary inertia data are defined in the global 
            coordinate system. The default value is None. 
        alpha
            A Float specifying the alpha damping magnitude. The default value is 0.0.This argument 
            applies only to Abaqus/Standard analyses. 
        composite
            A Float specifying the composite damping magnitude. The default value is 0.0.This 
            argument applies only to Abaqus/Standard analyses. 

        Returns
        -------
            A PointMassInertia object.
        """
        super().__init__()
        pass

    def setValues(self, mass: float = 0, mass1: float = 0, mass2: float = 0, mass3: float = 0, i11: float = 0,
                  i22: float = 0, i33: float = 0, i12: float = 0, i13: float = 0, i23: float = 0,
                  localCsys: str = None, alpha: float = 0, composite: float = 0):
        """This method modifies the PointMassInertia object.
        
        Parameters
        ----------
        mass
            A Float specifying the mass magnitude for isotropic mass. This parameter cannot be 
            specified when anisotropic mass terms are specified. The default value is 0.0. 
        mass1
            A Float specifying the mass in the 1-direction for anisotropic mass. This parameter 
            cannot be specified when isotropic mass is also specified. The default value is 0.0. 
        mass2
            A Float specifying the mass in the 2-direction for anisotropic mass. This parameter 
            cannot be specified when isotropic mass is also specified. The default value is 0.0. 
        mass3
            A Float specifying the mass in the 3-direction for anisotropic mass. This parameter 
            cannot be specified when isotropic mass is also specified. The default value is 0.0. 
        i11
            A Float specifying the rotary inertia about the local 1-axis, I11I11. The default value 
            is 0.0. 
        i22
            A Float specifying the rotary inertia about the local 2-axis, I22I22. The default value 
            is 0.0. 
        i33
            A Float specifying the rotary inertia about the local 3-axis, I33I33. The default value 
            is 0.0. 
        i12
            A Float specifying the product of inertia, I12I12. The default value is 0.0. 
        i13
            A Float specifying the product of inertia, I13I13. The default value is 0.0. 
        i23
            A Float specifying the product of inertia, I23I23. The default value is 0.0. 
        localCsys
            None or a DatumCsys object specifying the local coordinate system for the anisotropic 
            mass terms (when specified), and the rotary inertia (when specified). If 
            *localCsys*=None, the anisotropic mass and rotary inertia data are defined in the global 
            coordinate system. The default value is None. 
        alpha
            A Float specifying the alpha damping magnitude. The default value is 0.0.This argument 
            applies only to Abaqus/Standard analyses. 
        composite
            A Float specifying the composite damping magnitude. The default value is 0.0.This 
            argument applies only to Abaqus/Standard analyses. 
        """
        pass
