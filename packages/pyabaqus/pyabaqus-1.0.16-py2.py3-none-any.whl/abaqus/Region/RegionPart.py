import typing

from .Region import Region
from .RegionPartBase import RegionPartBase
from .Set import Set
from .Skin import Skin
from .Stringer import Stringer
from .Surface import Surface
from ..BasicGeometry.Cell import Cell
from ..BasicGeometry.Edge import Edge
from ..BasicGeometry.Face import Face
from ..BasicGeometry.ReferencePoint import ReferencePoint
from ..BasicGeometry.Vertex import Vertex
from ..Mesh.MeshEdge import MeshEdge
from ..Mesh.MeshElement import MeshElement
from ..Mesh.MeshFace import MeshFace
from ..Mesh.MeshNode import MeshNode


class RegionPart(RegionPartBase):
    """The following commands operate on Part objects. For more information about the Part 
    object, see Part object. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import regionToolset

    """

    def Surface(self, side1Faces: tuple[Face] = None, side2Faces: tuple[Face] = None, side12Faces: tuple[Face] = None,
                end1Edges: tuple[Face] = None, end2Edges: tuple[Face] = None, circumEdges: tuple[Face] = None,
                side1Edges: tuple[Face] = None, side2Edges: tuple[Face] = None, face1Elements: tuple[Face] = None,
                face2Elements: tuple[Face] = None, face3Elements: tuple[Face] = None, face4Elements: tuple[Face] = None,
                face5Elements: tuple[Face] = None, face6Elements: tuple[Face] = None, side1Elements: tuple[Face] = None,
                side2Elements: tuple[Face] = None, side12Elements: tuple[Face] = None, end1Elements: tuple[Face] = None,
                end2Elements: tuple[Face] = None, circumElements: tuple[Face] = None, name: str = '', **kwargs) -> \
            Surface:
        """This method creates a surface from a sequence of objects in a model database. The
        surface will apply to the sides specified by the arguments.For example

        .. code-block:: python

            surface=mdb.models['Model-1'].parts['Part-1'].Surface(side1Faces=side1Faces, name='Surf-1')

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].parts[*name*].Surface
                mdb.models[name].rootAssembly.Surface

        Required key-value arguments
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            On three-dimensional solid faces, you can use the following arguments:

            - side1Faces
            - side2Faces

            On three-dimensional shell faces, you can use the following arguments:

            - side1Faces
            - side2Faces
            - side12Faces

            On three-dimensional wire edges, you can use the following arguments:

            - end1Edges
            - end2Edges
            - circumEdges

            On three-dimensional or two-dimensional or axisymmetric edges, you can use the following arguments:

            - side1Edges
            - side2Edges

            On two-dimensional or axisymmetric shell elements, you can use the following arguments:

            - face1Elements
            - face2Elements
            - face3Elements
            - face4Elements

            On solid elements, you can use the following arguments:

            - face1Elements
            - face2Elements
            - face3Elements
            - face4Elements
            - face5Elements
            - face6Elements

            On three-dimensional shell elements, you can use the following arguments:

            - side1Elements
            - side2Elements
            - side12Elements

            On three-dimensional wire elements, you can use the following arguments:

            - end1Elements
            - end2Elements
            - circumElements

            On two-dimensional or axisymmetric wire elements, you can use the following arguments:

            - side1Elements
            - side2Elements
        
        Parameters
        ----------
        side1Faces
        side2Faces
        side12Faces
        end1Edges
        end2Edges
        circumEdges
        side1Edges
        side2Edges
        face1Elements
        face2Elements
        face3Elements
        face4Elements
        face5Elements
        face6Elements
        side1Elements
        side2Elements
        side12Elements
        end1Elements
        end2Elements
        circumElements
        name
            A String specifying the repository key. The default value is an empty string.

        Returns
        -------
        surf: Surface
            A Surface object
        """
        surface = Surface(side1Faces, side2Faces, side12Faces, end1Edges, end2Edges, circumEdges, side1Edges,
                          side2Edges, face1Elements, face2Elements, face3Elements, face4Elements, face5Elements,
                          face6Elements, side1Elements, side2Elements, side12Elements, end1Elements, end2Elements,
                          circumElements, name)
        self.surfaces[name] = surface
        self.allSurfaces[name] = surface
        return surface

    @typing.overload
    def Set(self, name: str, nodes: tuple[MeshNode] = None, elements: tuple[MeshElement] = None,
            region: Region = None, vertices: tuple[Vertex] = None, edges: tuple[Edge] = None,
            faces: tuple[Face] = None, cells: tuple[Cell] = None, xVertices: tuple[Vertex] = None,
            xEdges: tuple[Edge] = None, xFaces: tuple[Face] = None,
            referencePoints: tuple[ReferencePoint] = (), skinFaces: tuple = (),
            skinEdges: tuple = (), stringerEdges: tuple = ()) -> Set:
        """This method creates a set from a sequence of objects in a model database.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].parts[*name*].Set
                mdb.models[name].rootAssembly.Set
        
        Parameters
        ----------
        name
            A String specifying the repository key.
        nodes
            A sequence of MeshNode objects. The default value is None.
        elements
            A sequence of MeshElement objects. The default value is None.
        region
            A Region object specifying other objects to be included in the set. The default value is
            None.
        vertices
            A sequence of ConstrainedSketchVertex objects. The default value is None.
        edges
            A sequence of Edge objects. The default value is None.
        faces
            A sequence of Face objects. The default value is None.
        cells
            A sequence of Cell objects. The default value is None.
        xVertices
            A sequence of ConstrainedSketchVertex objects that excludes specific vertices from the set. The default
            value is None.
        xEdges
            A sequence of Edge objects that excludes specific edges from the set. The default value
            is None.
        xFaces
            A sequence of Face objects that exclude specific faces from the set. The default value
            is None.
        referencePoints
            A sequence of ReferencePoint objects. The default value is an empty sequence.
        skinFaces
            A tuple of tuples specifying a skin name and the sequence of faces associated with this
            skin. Valid only for geometric regions on 3D and 2D parts.
        skinEdges
            A tuple of tuples specifying a skin name and the sequence of edges associated with this
            skin. Valid only for geometric regions on Axisymmetric parts.
        stringerEdges
            A tuple of tuples specifying a stringer name and the sequence of edges associated with
            this stringer. Valid only for geometric regions on 3D and 2D parts.

        Returns
        -------
        set: Set
            A Set object
        """
        pass

    @typing.overload
    def Set(self, name: str, objectToCopy: Set) -> Set:
        """This method copies a set from an existing set.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].parts[*name*].Set
                mdb.models[name].rootAssembly.Set
        
        Parameters
        ----------
        name
            A String specifying the name of the set.
        objectToCopy
            A Set object to be copied.

        Returns
        -------
        set: Set
            A Set object
        """
        pass

    def Set(self, name, *args, **kwargs) -> Set:
        """This method creates a set from a sequence of objects in a model database.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].parts[*name*].Set
                mdb.models[name].rootAssembly.Set
        
        Parameters
        ----------
        name

        Returns
        -------
        set: Set
            A Set object
        """
        self.sets[name] = aSet = Set(name, *args, **kwargs)
        return aSet

    def Skin(self, name: str, faces: tuple[Face] = (), edges: tuple[Edge] = (),
             elementFaces: tuple[MeshFace] = (), elementEdges: tuple[MeshEdge] = ()) -> Skin:
        """This method creates a skin from a sequence of objects in a model database. At least one
        of the optional arguments needs to be specified.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].parts[*name*].Skin
        
        Parameters
        ----------
        name
            A String specifying the repository key. The default value is an empty string.
        faces
            A sequence of Face objects specifying the faces on which skins should be created.
            Applicable to three and two-dimensional parts.
        edges
            A sequence of Edge objects specifying the edges on which skins should be created.
            Applicable to axisymmetric parts.
        elementFaces
            A sequence of MeshFace objects specifying the mesh faces on which skins should be
            created. Applicable to three and two-dimensional parts.
        elementEdges
            A sequence of MeshEdge objects specifying the mesh edges on which skins should be
            created. Applicable to axisymmetric parts.

        Returns
        -------
        skin: Skin
            A Skin object
        """
        self.skins[name] = skin = Skin(name, faces, edges, elementFaces, elementEdges)
        return skin

    def EditSkin(self, name: str = '', faces: tuple[Face] = (), edges: tuple[Edge] = (),
                 elementFaces: tuple[MeshFace] = (), elementEdges: tuple[MeshEdge] = ()) -> Skin:
        """This method modifies underlying entities of the selected skin. At least one of the
        optional arguments needs to be specified.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].parts[*name*].EditSkin
        
        Parameters
        ----------
        name
            A String specifying the repository key. The default value is an empty string.
        faces
            A sequence of Face objects specifying the faces on which skins should be created.
            Applicable to three and two-dimensional parts.
        edges
            A sequence of Edge objects specifying the edges on which skins should be created.
            Applicable to axisymmetric parts.
        elementFaces
            A sequence of MeshFace objects specifying the mesh faces on which skins should be
            created. Applicable to three and two-dimensional parts.
        elementEdges
            A sequence of MeshEdge objects specifying the mesh edges on which skins should be
            created. Applicable to axisymmetric parts.

        Returns
        -------
        skin: Skin
            A Skin object
        """
        self.skins[name] = skin = Skin(name, faces, edges, elementFaces, elementEdges)
        return skin

    def Stringer(self, name: str, edges: tuple[Edge] = (), elementEdges: tuple[MeshEdge] = ()) -> Stringer:
        """This method creates a stringer from a sequence of objects in a model database. At least
        one of the optional arguments needs to be specified.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].parts[*name*].Stringer
        
        Parameters
        ----------
        name
            A String specifying the repository key. The default value is an empty string.
        edges
            A sequence of Edge objects specifying the edges on which stringers should be created.
            Applicable to three and two-dimensional parts.
        elementEdges
            A sequence of MeshEdge objects specifying the mesh edges on which stringers should be
            created. Applicable to three and two-dimensional parts.

        Returns
        -------
        stringer: Stringer
            A Stringer object
        """
        self.stringers[name] = stringer = Stringer(name, edges, elementEdges)
        return stringer
