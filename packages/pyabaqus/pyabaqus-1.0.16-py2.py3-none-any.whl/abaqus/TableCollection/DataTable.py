

class DataTable:
    """The DataTable object is used to specify the parameter table of the respective parameter
    table type. 
    The data type of the values in each column in the DataTable object corresponds to the 
    data type mentioned for the respective ParameterColumn object. The DataTable object 
    should be created when all the required ParameterColumn objects are created for the 
    current ParameterTable. 

    Attributes
    ----------
    label: str
        A String specifying the label of the data table.
    columns: str
        A DataColumnArray specifying all the dataColumns in the :py:class:`~abaqus.Field.DataTable.DataTable` object.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        mdb.models[name].tableCollections[name].parameterTables[name].dataTables[i]

    The corresponding analysis keywords are:

    - *PARAMETER TABLE

    """

    # A String specifying the label of the data table. 
    label: str = ''

    # A DataColumnArray specifying all the dataColumns in the DataTable object. 
    columns: str = ''

    def __init__(self, label: str):
        """This method creates a DataTable object and places it in the dataTables array.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].tableCollections[name].parameterTables[name].DataTable
        
        Parameters
        ----------
        label
            A String specifying a unique label name for the current ParameterTable object. 

        Returns
        -------
            A DataTable object. 

        Raises
        ------
            AbaqusException. 
        """
        pass
