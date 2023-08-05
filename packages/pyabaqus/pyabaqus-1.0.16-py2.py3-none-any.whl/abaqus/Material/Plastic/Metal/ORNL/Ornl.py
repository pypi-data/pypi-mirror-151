from abaqusConstants import *


class Ornl:
    """The Ornl object specifies the constitutive model developed by Oak Ridge National
    Laboratory. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].creep.ornl
        mdb.models[name].materials[name].Plastic.ornl
        import odbMaterial
        session.odbs[name].materials[name].creep.ornl
        session.odbs[name].materials[name].Plastic.ornl

    The corresponding analysis keywords are:

    - ORNL

    """

    def __init__(self, a: float = 0, h: float = None, reset: Boolean = OFF):
        """This method creates an Ornl object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].creep.Ornl
                mdb.models[name].materials[name].Plastic.Ornl
                session.odbs[name].materials[name].creep.Ornl
                session.odbs[name].materials[name].Plastic.Ornl
        
        Parameters
        ----------
        a
            A Float specifying the saturation rates for kinematic shift caused by creep strain, as 
            defined by Equation (15) of Section 4.3.3–3 of the Nuclear Standard. The default value 
            corresponds to that section of the Standard. Set *a*=0.0 to use the 1986 revision of the 
            Standard. The default value is 0.3. 
        h
            None or a Float specifying the rate of kinematic shift with respect to creep strain 
            [Equation (7) of Section 4.3.2–1 of the Nuclear Standard]. If *h*=None, the value of *h* 
            is determined according to Section 4.3.3–3 of the 1981 revision of the Standard. Set 
            *h*=0.0 to use the 1986 revision of the Standard. The default value is None. 
        reset
            A Boolean specifying whether to invoke the optional αα reset procedure described in 
            Section 4.3.5 of the Nuclear Standard. The default value is OFF. 

        Returns
        -------
            An Ornl object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the Ornl object.

        Raises
        ------
        RangeError
        """
        pass
