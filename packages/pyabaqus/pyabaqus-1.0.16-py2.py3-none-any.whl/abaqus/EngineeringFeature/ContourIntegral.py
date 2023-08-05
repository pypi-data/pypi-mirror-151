from abaqusConstants import *
from .Crack import Crack
from ..Region.RegionArray import RegionArray


class ContourIntegral(Crack):
    """The ContourIntegral object defines contour integral objects on an region. Currently only
    assembly regions are supported. 
    The ContourIntegral object is derived from the Crack object. 

    Attributes
    ----------
    suppressed: Boolean
        A Boolean specifying whether the crack is suppressed or not. The default value is OFF.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import part
        mdb.models[name].parts[name].engineeringFeatures.cracks[name]
        import assembly
        mdb.models[name].rootAssembly.engineeringFeatures.cracks[name]

    The corresponding analysis keywords are:

    - CONTOUR INTEGRAL

    """

    # A Boolean specifying whether the crack is suppressed or not. The default value is OFF. 
    suppressed: Boolean = OFF

    def __init__(self, name: str, crackFront: RegionArray, crackTip: RegionArray,
                 extensionDirectionMethod: SymbolicConstant, symmetric: Boolean = OFF,
                 listOfRegions: Boolean = OFF, crackFrontName: str = '', crackTipName: str = '',
                 crackNormal: tuple = (), qVectors: tuple = (), midNodePosition: float = 0,
                 collapsedElementAtTip: SymbolicConstant = NONE):
        """This method creates a ContourIntegral object. Although the constructor is available both
        for parts and for the assembly, ContourIntegral objects are currently supported only
        under the assembly.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].parts[name].engineeringFeatures.ContourIntegral
            mdb.models[name].rootAssembly.engineeringFeatures.ContourIntegral
        
        Parameters
        ----------
        name
            A String specifying the repository key. 
        crackFront
            A RegionArray object specifying the crack-front region to which the contour integral is 
            applied. If the crack-front consists of a single region, a Region object may be 
            specified instead of a sequence with a single item in it. 
        crackTip
            A RegionArray object specifying the crack-tip region to which the contour integral is 
            applied. If the crack-tip consists of a single region, a Region object may be specified 
            instead of a sequence with a single item in it. 
        extensionDirectionMethod
            A SymbolicConstant specifying how the virtual crack extension direction vectors are 
            defined. Possible values are CRACK_NORMAL and Q_VECTORS. 
        symmetric
            A Boolean specifying whether the crack is defined on a half model (about a symmetry 
            plane) or whether it is defined on the whole model. The default value is OFF. 
        listOfRegions
            A Boolean specifying whether the regions specified by *crackFront* and *crackTip* are 
            specified using a single region or tuples of region objects. The default value is OFF. 
        crackFrontName
            A String specifying the name of the crack-front region generated from the tuple of 
            regions specifying the crack-front region. This argument is valid only when 
            *listOfRegions* is ON. The default value is *name*+Front. 
        crackTipName
            A String specifying the name of the crack-tip region generated from the tuple of regions 
            specifying the crack-tip region. This parameter is valid only when *listOfRegions*=ON. 
            The default value is *name*+Tip. 
        crackNormal
            A sequence of sequences of Floats specifying the two points of the vector that describes 
            the crack normal direction. Each point is defined by a tuple of two or three coordinates 
            indicating its position. This argument is required only when 
            *extensionDirectionMethod*=CRACK_NORMAL. The default value is an empty sequence. 
        qVectors
            A sequence of sequences of sequences of Floats specifying the vectors that indicate the 
            set of crack extension directions. Each vector is described by a tuple of two points, 
            and each point is described by a tuple of two or three coordinates indicating its 
            position. This argument is required only when *extensionDirectionMethod*=Q_VECTORS. The 
            default value is an empty sequence. 
        midNodePosition
            A Float specifying the position of the midside node along the edges of the second-order 
            elements that radiate from the crack tip. Possible values are 0.0 << *midNodeParameter* 
            << 1.0. The default value is 0.5. 
        collapsedElementAtTip
            A SymbolicConstant specifying the crack-tip singularity. Possible values are NONE, 
            SINGLE_NODE, and DUPLICATE_NODES. The default value is NONE. 

        Returns
        -------
            A ContourIntegral object.
        """
        super().__init__()
        pass

    def setValues(self, symmetric: Boolean = OFF, listOfRegions: Boolean = OFF, crackFrontName: str = '',
                  crackTipName: str = '', crackNormal: tuple = (), qVectors: tuple = (),
                  midNodePosition: float = 0, collapsedElementAtTip: SymbolicConstant = NONE):
        """This method modifies the ContourIntegral object.
        
        Parameters
        ----------
        symmetric
            A Boolean specifying whether the crack is defined on a half model (about a symmetry 
            plane) or whether it is defined on the whole model. The default value is OFF. 
        listOfRegions
            A Boolean specifying whether the regions specified by *crackFront* and *crackTip* are 
            specified using a single region or tuples of region objects. The default value is OFF. 
        crackFrontName
            A String specifying the name of the crack-front region generated from the tuple of 
            regions specifying the crack-front region. This argument is valid only when 
            *listOfRegions* is ON. The default value is *name*+Front. 
        crackTipName
            A String specifying the name of the crack-tip region generated from the tuple of regions 
            specifying the crack-tip region. This parameter is valid only when *listOfRegions*=ON. 
            The default value is *name*+Tip. 
        crackNormal
            A sequence of sequences of Floats specifying the two points of the vector that describes 
            the crack normal direction. Each point is defined by a tuple of two or three coordinates 
            indicating its position. This argument is required only when 
            *extensionDirectionMethod*=CRACK_NORMAL. The default value is an empty sequence. 
        qVectors
            A sequence of sequences of sequences of Floats specifying the vectors that indicate the 
            set of crack extension directions. Each vector is described by a tuple of two points, 
            and each point is described by a tuple of two or three coordinates indicating its 
            position. This argument is required only when *extensionDirectionMethod*=Q_VECTORS. The 
            default value is an empty sequence. 
        midNodePosition
            A Float specifying the position of the midside node along the edges of the second-order 
            elements that radiate from the crack tip. Possible values are 0.0 << *midNodeParameter* 
            << 1.0. The default value is 0.5. 
        collapsedElementAtTip
            A SymbolicConstant specifying the crack-tip singularity. Possible values are NONE, 
            SINGLE_NODE, and DUPLICATE_NODES. The default value is NONE. 
        """
        pass
