import typing

from abaqusConstants import *
from .FieldOutput import FieldOutput
from .OdbLoadCase import OdbLoadCase


class OdbFrame:
    """The domain of the OdbFrame object is taken from the parent step.

    Attributes
    ----------
    cyclicModeNumber: int
        An Int specifying the cyclic mode number associated with the data stored on this frame.
        Only frequency analyses of cyclic symmetry models possess cyclic mode numbers.
    domain: SymbolicConstant
        A SymbolicConstant specifying the domain of the step of which the frame is a member.
        Possible values are TIME, FREQUENCY, and MODAL.
    frequency: float
        A Float specifying the frequency. This member is valid only if **domain=FREQUENCY** or if
        the **procedureType** member of the :py:class:`~abaqus.Step.Step.Step` object=FREQUENCY. The default value is 0.0.
    mode: int
        An Int specifying the eigenmode. This member is valid only if **domain=MODAL**.
    associatedFrame: 'OdbFrame'
        An :py:class:`~abaqus.Odb.OdbFrame.OdbFrame` object specifying the real or imaginary portion of the data corresponding to
        this cyclic symmetry mode.
    fieldOutputs: dict[str, FieldOutput]
        A repository of :py:class:`~abaqus.Odb.FieldOutput.FieldOutput` objects specifying the key to the **fieldOutputs**repository
        is a String representing an output variable.
    loadCase: OdbLoadCase
        An :py:class:`~abaqus.Odb.OdbLoadCase.OdbLoadCase` object specifying the load case for the frame.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import odbAccess
        session.odbs[name].steps[name].frames[i]

    """

    # An Int specifying the cyclic mode number associated with the data stored on this frame. 
    # Only frequency analyses of cyclic symmetry models possess cyclic mode numbers. 
    cyclicModeNumber: int = None

    # A SymbolicConstant specifying the domain of the step of which the frame is a member. 
    # Possible values are TIME, FREQUENCY, and MODAL. 
    domain: SymbolicConstant = None

    # A Float specifying the frequency. This member is valid only if *domain*=FREQUENCY or if 
    # the *procedureType* member of the Step object=FREQUENCY. The default value is 0.0. 
    frequency: float = 0

    # An Int specifying the eigenmode. This member is valid only if *domain*=MODAL. 
    mode: int = None

    # An OdbFrame object specifying the real or imaginary portion of the data corresponding to 
    # this cyclic symmetry mode. 
    associatedFrame: 'OdbFrame' = None

    # A repository of FieldOutput objects specifying the key to the *fieldOutputs*repository 
    # is a String representing an output variable. 
    fieldOutputs: dict[str, FieldOutput] = dict[str, FieldOutput]()

    # An OdbLoadCase object specifying the load case for the frame. 
    loadCase: OdbLoadCase = OdbLoadCase('loadCase')

    @typing.overload
    def __init__(self, incrementNumber: int, frameValue: float, description: str = ''):
        """This method creates an OdbFrame object and appends it to the frame sequence.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            session.odbs[name].steps[name].Frame
        
        Parameters
        ----------
        incrementNumber
            An Int specifying the frame increment number within the step. The base frame has 
            normally increment number 0, and the results run from 1. In case of multiple load cases, 
            the same increment number is duplicated for each loadcase. 
        frameValue
            A Float specifying the value in units determined by the *domain* member of the Step 
            object. The equivalent in the time domain is *stepTime*; in the frequency domain the 
            equivalent is *frequency*; and in the modal domain the equivalent is *mode*. 
        description
            A String specifying the contents of the frame. The default value is an empty string. 

        Returns
        -------
            An OdbFrame object.
        """
        pass

    @typing.overload
    def __init__(self, mode: int, frequency: float, description: str = ''):
        """This constructor creates an OdbFrame object in the frequency domain and appends it to
        the frame sequence. The arguments to the constructor are valid only when
        *domain*=FREQUENCY or *domain*=MODAL.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            session.odbs[name].steps[name].Frame
        
        Parameters
        ----------
        mode
            An Int specifying the eigenmode. This member is valid only if *domain*=MODAL. 
        frequency
            A Float specifying the frequency. This member is valid only if *domain*=FREQUENCY or if 
            the *procedureType* member of the Step object=FREQUENCY. The default value is 0.0. 
        description
            A String specifying the contents of the frame. The default value is an empty string. 

        Returns
        -------
            An OdbFrame object.
        """
        pass

    @typing.overload
    def __init__(self, loadCase: OdbLoadCase, description: str = '', frequency: float = 0):
        """This constructor creates an OdbFrame object for a specific load case and appends it to
        the frame sequence.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            session.odbs[name].steps[name].Frame
        
        Parameters
        ----------
        loadCase
            An OdbLoadCase object specifying the load case for the frame. 
        description
            A String specifying the contents of the frame. The default value is an empty string. 
        frequency
            A Float specifying the frequency. This member is valid only if *domain*=FREQUENCY or if 
            the *procedureType* member of the Step object=FREQUENCY. The default value is 0.0. 

        Returns
        -------
            An OdbFrame object.
        """
        pass

    def Frame(self, *args, **kwargs):
        pass

    @typing.overload
    def FieldOutput(self, name: str, description: str, type: SymbolicConstant, componentLabels: tuple = (),
                    validInvariants: SymbolicConstant = None, isEngineeringTensor: Boolean = OFF):
        """This method creates a FieldOutput object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            session.odbs[name].steps[name].Frame
        
        Parameters
        ----------
        name
            A String specifying the output variable name.
        description
            A String specifying the output variable. Colon (:) should not be used as a part of the
            field output description.
        type
            A SymbolicConstant specifying the output type. Possible values are SCALAR, VECTOR,
            TENSOR_3D_FULL, TENSOR_3D_PLANAR, TENSOR_3D_SURFACE, TENSOR_2D_PLANAR, and
            TENSOR_2D_SURFACE.
        componentLabels
            A sequence of Strings specifying the labels for each component of the value. The length
            of the sequence must match the type. If *type*=TENSOR, the default value is *name* with
            the suffixes ('11', '22', '33', '12', '13', '23'). If *type*=VECTOR, the default value
            is *name* with the suffixes ('1', '2', '3'). If *type*=SCALAR, the default value is an
            empty sequence.
        validInvariants
            A sequence of SymbolicConstants specifying which invariants should be calculated for
            this field. An empty sequence indicates that no invariants are valid for this field.
            Possible values
            are:MAGNITUDEMISESTRESCAPRESSINV3MAX_PRINCIPALMID_PRINCIPALMIN_PRINCIPALMAX_INPLANE_PRINCIPALMIN_INPLANE_PRINCIPALOUTOFPLANE_PRINCIPALThe
            default value is an empty sequence.
        isEngineeringTensor
            A Boolean specifying whether the field is an engineering tensor or not. Setting
            isEngineeringTensor to true makes a tensor field behave as a strain like quantity where
            the off-diagonal components of tensor are halved for invariants computation. This
            parameter applies only to tensor field outputs. The default value is OFF.

        Returns
        -------
            A FieldOutput object.
        """
        pass

    @typing.overload
    def FieldOutput(self, field: 'FieldOutput', name: str = '', description: str = ''):
        """This method creates a FieldOutput object from an existing FieldOutput object of the same
        output database.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            session.odbs[name].steps[name].Frame
        
        Parameters
        ----------
        field
            A FieldOutput object.
        name
            A String specifying the name of the FieldOutput object.
        description
            A String specifying the output variable. Colon (:) should not be used as a part of the
            field output description.

        Returns
        -------
            A FieldOutput object.
        """
        pass

    def FieldOutput(self, *args, **kwargs):
        if 'name' in kwargs.keys():
            name = kwargs['name']
        else:
            if isinstance(args[0], FieldOutput):
                name = args[1]
            else:
                name = args[0]
        self.fieldOutputs[name] = fieldOutput = FieldOutput(*args, **kwargs)
        return fieldOutput
