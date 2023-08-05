from abaqusConstants import *


class ConnectorOptions:
    """The ConnectorOptions object is used to define various options for connector behaviors.
    It can be used only in conjunction with CDCTerm, ConnectorDamage, ConnectorDamping, 
    ConnectorElasticity, ConnectorFriction, and ConnectorPlasticity objects. Because the 
    ConnectorDamage object contains two separate ConnectorOptions repositories (one for 
    damage initiation and one for damage evolution), there are two ConnectorOptions 
    constructors associated with that behavior—initiationOptions and evolutionOptions. The 
    ConnectorPlasticity object also contains two separate ConnectorOptions repositories (one 
    for isotropic hardening and one for kinematic hardening), so there are two 
    ConnectorOptions constructors associated with that behavior—isotropicOptions and 
    kinematicOptions. 

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python

        import section
        mdb.models[name].sections[name].behaviorOptions[i].connectorPotentials[i].derivedComponent.cdcTerms[i].options
        mdb.models[name].sections[name].behaviorOptions[i].derivedComponent.cdcTerms[i].options
        mdb.models[name].sections[name].behaviorOptions[i].evolutionOptions
        mdb.models[name].sections[name].behaviorOptions[i].evolutionPotentials[i].derivedComponent.cdcTerms[i].options
        mdb.models[name].sections[name].behaviorOptions[i].initiationOptions
        mdb.models[name].sections[name].behaviorOptions[i].initiationPotentials[i].derivedComponent.cdcTerms[i].options
        mdb.models[name].sections[name].behaviorOptions[i].isotropicOptions
        mdb.models[name].sections[name].behaviorOptions[i].kinematicOptions
        mdb.models[name].sections[name].behaviorOptions[i].options
        import odbSection
        session.odbs[name].sections[name].behaviorOptions[i].connectorPotentials[i].derivedComponent.cdcTerms[i].options
        session.odbs[name].sections[name].behaviorOptions[i].derivedComponent.cdcTerms[i].options
        session.odbs[name].sections[name].behaviorOptions[i].evolutionOptions
        session.odbs[name].sections[name].behaviorOptions[i].evolutionPotentials[i].derivedComponent.cdcTerms[i].options
        session.odbs[name].sections[name].behaviorOptions[i].initiationOptions
        session.odbs[name].sections[name].behaviorOptions[i].initiationPotentials[i].derivedComponent.cdcTerms[i].options
        session.odbs[name].sections[name].behaviorOptions[i].isotropicOptions
        session.odbs[name].sections[name].behaviorOptions[i].kinematicOptions
        session.odbs[name].sections[name].behaviorOptions[i].options

    The corresponding analysis keywords are:

    - CONNECTOR BEHAVIOR
            - CONNECTOR DAMAGE INITIATION
            - CONNECTOR DAMAGE EVOLUTION
            - CONNECTOR DAMPING
            - CONNECTOR DERIVED COMPONENT
            - CONNECTOR ELASTICITY
            - CONNECTOR FRICTION
            - CONNECTOR PLASTICITY

    """

    def __init__(self, useBehRegSettings: Boolean = ON, regularize: Boolean = ON,
                 defaultTolerance: Boolean = ON, regularization: float = 0,
                 defaultRateFactor: Boolean = ON, rateFactor: float = 0,
                 interpolation: SymbolicConstant = LINEAR, useBehExtSettings: Boolean = ON,
                 extrapolation: SymbolicConstant = CONSTANT):
        """This method creates a connector options object to be used in conjunction with an
        allowable connector behavior option, derived component term, or connector section.

        Notes
        -----
        This function can be accessed by:

        .. code-block:: python

            mdb.models[name].sections[name].behaviorOptions[i].connectorPotentials[i].derivedComponent.cdcTerms[i].ConnectorOptions
            mdb.models[name].sections[name].behaviorOptions[i].derivedComponent.cdcTerms[i].ConnectorOptions
            mdb.models[name].sections[name].behaviorOptions[i].ConnectorOptions
            mdb.models[name].sections[name].behaviorOptions[i].evolutionPotentials[i].derivedComponent.cdcTerms[i].ConnectorOptions
            mdb.models[name].sections[name].behaviorOptions[i].ConnectorOptions
            mdb.models[name].sections[name].behaviorOptions[i].initiationPotentials[i].derivedComponent.cdcTerms[i].ConnectorOptions
            mdb.models[name].sections[name].behaviorOptions[i].ConnectorOptions
            session.odbs[name].sections[name].behaviorOptions[i].connectorPotentials[i].derivedComponent.cdcTerms[i].ConnectorOptions
            session.odbs[name].sections[name].behaviorOptions[i].derivedComponent.cdcTerms[i].ConnectorOptions
            session.odbs[name].sections[name].behaviorOptions[i].ConnectorOptions
            session.odbs[name].sections[name].behaviorOptions[i].evolutionPotentials[i].derivedComponent.cdcTerms[i].ConnectorOptions
            session.odbs[name].sections[name].behaviorOptions[i].ConnectorOptions
            session.odbs[name].sections[name].behaviorOptions[i].initiationPotentials[i].derivedComponent.cdcTerms[i].ConnectorOptions
            session.odbs[name].sections[name].behaviorOptions[i].ConnectorOptions
        
        Parameters
        ----------
        useBehRegSettings
            A Boolean specifying whether or not to use the behavior-level settings for 
            regularization options. This argument is applicable only for an Abaqus/Explicit 
            analysis. The default value is ON. 
        regularize
            A Boolean specifying whether or not the tabular data will be regularized. This argument 
            is applicable only for an Abaqus/Explicit analysis and only if *useBehRegSettings*=OFF. 
            The default value is ON. 
        defaultTolerance
            A Boolean specifying whether or not the analysis default regularization tolerance will 
            be used. This argument is applicable only for an Abaqus/Explicit analysis and only if 
            *useBehRegSettings*=OFF and *regularize*=ON. The default value is ON. 
        regularization
            A Float specifying the regularization increment to be used. This argument is applicable 
            only for an Abaqus/Explicit analysis and only if *useBehRegSettings*=OFF, 
            *regularize*=ON, and *defaultTolerance*=OFF. The default value is 0.03. 
        defaultRateFactor
            A Boolean specifying whether or not the analysis default rate filter factor will be 
            used. This argument is applicable only for an Abaqus/Explicit analysis that includes 
            isotropic hardening with tabular definition or damage initiation with Plastic motion
            criteria. The default value is ON. 
        rateFactor
            A Float specifying the rate filter factor to be used. This argument is applicable only 
            for an Abaqus/Explicit analysis that includes isotropic hardening with tabular 
            definition or damage initiation with Plastic motion criteria. This argument is also
            applicable only if *defaultRateFactor*=OFF. The default value is 0.9. 
        interpolation
            A SymbolicConstant specifying the type of interpolation increment to be used on 
            rate-dependent tabular data. This argument is applicable only for an Abaqus/Explicit 
            analysis that includes isotropic hardening with tabular definition or damage initiation 
            with Plastic motion criteria. Possible values are LINEAR and LOGARITHMIC. The default
            value is LINEAR. 
        useBehExtSettings
            A Boolean specifying whether or not to use the behavior-level settings for extrapolation 
            options. The default value is ON. 
        extrapolation
            A SymbolicConstant specifying the extrapolation technique to be used. This argument is 
            applicable only if *useBehExtSettings*=OFF. Possible values are CONSTANT and LINEAR. The 
            default value is CONSTANT. 

        Returns
        -------
            A ConnectorOptions object. 

        Raises
        ------
            ValueError and TextError. 
        """
        pass

    def setValues(self):
        """This method modifies the ConnectorOptions object.

        Raises
        ------
            ValueError. 
        """
        pass
