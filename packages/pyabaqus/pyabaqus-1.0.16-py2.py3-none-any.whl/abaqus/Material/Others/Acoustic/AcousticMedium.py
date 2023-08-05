from abaqusConstants import *


class AcousticMedium:
    """The AcousticMedium object specifies the acoustic properties of a material.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import material
        mdb.models[name].materials[name].acousticMedium
        import odbMaterial
        session.odbs[name].materials[name].acousticMedium

    The corresponding analysis keywords are:

    - ACOUSTIC MEDIUM

    """

    def __init__(self, acousticVolumetricDrag: Boolean = OFF, temperatureDependencyB: Boolean = OFF,
                 temperatureDependencyV: Boolean = OFF, dependenciesB: int = 0, dependenciesV: int = 0,
                 bulkTable: tuple = (), volumetricTable: tuple = ()):
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
        pass

    def setValues(self):
        """This method modifies the AcousticMedium object.

        Raises
        ------
        RangeError
        """
        pass
