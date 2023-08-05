from abaqusConstants import *


class TensileFailure:
    """The TensileFailure object specifies the material tensile failure.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].Plastic.tensileFailure
        mdb.models[name].materials[name].eos.tensileFailure
        import odbMaterial
        session.odbs[name].materials[name].Plastic.tensileFailure
        session.odbs[name].materials[name].eos.tensileFailure

    The table data for this object are:

    - The Hydrostatic cutoff stress (positive in tension).
    - Temperature, if the data depend on temperature.
    - Value of the first field variable if the data depend on field variables.
    - Value of the second field variable.
    - Etc.

    The corresponding analysis keywords are:

    - TENSILE FAILURE

    """

    def tensileFailure(self, table: tuple, dependencies: int = 0, temperatureDependency: Boolean = OFF,
                       elementDeletion: Boolean = True, pressure: SymbolicConstant = None,
                       shear: SymbolicConstant = None):
        """This method creates a tensileFailure object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Plastic.TensileFailure
                mdb.models[name].materials[name].eos.TensileFailure
                session.odbs[name].materials[name].Plastic.TensileFailure
                session.odbs[name].materials[name].eos.TensileFailure
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 
        temperatureDependency
            A boolean specifying whether the data depends on temperature. The default value is OFF. 
        elementDeletion
            A boolean specifying whether element deletion is allowed. The default value is True. 
        pressure
            A SymbolicConstant specifying the pressure stress. The Possible values are BRITTLE and 
            DUCTILE. 
        shear
            A SymbolicConstant specifying the deviatoric stress. Possible values are BRITTLE and 
            DUCTILE. 

        Returns
        -------
            An TensileFailure object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the TensileFailure object.

        Raises
        ------
        RangeError
        """
        pass
