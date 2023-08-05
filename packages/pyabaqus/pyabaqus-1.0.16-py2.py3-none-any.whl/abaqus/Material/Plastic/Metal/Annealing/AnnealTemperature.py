
class AnnealTemperature:
    """The AnnealTemperature object specifies the material annealing temperature.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].Plastic.annealTemperature
        import odbMaterial
        session.odbs[name].materials[name].Plastic.annealTemperature

    The table data for this object are:
    
    - The annealing temperature, θθ.
    - Temperature, if the data depend on temperature.
    - Value of the first field variable, if the data depend on field variables.
    - Value of the second field variable.
    - Etc.

    The corresponding analysis keywords are:

    - ANNEAL TEMPERATURE

    """

    def __init__(self, table: tuple, dependencies: int = 0):
        """This method creates an AnnealTemperature object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].Plastic.AnnealTemperature
                session.odbs[name].materials[name].Plastic.AnnealTemperature
        
        Parameters
        ----------
        table
            A sequence of sequences of Floats specifying the items described below. 
        dependencies
            An Int specifying the number of field variable dependencies. The default value is 0. 

        Returns
        -------
            An AnnealTemperature object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the AnnealTemperature object.

        Raises
        ------
        RangeError
        """
        pass
