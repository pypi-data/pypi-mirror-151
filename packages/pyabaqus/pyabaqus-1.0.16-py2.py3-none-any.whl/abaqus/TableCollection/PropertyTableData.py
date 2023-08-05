from abaqusConstants import *


class PropertyTableData:
    """A PropertyTableData is an object that is used to specify the property table of the
    respective property table type. 
    The values in each column in the PropertyTableData object corresponds to the properties 
    and variables mentioned in the PropertyTable object. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        mdb.models[name].tableCollections[name].propertyTables[name].propertyTableDatas[name]

    The corresponding analysis keywords are:

    - PROPERTY TABLE TYPE
            - PROPERTY TABLE

    """

    def __init__(self, label: str = '', regularize: SymbolicConstant = None,
                 extrapolate: SymbolicConstant = None, isTemp: Boolean = OFF, fieldNums: int = None,
                 regularizeTolerance: str = '', data: str = ''):
        """This method creates a PropertyTableData object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].tableCollections[name].propertyTables[name].PropertTableData
        
        Parameters
        ----------
        label
            A String specifying a unique label name for the current PropertyTable object. 
        regularize
            A SymbolicConstant specifying the type of regularize to the user-defined property data. 
        extrapolate
            A SymbolicConstant specifying the type of extrapolation of dependent variables outside 
            the specified range of the independent variables. 
        isTemp
            A Boolean specifying the dependency of properties on temperature. 
        fieldNums
            An Int specifying the field variables on which properties are dependent. 
        regularizeTolerance
            A Double specifying the tolerance to be used to regularize the property table data. 
        data
            An Array of doubles specifying the values of the properties, the variables mentioned in 
            PropertyTable, and the field variables mentioned in PropertyTableData. 

        Returns
        -------
            A PropertyTableData object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the PropertyTableData object.

        Returns
        -------

        Raises
        ------
        RangeError
        """
        pass
