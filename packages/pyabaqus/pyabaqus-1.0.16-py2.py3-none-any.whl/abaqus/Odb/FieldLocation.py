from abaqusConstants import *
from .SectionPointArray import SectionPointArray


class FieldLocation:
    """The FieldLocation object specifies locations for which data are available in the field.
    For example, a displacement field will have a FieldLocation object with a *position* 
    member value of NODAL. The FieldLocation object has no constructor; it is created 
    automatically as an element of the *location* member of a FieldOutput object by the 
    addData method of a FieldOutput object. 

    Attributes
    ----------
    position: SymbolicConstant
        A SymbolicConstant specifying the position of the output in the element. Possible values
        are:NODAL, specifying the values calculated at the nodes.INTEGRATION_POINT, specifying
        the values calculated at the integration points.ELEMENT_NODAL, specifying the values
        obtained by extrapolating results calculated at the integration
        points.ELEMENT_FACE.CENTROID, specifying the value at the centroid obtained by
        extrapolating results calculated at the integration points.
    sectionPoints: SectionPointArray
        A :py:class:`~abaqus.Odb.SectionPointArray.SectionPointArray` object.

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import odbAccess
        session.odbs[name].steps[name].frames[i].fieldOutputs[name].locations[i]

    """

    # A SymbolicConstant specifying the position of the output in the element. Possible values 
    # are:NODAL, specifying the values calculated at the nodes.INTEGRATION_POINT, specifying 
    # the values calculated at the integration points.ELEMENT_NODAL, specifying the values 
    # obtained by extrapolating results calculated at the integration 
    # points.ELEMENT_FACE.CENTROID, specifying the value at the centroid obtained by 
    # extrapolating results calculated at the integration points. 
    position: SymbolicConstant = None

    # A SectionPointArray object. 
    sectionPoints: SectionPointArray = SectionPointArray()
