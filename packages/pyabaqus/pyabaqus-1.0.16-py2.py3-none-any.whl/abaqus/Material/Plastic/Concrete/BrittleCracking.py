from abaqusConstants import *
from .BrittleFailure import BrittleFailure
from .BrittleShear import BrittleShear


class BrittleCracking:
    """The BrittleCracking object specifies cracking and postcracking properties for the
    brittle cracking material model. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].brittleCracking
        import odbMaterial
        session.odbs[name].materials[name].brittleCracking

    The table data for this object are:
    
    - If *type*=STRAIN the table data specify the following:
        - Remaining direct stress after cracking.
        - Direct cracking strain.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *type*=DISPLACEMENT the table data specify the following:
        - Remaining direct stress after cracking.
        - Direct cracking displacement.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.
    - If *type*=GFI the table data specify the following:
        - Failure stress.
        - Mode I fracture energy.
        - Temperature, if the data depend on temperature.
        - Value of the first field variable, if the data depend on field variables.
        - Value of the second field variable.
        - Etc.

    The corresponding analysis keywords are:

    - BRITTLE CRACKING

    """

    # A BrittleShear object. 
    brittleShear: BrittleShear = BrittleShear(((),))

    # A BrittleFailure object. 
    brittleFailure: BrittleFailure = BrittleFailure(((),))

    def __init__(self, table: tuple, temperatureDependency: Boolean = OFF, dependencies: int = 0,
                 type: SymbolicConstant = STRAIN):
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
        pass

    def setValues(self):
        """This method modifies the BrittleCracking object.
        """
        pass
