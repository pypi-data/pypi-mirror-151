from abaqusConstants import *
from .CDCTerm import CDCTerm
from .CDCTermArray import CDCTermArray


class DerivedComponent:
    """A DerivedComponent object describes user-customized components for use in defining
    ConnectorFriction and Potential objects. 

    Attributes
    ----------
    cdcTerms: CDCTermArray
        A :py:class:`~abaqus.Connector.CDCTermArray.CDCTermArray` object.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import section
        mdb.models[name].sections[name].behaviorOptions[i].connectorPotentials[i].derivedComponent
        mdb.models[name].sections[name].behaviorOptions[i].derivedComponent
        mdb.models[name].sections[name].behaviorOptions[i].evolutionPotentials[i].derivedComponent
        mdb.models[name].sections[name].behaviorOptions[i].initiationPotentials[i].derivedComponent
        import odbSection
        session.odbs[name].sections[name].behaviorOptions[i].connectorPotentials[i].derivedComponent
        session.odbs[name].sections[name].behaviorOptions[i].derivedComponent
        session.odbs[name].sections[name].behaviorOptions[i].evolutionPotentials[i].derivedComponent
        session.odbs[name].sections[name].behaviorOptions[i].initiationPotentials[i].derivedComponent

    The corresponding analysis keywords are:

    - CONNECTOR DERIVED COMPONENT

    """

    # A CDCTermArray object. 
    cdcTerms: CDCTermArray = CDCTermArray()

    def __init__(self):
        """This method creates a DerivedComponent object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].sections[name].behaviorOptions[i].connectorPotentials[i].DerivedComponent
            mdb.models[name].sections[name].behaviorOptions[i].DerivedComponent
            mdb.models[name].sections[name].behaviorOptions[i].evolutionPotentials[i].DerivedComponent
            mdb.models[name].sections[name].behaviorOptions[i].initiationPotentials[i].DerivedComponent
            session.odbs[name].sections[name].behaviorOptions[i].connectorPotentials[i].DerivedComponent
            session.odbs[name].sections[name].behaviorOptions[i].DerivedComponent
            session.odbs[name].sections[name].behaviorOptions[i].evolutionPotentials[i].DerivedComponent
            session.odbs[name].sections[name].behaviorOptions[i].initiationPotentials[i].DerivedComponent

        Returns
        -------
            A DerivedComponent object. 

        Raises
        ------
            ValueError and TextError. 
        """
        pass

    def setValues(self):
        """This method modifies the DerivedComponent object.

        Raises
        ------
            ValueError. 
        """
        pass

    def CDCTerm(self, intrinsicComponents: tuple, table: tuple, termOperator: SymbolicConstant = RSS,
                termSign: SymbolicConstant = POSITIVE, localDependency: Boolean = OFF,
                indepCompType: SymbolicConstant = POSITION, indepComponents: tuple = (),
                tempDependency: Boolean = OFF, fieldDependencies: int = 0) -> CDCTerm:
        """This method creates a CDCTerm object.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].sections[name].behaviorOptions[i].connectorPotentials[i].DerivedComponent
            mdb.models[name].sections[name].behaviorOptions[i].DerivedComponent
            mdb.models[name].sections[name].behaviorOptions[i].evolutionPotentials[i].DerivedComponent
            mdb.models[name].sections[name].behaviorOptions[i].initiationPotentials[i].DerivedComponent
            session.odbs[name].sections[name].behaviorOptions[i].connectorPotentials[i].DerivedComponent
            session.odbs[name].sections[name].behaviorOptions[i].DerivedComponent
            session.odbs[name].sections[name].behaviorOptions[i].evolutionPotentials[i].DerivedComponent
            session.odbs[name].sections[name].behaviorOptions[i].initiationPotentials[i].DerivedComponent
        
        Parameters
        ----------
        intrinsicComponents
            A sequence of Ints specifying the components of relative motion for which the
            contributing term is defined. Possible values are 1 ≤≤ *intrinsicComponents* ≤≤ 6. Only
            available components can be specified if the DerivedComponent object is being referenced
            by a Potential object. This is not the case if the DerivedComponent object is referenced
            by a ConnectorFriction object directly. The default value is an empty sequence.
        table
            A sequence of sequences of Floats specifying components numbers and temperature and
            field values. Each sequence of the table data specifies:The first intrinsic component
            number.If applicable, the second intrinsic component number.Etc.If applicable, the first
            independent component number.If applicable, the second independent component
            number.Etc.If applicable, the temperature value.If applicable, the value of the first
            field variable.If applicable, the value of the second field variable.Etc.The default
            value is an empty sequence.
        termOperator
            A SymbolicConstant specifying the method for combining contributing terms: square root
            of a sum of the squares, direct sum, or Macauley sum. Possible values are RSS, SUM, and
            MACAULEY. The default value is RSS.
        termSign
            A SymbolicConstant specifying the overall sign for the contributing term. Possible
            values are POSITIVE and NEGATIVE. The default value is POSITIVE.
        localDependency
            A Boolean specifying whether the table data depend on either components of relative
            position or components of constitutive relative motion. The default value is OFF.
        indepCompType
            A SymbolicConstant specifying whether localDependency refers to components of relative
            position or components of constitutive relative motion. Possible values are POSITION and
            MOTION. The default value is POSITION.The *indepCompType* argument applies only if
            *localDependency*=ON.
        indepComponents
            A sequence of Ints specifying the independent components included in the derived
            component definition. Possible values are 1 ≤≤ *indepComponents* ≤≤ 6. Only available
            components can be specified. The *indepComponents* argument applies only if
            *localDependency*=ON. The default value is an empty sequence.
        tempDependency
            A Boolean specifying whether the table data depend on temperature. The default value is
            OFF.
        fieldDependencies
            An Int specifying the number of field variable dependencies. The default value is 0.

        Returns
        -------
            A CDCTerm object.

        Raises
        ------
            ValueError and TextError.
        """
        cDCTerm = CDCTerm(intrinsicComponents, table, termOperator, termSign, localDependency,
                          indepCompType, indepComponents, tempDependency, fieldDependencies)
        self.cdcTerms.append(cDCTerm)
        return cDCTerm
