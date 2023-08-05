class DamageStabilizationCohesive:
    """The DamageStabilizationCohesive object specifies the viscosity coefficients for the
    damage model for surface-based cohesive behavior or enriched cohesive behavior. 

    Notes
    -----
    This object can be accessed by:
    
    .. code-block:: python
        
        import material
        mdb.models[name].materials[name].ductileDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].fldDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].flsdDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].hashinDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].johnsonCookDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].maxeDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].maxpeDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].maxpsDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].maxsDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].mkDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].msfldDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].quadeDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].quadsDamageInitiation.damageStabilizationCohesive
        mdb.models[name].materials[name].shearDamageInitiation.damageStabilizationCohesive
        import odbMaterial
        session.odbs[name].materials[name].ductileDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].fldDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].flsdDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].hashinDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].johnsonCookDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].maxeDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].maxpeDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].maxpsDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].maxsDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].mkDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].msfldDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].quadeDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].quadsDamageInitiation.damageStabilizationCohesive
        session.odbs[name].materials[name].shearDamageInitiation.damageStabilizationCohesive

    The corresponding analysis keywords are:

    - DAMAGE STABILIZATION

    """

    def __init__(self, cohesiveCoeff: float = None):
        """This method creates a DamageStabilizationCohesive object.

        Notes
        -----
            This function can be accessed by:
            
            .. code-block:: python
            
                mdb.models[name].materials[name].ductileDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].fldDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].flsdDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].hashinDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].johnsonCookDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].maxeDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].maxpeDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].maxpsDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].maxsDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].mkDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].msfldDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].quadeDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].quadsDamageInitiation\
            - .DamageStabilizationCohesive
                mdb.models[name].materials[name].shearDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].ductileDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].fldDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].flsdDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].hashinDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].johnsonCookDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].maxeDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].maxpeDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].maxpsDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].maxsDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].mkDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].msfldDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].quadeDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].quadsDamageInitiation\
            - .DamageStabilizationCohesive
                session.odbs[name].materials[name].shearDamageInitiation\
            - .DamageStabilizationCohesive
        
        Parameters
        ----------
        cohesiveCoeff
            None or a Float specifying the viscosity coefficient. The default value is None. 

        Returns
        -------
            A DamageStabilizationCohesive object. 

        Raises
        ------
        RangeError
        """
        pass

    def setValues(self):
        """This method modifies the DamageStabilizationCohesive object.

        Raises
        ------
        RangeError
        """
        pass
