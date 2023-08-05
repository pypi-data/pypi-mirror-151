from .OdbAuxiliaryData import OdbAuxiliaryData


class OdbContactDiagnostics:
    """The OdbDiagnosticContact object.

    Attributes
    ----------
    data: dict[str, OdbAuxiliaryData]
        A repository of :py:class:`~abaqus.PlotOptions.OdbAuxiliaryData.OdbAuxiliaryData` objects. This attribute is read-only.
    description: str
        A string specifying the opening/overclosure status of the contact. This attribute is
        read-only.
    detailStrings: tuple
        A sequence of strings specifying the nature of each of the contact pair. This attribute
        is read-only.
    type: str
        A string specifying the type of contact initialization. This attribute is read-only.
    defaultFormats: str
        A string specifying the default format value. This attribute is read-only.
    elementDescriptions: str
        A string specifying the element description. This attribute is read-only.
    nodeDescriptions: str
        A string specifying the node description. This attribute is read-only.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import visualization
        session.odbData[name].diagnosticData.steps[i].contactDiagnostics[i]

    """

    # A repository of OdbAuxiliaryData objects. This attribute is read-only. 
    data: dict[str, OdbAuxiliaryData] = dict[str, OdbAuxiliaryData]()

    # A string specifying the opening/overclosure status of the contact. This attribute is 
    # read-only. 
    description: str = ''

    # A sequence of strings specifying the nature of each of the contact pair. This attribute 
    # is read-only. 
    detailStrings: tuple = ()

    # A string specifying the type of contact initialization. This attribute is read-only. 
    type: str = ''

    # A string specifying the default format value. This attribute is read-only. 
    defaultFormats: str = ''

    # A string specifying the element description. This attribute is read-only. 
    elementDescriptions: str = ''

    # A string specifying the node description. This attribute is read-only. 
    nodeDescriptions: str = ''
