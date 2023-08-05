# pylint: disable=C0103
from typing import Optional, Union
from warnings import warn

import numpy as np
# import bottleneck as bn

from pyrealm.bounds_checker import bounds_checker
from pyrealm.param_classes import PModelParams
from pyrealm.utilities import check_input_shapes, summarize_attrs

# TODO - Note that the typing currently does not enforce the dtype of ndarrays
#        but it looks like the upcoming np.typing module might do this.

def calc_density_h2o(tc: Union[float, np.ndarray],
                     patm: Union[float, np.ndarray],
                     pmodel_params: PModelParams = PModelParams(),
                     safe: bool = True) -> Union[float, np.ndarray]:
    """Calculates the **density of water** as a function of temperature and
    atmospheric pressure, using the Tumlirz Equation and coefficients calculated
    by :cite:`Fisher:1975tm`.

    Parameters:

        tc: air temperature, °C
        patm: atmospheric pressure, Pa
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.
        safe: Prevents the function from estimating density below -30°C, where the
            function behaves poorly

    Other Parameters:

        lambda_: polynomial coefficients of Tumlirz equation (`pmodel_params.fisher_dial_lambda`).
        Po: polynomial coefficients of Tumlirz equation (`pmodel_params.fisher_dial_Po`).
        Vinf: polynomial coefficients of Tumlirz equation (`pmodel_params.fisher_dial_Vinf`).

    Returns:

        Water density as a float in (g cm^-3)

    Examples:

        >>> round(calc_density_h2o(20, 101325), 3)
        998.206
    """

    # DESIGN NOTE:
    # It doesn't make sense to use this function for tc < 0, but in particular
    # the calculation shows wild numeric instability between -44 and -46 that
    # leads to numerous downstream issues - see the extreme values documentation.
    if safe and np.nanmin(tc) < -30:
        raise RuntimeError('Water density calculations below about -30°C are '
                           'unstable. See argument safe to calc_density_h2o')
        
    # Check input shapes, shape not used
    _ = check_input_shapes(tc, patm)

    # Get powers of tc, including tc^0 = 1 for constant terms
    tc_pow = np.power.outer(tc, np.arange(0, 10))

    # Calculate lambda, (bar cm^3)/g:
    lambda_val = np.sum(np.array(pmodel_params.fisher_dial_lambda) * tc_pow[..., :5], axis=-1)

    # Calculate po, bar
    po_val = np.sum(np.array(pmodel_params.fisher_dial_Po) * tc_pow[..., :5], axis=-1)

    # Calculate vinf, cm^3/g
    vinf_val = np.sum(np.array(pmodel_params.fisher_dial_Vinf) * tc_pow, axis=-1)

    # Convert pressure to bars (1 bar <- 100000 Pa)
    pbar = 1e-5 * patm

    # Calculate the specific volume (cm^3 g^-1):
    spec_vol = vinf_val + lambda_val / (po_val + pbar)

    # Convert to density (g cm^-3) -> 1000 g/kg; 1000000 cm^3/m^3 -> kg/m^3:
    rho = 1e3 / spec_vol

    # CDLO: Method of Chen et al (1997) - I tested this to compare to the TerrA-P
    # code base but I don't think we need it. Preserving the code in case it is
    # needed in the future.
    #
    #     # Calculate density at 1 atm (kg/m^3):
    #     chen_po = np.array([0.99983952, 6.788260e-5 , -9.08659e-6 , 1.022130e-7 ,
    #                         -1.35439e-9 , 1.471150e-11, -1.11663e-13, 5.044070e-16,
    #                         -1.00659e-18])
    #     po = np.sum(np.array(chen_po) * tc_pow[..., :9], axis=-1)
    #
    #     # Calculate bulk modulus at 1 atm (bar):
    #     chen_ko = np.array([19652.17, 148.1830, -2.29995, 0.01281,
    #                         -4.91564e-5, 1.035530e-7])
    #     ko = np.sum(np.array(chen_ko) * tc_pow[..., :6], axis=-1)
    #
    #     # Calculate temperature dependent coefficients:
    #     chen_ca = np.array([3.26138, 5.223e-4, 1.324e-4, -7.655e-7, 8.584e-10])
    #     ca = np.sum(np.array(chen_ca) * tc_pow[..., :5], axis=-1)
    #
    #     chen_cb = np.array([7.2061e-5, -5.8948e-6, 8.69900e-8, -1.0100e-9, 4.3220e-12])
    #     cb = np.sum(np.array(chen_cb) * tc_pow[..., :5], axis=-1)
    #
    #     # Convert atmospheric pressure to bar (1 bar = 100000 Pa)
    #     pbar = 1.0e-5 * patm
    #
    #     rho = (ko + ca * pbar + cb * pbar ** 2.0)
    #     rho /= (ko + ca * pbar + cb * pbar ** 2.0 - pbar)
    #     rho *= 1e3 * po

    return rho


def calc_ftemp_arrh(tk: Union[float, np.ndarray],
                    ha: float,
                    pmodel_params: PModelParams = PModelParams()
                    ) -> Union[float, np.ndarray]:
    r"""Calculates the temperature-scaling factor :math:`f` for enzyme kinetics
    following an Arrhenius response for a given temperature (``tk``, :math:`T`)
    and activation energy (`ha`, :math:`H_a`).

    Arrhenius kinetics are described as:

    .. math::

        x(T)= exp(c - H_a / (T R))

    The temperature-correction function :math:`f(T, H_a)` is:

      .. math::
        :nowrap:

        \[
            \begin{align*}
                f &= \frac{x(T)}{x(T_0)} \\
                  &= exp \left( \frac{ H_a (T - T_0)}{T_0 R T}\right)\text{, or equivalently}\\
                  &= exp \left( \frac{ H_a}{R} \cdot \left(\frac{1}{T_0} - \frac{1}{T}\right)\right)
            \end{align*}
        \]

    Parameters:

        tk: Temperature (in Kelvin)
        ha: Activation energy (in :math:`J \text{mol}^{-1}`)
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.

    Other Parameters:

        To: a standard reference temperature (:math:`T_0`, `pmodel_params.k_To`)
        R: the universal gas constant (:math:`R`, `pmodel_params.k_R`)

    Returns:

        A float value for :math:`f`

    Examples:

        >>> # Relative rate change from 25 to 10 degrees Celsius (percent change)
        >>> round((1.0-calc_ftemp_arrh( 283.15, 100000)) * 100, 4)
        88.1991
    """

    # Note that the following forms are equivalent:
    # exp( ha * (tk - 298.15) / (298.15 * kR * tk) )
    # exp( ha * (tc - 25.0)/(298.15 * kR * (tc + 273.15)) )
    # exp( (ha/kR) * (1/298.15 - 1/tk) )

    tkref = pmodel_params.k_To + pmodel_params.k_CtoK

    return np.exp(ha * (tk - tkref) / (tkref * pmodel_params.k_R * tk))


def calc_ftemp_inst_rd(tc: Union[float, np.ndarray],
                       pmodel_params: PModelParams = PModelParams()
                       ) -> Union[float, np.ndarray]:
    """Calculates the **temperature-scaling factor for dark respiration**
    at a given temperature (``tc``, :math:`T` in °C), relative to the standard
    reference temperature :math:`T_o` (:cite:`Heskel:2016fg`).

    .. math::

            fr = exp( b (T_o - T) -  c ( T_o^2 - T^2 ))

    Parameters:

        tc: Temperature (degrees Celsius)

    Other parameters:

        To: standard reference temperature (:math:`T_o`, `pmodel_params.k_To`)
        b: empirically derived global mean coefficient (:math:`b`, Table 1, ::cite:`Heskel:2016fg`)
        c: empirically derived global mean coefficient (:math:`c`, Table 1, ::cite:`Heskel:2016fg`)


    Returns:

        A float value for :math:`fr`

    Examples:

        >>> # Relative percentage instantaneous change in Rd going from 10 to 25 degrees
        >>> val = (calc_ftemp_inst_rd(25) / calc_ftemp_inst_rd(10) - 1) * 100
        >>> round(val, 4)
        250.9593
    """

    return np.exp(pmodel_params.heskel_b * (tc - pmodel_params.k_To) -
                  pmodel_params.heskel_c * (tc ** 2 - pmodel_params.k_To ** 2))


def calc_ftemp_inst_vcmax(tc: Union[float, np.ndarray],
                          pmodel_params: PModelParams = PModelParams()
                          ) -> Union[float, np.ndarray]:
    r"""This function calculates the **temperature-scaling factor :math:`f` of
    the instantaneous temperature response of :math:`V_{cmax}`** given the
    temperature (:math:`T`) relative to the standard reference temperature
    (:math:`T_0`), following modified Arrhenius kinetics.

    .. math::

       V = f V_{ref}

    The value of :math:`f` is given by :cite:`Kattge:2007db` (Eqn 1) as:

    .. math::

        f = g(T, H_a) \cdot
                \frac{1 + exp( (T_0 \Delta S - H_d) / (T_0 R))}
                     {1 + exp( (T \Delta S - H_d) / (T R))}

    where :math:`g(T, H_a)` is a regular Arrhenius-type temperature response
    function (see :func:`calc_ftemp_arrh`). The term :math:`\Delta S` is the
    entropy factor, calculated as a linear function of :math:`T` in °C following
    :cite:`Kattge:2007db` (Table 3, Eqn 4):

    .. math::

        \Delta S = a + b T

    Parameters:

        tc:  temperature, or in general the temperature relevant for
            photosynthesis (°C)
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.

    Other parameters:

        Ha: activation energy (:math:`H_a`, `pmodel_params.kattge_knorr_Ha`)
        Hd: deactivation energy (:math:`H_d`, `pmodel_params.kattge_knorr_Hd`)
        To: standard reference temperature expressed in Kelvin (`T_0`, `pmodel_params.k_To`)
        R: the universal gas constant (:math:`R`,`pmodel_params.k_R`)
        a: intercept of the entropy factor(:math:`a`, `pmodel_params.kattge_knorr_a_ent`)
        b: slope of the entropy factor (:math:`b`, `pmodel_params.kattge_knorr_b_ent`)

    Returns: A float value for :math:`f`

    Examples:

        >>> # Relative change in Vcmax going (instantaneously, i.e. not
        >>> # not acclimatedly) from 10 to 25 degrees (percent change):
        >>> val = ((calc_ftemp_inst_vcmax(25)/calc_ftemp_inst_vcmax(10)-1) * 100)
        >>> round(val, 4)
        283.1775

    """

    # Convert temperatures to Kelvin
    tkref = pmodel_params.k_To + pmodel_params.k_CtoK
    tk = tc + pmodel_params.k_CtoK

    # Calculate entropy following Kattge & Knorr (2007): slope and intercept
    # are defined using temperature in °C, not K!!! 'tcgrowth' corresponds
    # to 'tmean' in Nicks, 'tc25' is 'to' in Nick's
    dent = pmodel_params.kattge_knorr_a_ent + pmodel_params.kattge_knorr_b_ent * tc
    fva = calc_ftemp_arrh(tk, pmodel_params.kattge_knorr_Ha)
    fvb = ((1 + np.exp((tkref * dent - pmodel_params.kattge_knorr_Hd) /
                       (pmodel_params.k_R * tkref))) /
           (1 + np.exp((tk * dent - pmodel_params.kattge_knorr_Hd) /
                       (pmodel_params.k_R * tk))))

    return fva * fvb

# TODO - update unpublished reference to:
#  Cai, W., and Prentice, I. C.: Recent trends in gross primary production 
#        and their drivers: analysis and modelling at flux-site and global scales,
#        Environ. Res. Lett. 15 124050 https://doi.org/10.1088/1748-9326/abc64e, 2020

def calc_ftemp_kphio(tc: Union[float, np.ndarray],
                     c4: bool = False,
                     pmodel_params: PModelParams = PModelParams()
                     ) -> Union[float, np.ndarray]:
    r"""Calculates the **temperature dependence of the quantum yield
    efficiency**, as a quadratic function of temperature (:math:`T`). The values
    of the coefficients depend on whether C3 or C4 photosynthesis is being
    modelled

    .. math::

        \phi(T) = a + b T - c T^2

    The factor :math:`\phi(T)` is to be multiplied with leaf absorptance and the
    fraction of absorbed light that reaches photosystem II. In the P-model these
    additional factors are lumped into a single apparent quantum yield
    efficiency parameter (argument `kphio` to the class :class:`~pyrealm.pmodel.PModel`).

    Parameters:

        tc: Temperature, relevant for photosynthesis (°C)
        c4: Boolean specifying whether fitted temperature response for C4 plants
            is used. Defaults to \code{FALSE}.
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.

    Other parameters:

        C3: the parameters (:math:`a,b,c`, `pmodel_params.kphio_C3`) are taken from the
            temperature dependence of the maximum quantum yield of photosystem
            II in light-adapted tobacco leaves determined by :cite:`Bernacchi:2003dc`.
        C4: the parameters (:math:`a,b,c`, `pmodel_params.kphio_C4`) are taken from unpublished
            work.

    Returns:

        A float value for :math:`\phi(T)`

    Examples:

        >>> # Relative change in the quantum yield efficiency between 5 and 25
        >>> # degrees celsius (percent change):
        >>> val = (calc_ftemp_kphio(25.0) / calc_ftemp_kphio(5.0) - 1) * 100
        >>> round(val, 5)
        52.03969
        >>> # Relative change in the quantum yield efficiency between 5 and 25
        >>> # degrees celsius (percent change) for a C4 plant:
        >>> val = (calc_ftemp_kphio(25.0, c4=True) /
        ...        calc_ftemp_kphio(5.0, c4=True) - 1) * 100
        >>> round(val, 5)
        432.25806

    """

    if c4:
        coef = pmodel_params.kphio_C4
    else:
        coef = pmodel_params.kphio_C3

    ftemp = coef[0] + coef[1] * tc + coef[2] * tc ** 2
    ftemp = np.clip(ftemp, 0.0, None)
    
    return ftemp


def calc_gammastar(tc: Union[float, np.ndarray],
                   patm: Union[float, np.ndarray],
                   pmodel_params: PModelParams = PModelParams()
                   ) -> Union[float, np.ndarray]:
    r"""Calculates the photorespiratory **CO2 compensation point** in absence of
    dark respiration (:math:`\Gamma^{*}`, ::cite:`Farquhar:1980ft`) as:

    .. math::

        \Gamma^{*} = \Gamma^{*}_{0} \cdot \frac{p}{p_0} \cdot f(T, H_a)

    where :math:`f(T, H_a)` modifies the activation energy to the the local
    temperature following an Arrhenius-type temperature response function
    implemented in :func:`calc_ftemp_arrh`.

    Parameters:

        tc: Temperature relevant for photosynthesis (:math:`T`, °C)
        patm: Atmospheric pressure (:math:`p`, Pascals)
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.

    Other Parameters:

        To: the standard reference temperature (:math:`T_0` )
        Po: the standard pressure (:math:`p_0` )
        gs_0: the reference value of :math:`\Gamma^{*}` at standard temperature
            (:math:`T_0`) and pressure (:math:`P_0`)  (:math:`\Gamma^{*}_{0}`,
            ::cite:`Bernacchi:2001kg`, `pmodel_params.bernacchi_gs25_0`)
        ha: the activation energy (:math:`\Delta H_a`, ::cite:`Bernacchi:2001kg`,
            `pmodel_params.bernacchi_dha`)

    Returns:

        A float value for :math:`\Gamma^{*}` (in Pa)

    Examples:

        >>> # CO2 compensation point at 20 degrees Celsius and standard
        >>> # atmosphere (in Pa) >>> round(calc_gammastar(20, 101325), 5)
        3.33925
    """

    # check inputs, return shape not used
    _ = check_input_shapes(tc, patm)

    return (pmodel_params.bernacchi_gs25_0 * patm / pmodel_params.k_Po *
            calc_ftemp_arrh((tc + pmodel_params.k_CtoK), ha=pmodel_params.bernacchi_dha))


def calc_ns_star(tc: Union[float, np.ndarray],
                 patm: Union[float, np.ndarray],
                 pmodel_params: PModelParams = PModelParams()
                 ) -> Union[float, np.ndarray]:

    r"""Calculates the relative viscosity of water (:math:`\eta^*`), given the
    standard temperature and pressure, using :func:`~pyrealm.pmodel.calc_viscosity_h20`
    (:math:`v(t,p)`) as:

    .. math::

        \eta^* = \frac{v(t,p)}{v(t_0,p_0)}

    Parameters:

        tc: Temperature, relevant for photosynthesis (:math:`T`, °C)
        patm: Atmospheric pressure (:math:`p`, Pa)
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.

    Other parameters:

        To: standard temperature (:math:`t0`, `pmodel_params.k_To`)
        Po: standard pressure (:math:`p_0`, `pmodel_params.k_Po`)

    Returns:

        A numeric value for :math:`\eta^*` (a unitless ratio)

    Examples:

        >>> # Relative viscosity at 20 degrees Celsius and standard
        >>> # atmosphere (in Pa):
        >>> round(calc_ns_star(20, 101325), 5)
        1.12536
    """

    visc_env = calc_viscosity_h2o(tc, patm, pmodel_params = pmodel_params)
    visc_std = calc_viscosity_h2o(pmodel_params.k_To, pmodel_params.k_Po,
                                  pmodel_params = pmodel_params)

    return visc_env / visc_std


def calc_kmm(tc: Union[float, np.ndarray],
             patm: Union[float, np.ndarray],
             pmodel_params: PModelParams = PModelParams()
             ) -> Union[float, np.ndarray]:
    r"""Calculates the **Michaelis Menten coefficient of Rubisco-limited
    assimilation** (:math:`K`, ::cite:`Farquhar:1980ft`) as a function of
    temperature (:math:`T`) and atmospheric pressure (:math:`p`) as:

      .. math:: K = K_c ( 1 + p_{\ce{O2}} / K_o),

    where, :math:`p_{\ce{O2}} = 0.209476 \cdot p` is the partial pressure of
    oxygen. :math:`f(T, H_a)` is an Arrhenius-type temperature response of
    activation energies (:func:`calc_ftemp_arrh`) used to correct
    Michalis constants at standard temperature for both :math:`\ce{CO2}` and
    :math:`\ce{O2}` to the local temperature (Table 1, ::cite:`Bernacchi:2001kg`):

      .. math::
        :nowrap:

        \[
            \begin{align*}
                K_c &= K_{c25} \cdot f(T, H_{kc})\\
                K_o &= K_{o25} \cdot f(T, H_{ko})
            \end{align*}
        \]

    .. TODO - why this height? Inconsistent with calc_gammastar which uses P_0
              for the same conversion for a value in the same table.

    Parameters:

        tc: Temperature, relevant for photosynthesis (:math:`T`, °C)
        patm: Atmospheric pressure (:math:`p`, Pa)
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.

    Other parameters:

        hac: activation energy for :math:`\ce{CO2}` (:math:`H_{kc}`, `pmodel_params.bernacchi_dhac`)
        hao:  activation energy for :math:`\ce{O2}` (:math:`\Delta H_{ko}`, `pmodel_params.bernacchi_dhao`)
        kc25: Michelis constant for :math:`\ce{CO2}` at standard temperature
            (:math:`K_{c25}`, `pmodel_params.bernacchi_kc25`)
        ko25: Michelis constant for :math:`\ce{O2}` at standard temperature
            (:math:`K_{o25}`, `pmodel_params.bernacchi_ko25`)

    Returns:

        A numeric value for :math:`K` (in Pa)

    Examples:

        >>> # Michaelis-Menten coefficient at 20 degrees Celsius and standard
        >>> # atmosphere (in Pa):
        >>> round(calc_kmm(20, 101325), 5)
        46.09928

    """

    # Check inputs, return shape not used
    _ = check_input_shapes(tc, patm)

    # conversion to Kelvin
    tk = tc + pmodel_params.k_CtoK

    kc = pmodel_params.bernacchi_kc25 * calc_ftemp_arrh(tk, ha=pmodel_params.bernacchi_dhac)
    ko = pmodel_params.bernacchi_ko25 * calc_ftemp_arrh(tk, ha=pmodel_params.bernacchi_dhao)

    # O2 partial pressure
    po = pmodel_params.k_co * 1e-6 * patm

    return kc * (1.0 + po/ko)


def calc_soilmstress(soilm: Union[float, np.ndarray],
                     meanalpha: Union[float, np.ndarray] = 1.0,
                     pmodel_params: PModelParams = PModelParams()
                     ) -> Union[float, np.ndarray]:
    r"""Calculates an **empirical soil moisture stress factor**  (:math:`\beta`,
    ::cite:`Stocker:2020dh`) as a function of relative soil moisture
    (:math:`m_s`, fraction of field capacity) and average aridity, quantified by
    the local annual mean ratio of actual over potential evapotranspiration
    (:math:`\bar{\alpha}`).

    The value of :math:`\beta` is defined relative to two soil moisture
    thresholds (:math:`\theta_0, \theta^{*}`) as:

      .. math::
        :nowrap:

        \[
            \beta =
                \begin{cases}
                    0
                    q(m_s - \theta^{*})^2 + 1,  & \theta_0 < m_s <= \theta^{*} \\
                    1, &  \theta^{*} < m_s,
                \end{cases}
        \]

    where :math:`q` is an aridity sensitivity parameter setting the stress
    factor at :math:`\theta_0`:

    .. math:: q=(1 - (a + b \bar{\alpha}))/(\theta^{*} - \theta_{0})^2

    Default parameters of :math:`a=0` and :math:`b=0.7330` are as described in
    Table 1 of :cite:`Stocker:2020dh` specifically for the 'FULL' use case, with
    ``method_jmaxlim="wang17"``, ``do_ftemp_kphio=TRUE``.


    Parameters:

        soilm: Relative soil moisture as a fraction of field capacity
            (unitless). Defaults to 1.0 (no soil moisture stress).
        meanalpha: Local annual mean ratio of actual over potential
            evapotranspiration, measure for average aridity. Defaults to 1.0.
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.

    Other parameters:

        theta0: lower bound of soil moisture (:math:`\theta_0`, `pmodel_params.soilmstress_theta0`).
        thetastar: upper bound of soil moisture (:math:`\theta^{*}`, `pmodel_params.soilmstress_thetastar`).
        a: aridity parameter (:math:`a`, `pmodel_params.soilmstress_a`).
        b: aridity parameter (:math:`b`, `pmodel_params.soilmstress_b`).

    Returns:

        A numeric value for :math:`\beta`

    Examples:

        >>> # Relative reduction (%) in GPP due to soil moisture stress at
        >>> # relative soil water content ('soilm') of 0.2:
        >>> round((calc_soilmstress(0.2) - 1) * 100, 5)
        -11.86667
    """
    
    # TODO - presumably this should also have beta(theta) = 0 when m_s <=
    #        theta_0. Actually, no - these limits aren't correct. This is only
    #        true when meanalpha=0, otherwise beta > 0 when m_s < theta_0.
    # TODO - move soilm params into standalone param class for this function -
    #        keep the PModelParams cleaner?
        
    # Check inputs, return shape not used
    _ = check_input_shapes(soilm, meanalpha)

    # Calculate outstress
    y0 = (pmodel_params.soilmstress_a + pmodel_params.soilmstress_b * meanalpha)
    beta = (1.0 - y0) / (pmodel_params.soilmstress_theta0 - pmodel_params.soilmstress_thetastar) ** 2
    outstress = 1.0 - beta * (soilm - pmodel_params.soilmstress_thetastar) ** 2

    # Filter wrt to thetastar
    outstress = np.where(soilm <= pmodel_params.soilmstress_thetastar, outstress, 1.0)

    # Clip
    outstress = np.clip(outstress, 0.0, 1.0)

    return outstress


def calc_viscosity_h2o(tc: Union[float, np.ndarray],
                       patm: Union[float, np.ndarray],
                       pmodel_params: PModelParams = PModelParams(),
                       simple: bool = False) -> Union[float, np.ndarray]:
    r"""Calculates the **viscosity of water** (:math:`\eta`) as a function of
    temperature and atmospheric pressure (::cite:`Huber:2009fy`). 

    Parameters:

        tc: air temperature (°C)
        patm: atmospheric pressure (Pa)
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.
        simple: Use the simple formulation.

    Returns:

        A float giving the viscosity of water (mu, Pa s)

    Examples:

        >>> # Density of water at 20 degrees C and standard atmospheric pressure:
        >>> round(calc_viscosity_h2o(20, 101325), 7)
        0.0010016
    """

    # Check inputs, return shape not used
    _ = check_input_shapes(tc, patm)

    if simple or pmodel_params.simple_viscosity:
        # The reference for this is unknown, but is used in some implementations
        # so is included here to allow intercomparison.
        return np.exp(-3.719 + 580/((tc + 273) - 138))

    # Get the density of water, kg/m^3
    rho = calc_density_h2o(tc, patm, pmodel_params=pmodel_params)

    # Calculate dimensionless parameters:
    tbar = (tc + pmodel_params.k_CtoK) / pmodel_params.huber_tk_ast
    rbar = rho / pmodel_params.huber_rho_ast

    # Calculate mu0 (Eq. 11 & Table 2, Huber et al., 2009):
    tbar_pow = np.power.outer(tbar, np.arange(0, 4))
    mu0 = (1e2 * np.sqrt(tbar)) / np.sum(np.array(pmodel_params.huber_H_i) / tbar_pow, axis=-1)

    # Calculate mu1 (Eq. 12 & Table 3, Huber et al., 2009):
    h_array = np.array(pmodel_params.huber_H_ij)
    ctbar = (1.0 / tbar) - 1.0
    row_j, _ = np.indices(h_array.shape)
    mu1 = h_array * np.power.outer(rbar - 1.0, row_j)
    mu1 = np.power.outer(ctbar, np.arange(0, 6)) * np.sum(mu1, axis=(-2))
    mu1 = np.exp(rbar * mu1.sum(axis=-1))

    # Calculate mu_bar (Eq. 2, Huber et al., 2009), assumes mu2 = 1
    mu_bar = mu0 * mu1

    # Calculate mu (Eq. 1, Huber et al., 2009)
    return mu_bar * pmodel_params.huber_mu_ast  # Pa s


def calc_patm(elv: Union[float, np.ndarray],
              pmodel_params: PModelParams = PModelParams()
              ) -> Union[float, np.ndarray]:
    r"""Calculates **atmospheric pressure** as a function of elevation with reference to
    the standard atmosphere.  The elevation-dependence of atmospheric pressure
    is computed by assuming a linear decrease in temperature with elevation and
    a mean adiabatic lapse rate (Eqn 3, ::cite:`BerberanSantos:2009bk`):

    .. math::

        p(z) = p_0 ( 1 - L z / K_0) ^{ G M / (R L) },

    Parameters:

        elv: Elevation above sea-level (:math:`z`, metres above sea level.)
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.

    Other parameters:

        G: gravity constant (:math:`g`, `pmodel_params.k_G`)
        Po: standard atmospheric pressure at sea level (:math:`p_0`, `pmodel_params.k_Po`)
        L: adiabatic temperature lapse rate (:math:`L}`, `pmodel_params.k_L`),
        M: molecular weight for dry air (:math:`M`, `pmodel_params.k_Ma`),
        R: universal gas constant (:math:`R`, `pmodel_params.k_R`)
        Ko: reference temperature in Kelvin (:math:`K_0`, `pmodel_params.k_To`).

    Returns:

        A numeric value for :math:`p` in Pascals.

    Examples:

        >>> # Standard atmospheric pressure, in Pa, corrected for 1000 m.a.s.l.
        >>> round(calc_patm(1000), 2)
        90241.54

    """

    # Convert elevation to pressure, Pa. This equation uses the base temperature
    # in Kelvins, while other functions use this constant in the PARAM units of
    # °C.

    kto = pmodel_params.k_To + pmodel_params.k_CtoK

    return (pmodel_params.k_Po * (1.0 - pmodel_params.k_L * elv / kto) **
            (pmodel_params.k_G * pmodel_params.k_Ma /
             (pmodel_params.k_R * pmodel_params.k_L)))


def calc_co2_to_ca(co2: Union[float, np.ndarray],
                   patm: Union[float, np.ndarray],
                   ) -> Union[float, np.ndarray]:
    r"""Converts ambient :math:`\ce{CO2}` (:math:`c_a`) in part per million to
    Pascals, accounting for atmospheric pressure.

    Parameters:
        co2 (float): atmospheric :math:`\ce{CO2}`, ppm
        patm (float): atmospheric pressure, Pa

    Returns:
        Ambient :math:`\ce{CO2}` in units of Pa

    Examples:
        >>> np.round(calc_co2_to_ca(413.03, 101325), 6)
        41.850265
    """


    return 1.0e-6 * co2 * patm  # Pa, atms. CO2


# Design notes on PModel (0.3.1 -> 0.4.0)
# The PModel until 0.3.1 was a single class taking tc etc. as inputs. However
# a common use case would be to look at how the PModel predictions change with
# different options. I (DO) did consider retaining the single class and having
# PModel __init__ create the environment and then have PModel.fit(), but
# having two classes seemed to better separate the physiological model (PModel
# class and attributes) from the environment the model is being fitted to and
# also creates _separate_ PModel objects.

# Design notes on PModel (0.4.0 -> 0.5.0)
# In separating PPFD and FAPAR into a second step, I had created the IabsScaled
# class to store variables that scale linearly with Iabs. That class held and
# exposed scaled and unscaled versions of several parameteres. For a start, that
# was a bad class name since the values could be unscaled, but also most of the
# unscaled versions are never really used. Really (hat tip, Keith Bloomfield),
# there are two meaningful _efficiency_ variables (LUE, IWUE) and then a set of
# productivity variables. The new structure reflects that, removing the
# un-needed unscaled variables and simplifying the structure.


class PModelEnvironment:

    r"""Create a PModelEnvironment instance using the input parameters.

    This class takes the four key environmental inputs to the P Model and
    calculates four photosynthetic variables for those environmental
    conditions:

    * the photorespiratory CO2 compensation point (:math:`\Gamma^{*}`,
      :func:`~pyrealm.pmodel.calc_gammastar`),
    * the relative viscosity of water (:math:`\eta^*`,
      :func:`~pyrealm.pmodel.calc_ns_star`),
    * the ambient partial pressure of :math:`\ce{CO2}` (:math:`c_a`,
      :func:`~pyrealm.pmodel.calc_c02_to_ca`) and
    * the Michaelis Menten coefficient of Rubisco-limited assimilation
      (:math:`K`, :func:`~pyrealm.pmodel.calc_kmm`).

    These variables can then be used to fit P models using different
    configurations. Note that the underlying parameters of the P model
    (:class:`~pyrealm.param_classes.PModelParams`) are set when creating
    an instance of this class.

    Parameters:

        tc: Temperature, relevant for photosynthesis (°C)
        vpd: Vapour pressure deficit (Pa)
        co2: Atmospheric CO2 concentration (ppm)
        patm: Atmospheric pressure (Pa).
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.
    """

    def __init__(self,
                 tc: Union[float, np.ndarray],
                 vpd: Union[float, np.ndarray],
                 co2: Union[float, np.ndarray],
                 patm: Union[float, np.ndarray],
                 pmodel_params: PModelParams = PModelParams()):

        self.shape = check_input_shapes(tc, vpd, co2, patm)

        # Validate and store the forcing variables
        self.tc = bounds_checker(tc, -25, 80, '[]', 'tc', '°C')
        self.vpd = bounds_checker(vpd, 0, 10000, '[]', 'vpd', 'Pa')
        self.co2 = bounds_checker(co2, 0, 1000, '[]', 'co2', 'ppm')
        self.patm = bounds_checker(patm, 30000, 110000, '[]', 'tc', '°C')

        # Guard against calc_density issues
        if np.nanmin(self.tc) < -25:
            raise ValueError('Cannot calculate P Model predictions for values below -25°C. See calc_density_h2o.')

        # Guard against negative VPD issues
        if np.nanmin(self.vpd) < 0:
            raise ValueError('Negative VPD values will lead to missing data - clip to zero or explicitly set to np.nan')

        # ambient CO2 partial pressure (Pa)
        self.ca = calc_co2_to_ca(self.co2, self.patm)

        # photorespiratory compensation point - Gamma-star (Pa)
        self.gammastar = calc_gammastar(tc, patm, pmodel_params=pmodel_params)

        # Michaelis-Menten coef. (Pa)
        self.kmm = calc_kmm(tc, patm, pmodel_params=pmodel_params)

        # viscosity correction factor relative to standards
        self.ns_star = calc_ns_star(tc, patm, pmodel_params=pmodel_params)  # (unitless)

        # Store parameters
        self.pmodel_params = pmodel_params

    def __repr__(self):

        # DESIGN NOTE: This is deliberately extremely terse. It could contain
        # a bunch of info on the environment but that would be quite spammy
        # on screen. Having a specific summary method that provides that info
        # is more user friendly.

        return f"PModelEnvironment(shape={self.shape})"

    def summarize(self, dp=2):
        """Prints a summary of the input and photosynthetic attributes in a
        instance of a PModelEnvironment including the mean, range and number
        of nan values.

        Args:
            dp: The number of decimal places used in rounding summary stats.

        Returns:
            None
        """

        attrs = [('tc', '°C'), ('vpd', 'Pa'), ('co2', 'ppm'), 
                 ('patm', 'Pa'), ('ca', 'Pa'), ('gammastar', 'Pa'), 
                 ('kmm', 'Pa'), ('ns_star', '-')]
        summarize_attrs(self, attrs, dp=dp)


class PModel:

    r"""Fits the P Model to a given set of environmental and photosynthetic
    parameters. The calculated attributes of the class are described below. An
    extended description with typical use cases is given in
    :any:`pmodel_overview` but the basic flow of the model is:

    1. Estimate :math:`\ce{CO2}` limitation factors and optimal internal to
       ambient :math:`\ce{CO2}` partial pressure ratios (:math:`\chi`), using
       :class:`~pyrealm.pmodel.CalcOptimalChi`.
    2. Estimate limitation factors to :math:`V_{cmax}` and :math:`J_{max}` 
       using :class:`~pyrealm.pmodel.JmaxLimitation`.
    3. Optionally, estimate productivity measures including GPP by supplying
       FAPAR and PPFD using the
       :meth:`~pyrealm.pmodel.PModel.estimate_productivity` method.

    The model predictions from step 1 and 2 are then:

    * Intrinsic water use efficiency (iWUE,
      :math:`\mu\mathrm{mol}\;\mathrm{mol}^{-1}`), calculated as :math:`( 5/8 *
      (c_a - c_i)) / P`, where `c_a` and `c_i` are measured in Pa and :math:`P`
      is atmospheric pressure in megapascals. This is equivalent to :math:`(c_a
      - c_i)/1.6` when `c_a` and `c_i` are expressed as parts per million.

    * The light use efficienciy (LUE, gC mol-1), calculated as:
    
        .. math::

            \text{LUE} = \phi_0 \cdot m_j \cdot f_v \cdot M_C \cdot \beta(\theta),

      where :math:`f_v` is a limitation factor defined in 
      :class:`~pyrealm.pmodel.JmaxLimitation`, :math:`M_C` is the molar mass of
      carbon and :math:`\beta(\theta)` is an empirical soil moisture factor 
      (see :func:`~pyrealm.pmodel.calc_soilmstress`,  :cite:`Stocker:2020dh`).

    After running :meth:`~pyrealm.pmodel.PModel.estimate_productivity`, the following
    predictions are also populated:

    * Gross primary productivity, calculated as 
      :math:`\text{GPP} = \text{LUE} \cdot I_{abs}`, where :math:`I_{abs}` is the 
      absorbed photosynthetic radiation 

    * The maximum rate of Rubisco regeneration at the growth temperature
      (:math:`J_{max}`)

    * The maximum carboxylation capacity (mol C m-2) at the growth temperature
      (:math:`V_{cmax}`).

    These two predictions are calculated as follows: 

        .. math::
            :nowrap:

            \[
                \begin{align*}
                V_{cmax} &= \phi_{0} I_{abs} \frac{m}{m_c} f_{v} \\
                J_{max} &= 4 \phi_{0} I_{abs} f_{j} \\
                \end{align*}
            \]

    where  :math:`f_v, f_j` are limitation terms described in
    :class:`~pyrealm.pmodel.JmaxLimitation`

    * The maximum carboxylation capacity (mol C m-2) normalised to the standard
      temperature as: :math:`V_{cmax25} = V_{cmax}  / fv(t)`, where :math:`fv(t)` is
      the instantaneous temperature response of :math:`V_{cmax}` implemented in
      :func:`~pyrealm.pmodel.calc_ftemp_inst_vcmax`

    * Dark respiration, calculated as:

        .. math::

            R_d = b_0 \frac{fr(t)}{fv(t)} V_{cmax}

      following :cite:`Atkin:2015hk`, where :math:`fr(t)` is the instantaneous 
      temperature response of dark respiration implemented in
      :func:`~pyrealm.pmodel.calc_ftemp_inst_rd`, and :math:`b_0` is set 
      in :attr:`~pyrealm.pmodel_params.atkin_rd_to_vcmax`.

    * Stomatal conductance (:math:`g_s`), calculated as:

        .. math::

            g_s = \frac{LUE}{M_C}\frac{1}{c_a - c_i}

      When C4 photosynthesis is being used, the true partial pressure of CO2
      in the substomatal cavities (:math:`c_i`) is used following the
      calculation of :math:`\chi` using
      :attr:`~pyrealm.param_classes.PModelParams.beta_cost_ratio_c4`


    Parameters:

        env: An instance of :class:`~pyrealm.pmodel.PModelEnvironment`. 
        kphio: (Optional) The quantum yield efficiency of photosynthesis
            (:math:`\phi_0`, unitless). Note that :math:`\phi_0` is 
            sometimes used to refer to the quantum yield of electron transfer,
            which is exactly four times larger, so check definitions here.
        rootzonestress: (Optional, default=None) An experimental option
            for providing a root zone water stress factor. This is not
            compatible with the soilmstress approach.
        soilmstress: (Optional, default=None) A soil moisture stress factor
            calculated using :func:`~pyrealm.pmodel.calc_soilmstress`.
        c4: (Optional, default=False) Selects the C3 or C4 photosynthetic
            pathway. 
        method_jmaxlim: (Optional, default=`wang17`) Method to use for
            :math:`J_{max}` limitation
        do_ftemp_kphio: (Optional, default=True) Include the temperature-
            dependence of quantum yield efficiency (see
            :func:`~pyrealm.pmodel.calc_ftemp_kphio`).

    Attributes:

        env: The photosynthetic environment to which the model is fitted
            (:class:`~pyrealm.pmodel.PModelEnvironment`)
        pmodel_params: The parameters used in the underlying calculations
            (:class:`~pyrealm.param_classes.PModelParams`)
        optchi: Details of the optimal chi calculation
            (:class:`~pyrealm.pmodel.CalcOptimalChi`)
        init_kphio: The initial value of :math:`\phi_0`.
        kphio: The value of :math:`\phi_0` used in calculations with 
            any temperature correction applied.
        iwue: Intrinsic water use efficiency (iWUE, µmol mol-1) 
        lue: Light use efficiency (LUE, g C mol-1)

    After :meth:`~pyrealm.pmodel.estimate_productivity` has been run,
    the following attributes are also populated. See the documentation
    for :meth:`~pyrealm.pmodel.estimate_productivity` for details.

    Attributes:

        gpp: Gross primary productivity (µg C m-2 s-1)
        rd: Dark respiration (µmol m-2 s-1)
        vcmax: Maximum rate of carboxylation (µmol m-2 s-1)
        vcmax25: Maximum rate of carboxylation at standard temperature (µmol m-2 s-1)
        jmax: Maximum rate of electron transport (µmol m-2 s-1)
        gs: Stomatal conductance (µmol m-2 s-1)

    Examples:

        >>> env = PModelEnvironment(tc=20, vpd=1000, co2=400, patm=101325.0)
        >>> mod_c3 = PModel(env)
        >>> # Key variables from pmodel
        >>> np.round(mod_c3.optchi.ci, 5)
        28.14209
        >>> np.round(mod_c3.optchi.chi, 5)
        0.69435
        >>> mod_c3.estimate_productivity(fapar=1, ppfd=300)
        >>> np.round(mod_c3.gpp, 5)
        76.42545
        >>> mod_c4 = PModel(env, c4=True, method_jmaxlim='none')
        >>> # Key variables from PModel
        >>> np.round(mod_c4.optchi.ci, 5)
        18.22528
        >>> np.round(mod_c4.optchi.chi, 5)
        0.44967
        >>> mod_c4.estimate_productivity(fapar=1, ppfd=300)
        >>> np.round(mod_c4.gpp, 5)
        103.25886
    """

    def __init__(self,
                 env: PModelEnvironment,
                 rootzonestress: Optional[Union[float, np.ndarray]] = None,
                 soilmstress: Optional[Union[float, np.ndarray]] = None,
                 kphio: Optional[float] = None,
                 do_ftemp_kphio: bool = True,
                 c4: bool = False,
                 method_jmaxlim: str = "wang17",
                 ):

        # Check possible array inputs against the photosynthetic environment
        self.shape = check_input_shapes(env.gammastar, soilmstress, rootzonestress)

        # Store a reference to the photosynthetic environment and a direct
        # reference to the parameterisation
        self.env = env
        self.pmodel_params = env.pmodel_params

        # ---------------------------------------------
        # Soil moisture and root zone stress handling
        # ---------------------------------------------

        if soilmstress is not None and rootzonestress is not None:
            raise AttributeError("Soilmstress and rootzonestress are alternative "
                                 "approaches to soil moisture effects. Do not use both.")

        if soilmstress is None:
            self.soilmstress = 1.0
            self.do_soilmstress = False
        else:
            self.soilmstress = soilmstress
            self.do_soilmstress = True

        if rootzonestress is None:
            rootzonestress = 1.0
            self.do_rootzonestress = False
        else:
            self.do_rootzonestress = True

        # kphio defaults:
        self.do_ftemp_kphio = do_ftemp_kphio
        if kphio is None:
            if not self.do_ftemp_kphio:
                self.init_kphio = 0.049977
            elif self.do_soilmstress:
                self.init_kphio = 0.087182
            else:
                self.init_kphio = 0.081785
        else:
            self.init_kphio = kphio

        # -----------------------------------------------------------------------
        # Temperature dependence of quantum yield efficiency
        # -----------------------------------------------------------------------
        # 'calc_ftemp_kphio' is the temperature-dependency of the quantum yield
        # efficiency after Bernacchi et al., 2003

        if self.do_ftemp_kphio:
            ftemp_kphio = calc_ftemp_kphio(env.tc, c4,
                                           pmodel_params=env.pmodel_params)
            self.kphio = self.init_kphio * ftemp_kphio 
        else:
            self.kphio = self.init_kphio 

        # -----------------------------------------------------------------------
        # Optimal ci
        # The heart of the P-model: calculate ci:ca ratio (chi) and additional terms
        # -----------------------------------------------------------------------
        self.c4 = c4

        if self.c4:
            method_optci = "c4"
        else:
            method_optci = "prentice14"

        self.optchi = CalcOptimalChi(env=env, method=method_optci,
                                     rootzonestress=rootzonestress,
                                     pmodel_params=env.pmodel_params)

        # -----------------------------------------------------------------------
        # Calculation of Jmax limitation terms
        # -----------------------------------------------------------------------

        self.method_jmaxlim = method_jmaxlim

        self.jmaxlim = JmaxLimitation(self.optchi,
                                      method=self.method_jmaxlim,
                                      pmodel_params=env.pmodel_params)

        # -----------------------------------------------------------------------
        # Store the two efficiency predictions
        # -----------------------------------------------------------------------

        # Intrinsic water use efficiency (in µmol mol-1). The rpmodel reports this
        # in Pascals, but more commonly reported in µmol mol-1. The standard equation
        # (ca - ci) / 1.6 expects inputs in ppm, so the pascal versions are back
        # converted here.
        self.iwue = (5/8 * (env.ca - self.optchi.ci)) / (1e-6 * self.env.patm)

        # The basic calculation of LUE = phi0 * M_c * m but here we implement
        # two penalty terms for jmax limitation and Stocker beta soil moisture
        # stress 
        # Note: the rpmodel implementation also estimates soilmstress effects on
        #       jmax and vcmax but pyrealm.pmodel only applies the stress factor
        #       to LUE and hence GPP
        self.lue = (self.kphio * self.optchi.mj * self.jmaxlim.f_v 
                     * self.pmodel_params.k_c_molmass * self.soilmstress)

        # -----------------------------------------------------------------------
        # Define attributes populated by estimate_productivity method
        # -----------------------------------------------------------------------
        self._vcmax = None
        self._vcmax25 = None
        self._rd = None
        self._jmax = None
        self._gpp = None
        self._gs = None

    def _soilwarn(self, varname: str) -> None:
        """The empirical soil moisture stress factor (Stocker et al. 2020) _can_
        be used to back calculate realistic Jmax and Vcmax values. The pyrealm.PModel
        implementation does not do so and this helper function is used to warn users
        within property getter functions"""
        
        if self.do_soilmstress:
            warn(f'pyrealm.PModel does not correct {varname} for empirical soil moisture effects on LUE.')

    @property
    def gpp(self) -> Union[float, np.ndarray]:
        """Cannot return GPP if estimate_productivity has not been run, do
           not return None silently"""
        if self._gpp is None:
            raise RuntimeError('GPP not calculated: use estimate_productivity')

        return self._gpp

    @property
    def vcmax(self) -> Union[float, np.ndarray]:
        """Cannot return V_cmax if estimate_productivity has not been run, do
           not return None silently. Also screen for soilmoisture, which is
           calculated differently in rpmodel.
           """

        if self._vcmax is None:
            raise RuntimeError('vcmax not calculated: use estimate_productivity')

        self._soilwarn('vcmax')
        return self._vcmax

    @property
    def vcmax25(self) -> Union[float, np.ndarray]:
        """Cannot return V_cmax25 if estimate_productivity has not been run, do
           not return None silently"""
        if self._vcmax25 is None:
            raise RuntimeError('vcmax25 not calculated: use estimate_productivity')

        self._soilwarn('vcmax25')
        return self._vcmax25

    @property
    def rd(self) -> Union[float, np.ndarray]:
        """Cannot return RD if estimate_productivity has not been run, do
           not return None silently"""
        if self._rd is None:
            raise RuntimeError('RD not calculated: use estimate_productivity')

        self._soilwarn('rd')
        return self._rd

    @property
    def jmax(self) -> Union[float, np.ndarray]:
        """Cannot return Jmax if estimate_productivity has not been run, do
           not return None silently"""
        if self._jmax is None:
            raise RuntimeError('Jmax not calculated: use estimate_productivity')

        self._soilwarn('jmax')
        return self._jmax

    @property
    def gs(self) -> Union[float, np.ndarray]:
        """Cannot return gs if estimate_productivity has not been run, do
           not return None silently"""
        if self._gs is None:
            raise RuntimeError('GS not calculated: use estimate_productivity')

        self._soilwarn('gs')
        return self._gs

    def estimate_productivity(self,
                              fapar: Union[float, np.ndarray] = 1,
                              ppfd: Union[float, np.ndarray] = 1):
        r""" This function takes the light use efficiency and Vcmax per unit
        absorbed irradiance and populates the PModel instance with estimates
        of the following:

            * gpp: Gross primary productivity
            * rd: Dark respiration
            * vcmax: Maximum rate of carboxylation
            * vcmax25: Maximum rate of carboxylation at standard temperature
            * jmax: Maximum rate of electron transport.
            * gs: Stomatal conductance

        The functions finds the total absorbed irradiance (:math:`I_{abs}`) as
        the product of the photosynthetic photon flux density (PPFD, `ppfd`) and
        the fraction of absorbed photosynthetically active radiation (`fapar`).

        The default values of ``ppfd`` and ``fapar`` provide estimates of the
        variables above per unit absorbed irradiance. 

        PPFD _must_ be provided in units of micromols per metre square per 
        second (µmol m-2 s-1). This is required to ensure that values of 
        :math:`J_{max}` and :math:`V_{cmax}` are also in µmol m-2 s-1.

        Args:
            fapar: the fraction of absorbed photosynthetically active radiation (-)
            ppfd: photosynthetic photon flux density (µmol m-2 s-1)
        """

        # Check input shapes against each other and an existing calculated value
        _ = check_input_shapes(ppfd, fapar, self.lue)
        
        # Calculate Iabs 
        iabs = fapar * ppfd
        
        # GPP
        self._gpp = self.lue * iabs

        # V_cmax
        self._vcmax = self.kphio * iabs * self.optchi.mjoc * self.jmaxlim.f_v

        # V_cmax25 (vcmax normalized to pmodel_params.k_To)
        ftemp25_inst_vcmax = calc_ftemp_inst_vcmax(self.env.tc,
                                                   pmodel_params=self.pmodel_params)
        self._vcmax25 = self._vcmax / ftemp25_inst_vcmax

        # Dark respiration at growth temperature
        ftemp_inst_rd = calc_ftemp_inst_rd(self.env.tc,
                                           pmodel_params=self.pmodel_params)
        self._rd = (self.pmodel_params.atkin_rd_to_vcmax *
                    (ftemp_inst_rd / ftemp25_inst_vcmax) * self._vcmax)


        # Calculate Jmax
        self._jmax = 4 * self.kphio * iabs * self.jmaxlim.f_j

        # AJ and AC
        a_j = (self.kphio * iabs * self.optchi.mj * self.jmaxlim.f_v)
        a_c = (self._vcmax * self.optchi.mc)

        assim = np.minimum(a_j, a_c)

        if not self.do_soilmstress and not np.allclose(assim, self._gpp / self.pmodel_params.k_c_molmass, equal_nan=True):
            warn('Assimilation and GPP are not identical')

        # Stomatal conductance
        self._gs = assim / (self.env.ca - self.optchi.ci)

    def __repr__(self):
        if self.do_soilmstress:
            stress = 'Soil moisture'
        elif self.do_rootzonestress:
            stress = 'Root zone'
        else:
            stress = 'None'
        return (f"PModel("
                f"shape={self.shape}, "
                f"initial kphio={self.init_kphio}, "
                f"ftemp_kphio={self.do_ftemp_kphio}, "
                f"c4={self.c4}, "
                f"Jmax_method={self.method_jmaxlim}, "
                f"Water stress={stress})")

    def summarize(self, dp=2):
        """Prints a summary of the calculated values in a PModel instance
        including the mean, range and number of nan values. This will always
        show efficiency variables (LUE and IWUE) and productivity estimates are
        shown if :meth:`~pyrealm.pmodel.PModel.calculate_productivity` has been
        run.

        Args:
            dp: The number of decimal places used in rounding summary stats.

        Returns:
            None
        """

        attrs = [('lue', 'g C mol-1'), 
                 ('iwue', 'µmol mol-1')]

        if self._gpp is not None:
            attrs.extend([('gpp', 'µg C m-2 s-1'),
                          ('vcmax', 'µmol m-2 s-1'),
                          ('vcmax25', 'µmol m-2 s-1'), 
                          ('rd', 'µmol m-2 s-1'),
                          ('gs', 'µmol m-2 s-1'),
                          ('jmax', 'µmol m-2 s-1')])

        summarize_attrs(self, attrs, dp=dp)



class CalcOptimalChi:
    r"""This class provides alternative approaches to calculating the optimal
    :math:`\chi` and :math:`\ce{CO2}` limitation factors. These values are:

    - The optimal ratio of leaf internal to ambient :math:`\ce{CO2}` partial
      pressure (:math:`\chi = c_i/c_a`).
    - The :math:`\ce{CO2}` limitation term for light-limited
      assimilation (:math:`m_j`).
    - The :math:`\ce{CO2}` limitation term for Rubisco-limited
      assimilation  (:math:`m_c`).

    The value for :math:`\chi` is calculated using the parameter :math:`\beta`,
    which differs between C3 and C4 plants. :cite:`Stocker:2020dh` estimated
    $\beta = 146$ for C3 plants, and this is defined as `beta_unit_cost_c3` in
    :class:`~pyrealm.param_classes.PModelParams`. For C4 plants, the default
    value used is $\beta = 146 /  9 \approx 16.222$, defined as
    `beta_unit_cost_c4` in :class:`~pyrealm.param_classes.PModelParams`.

    The chosen method is automatically used to estimate these values when an
    instance is created.

    Attributes:

        env (PModelEnvironment): An instance of PModelEnvironment providing
            the photosynthetic environment for the model.
        method (str): one of ``c4`` or ``prentice14``
        xi (float): defines the sensitivity of :math:`\chi` to the vapour 
            pressure deficit and  is related to the carbon cost of water 
            (Medlyn et al. 2011; Prentice et 2014) # TODO
        chi (float): the ratio of leaf internal to ambient :math:`\ce{CO2}`
            partial pressure (:math:`\chi`).
        mj (float): :math:`\ce{CO2}` limitation factor for light-limited
            assimilation (:math:`m_j`).
        mc (float): :math:`\ce{CO2}` limitation factor for RuBisCO-limited
            assimilation (:math:`m_c`).
        mjoc (float):  :math:`m_j/m_c` ratio

    Returns:

        An instance of :class:`CalcOptimalChi` where the :attr:`chi`,
        :attr:`mj`, :attr:`mc` and :attr:`mjoc` have been populated
        using the chosen method.

    Examples:

        >>> env = PModelEnvironment(tc= 20, patm=101325, co2=400, vpd=1000) 
        >>> vals = CalcOptimalChi(env=env)
        >>> round(vals.chi, 5)
        0.69435
        >>> round(vals.mc, 5)
        0.33408
        >>> round(vals.mj, 5)
        0.7123
        >>> round(vals.mjoc, 5)
        2.13211
        >>> # The c4 method estimates chi but sets the others at 1.
        >>> c4_vals = CalcOptimalChi(env=env, method='c4')
        >>> round(c4_vals.chi, 5)
        0.44967
    """

    # TODO - move chi calc into __init__? Shared between the two methods

    def __init__(self,
                 env: PModelEnvironment,
                 rootzonestress: Union[float, np.ndarray] = 1.0,
                 method: str = 'prentice14',
                 pmodel_params: PModelParams = PModelParams()
                 ):

        # Check rootzone stress is broadcastable to the environment
        self.shape = check_input_shapes(env.ca, rootzonestress)

        # set attribute defaults
        self.xi = None
        self.chi = None
        self.ci = None
        self.mc = None
        self.mj = None
        self.mjoc = None

        # Identify and run the selected method
        self.pmodel_params = pmodel_params
        self.method = method
        all_methods = {'prentice14': self.prentice14, 
                       'c4': self.c4}

        if self.method in all_methods:
            this_method = all_methods[self.method]
            this_method(env = env, rootzonestress=rootzonestress)
        else:
            raise ValueError(f"CalcOptimalChi: method argument '{method}' invalid.")

        # Calculate internal CO2 partial pressure
        self.ci = self.chi * env.ca

    def __repr__(self):

        return f"CalcOptimalChi(shape={self.shape}, method={self.method})"

    def c4(self, env, rootzonestress):
        r"""Optimal :math:`\chi` is calculated following Equation 8 in
        :cite:`Prentice:2014bc` (see :meth:`~pyrealm.pmodel.CalcOptimalChi.prentice14`),
        but using a C4 specific estimate of the unit cost ratio :math:`\beta`,
        specified in :meth:`~pyrealm.param_classes.PModelParams.beta_cost_ratio_c4`.

        This method then simply sets :math:`m_j = m_c = m_{joc} = 1.0` to capture the
        boosted :math:`\ce{CO2}` concentrations at the chloropolast in C4
        photosynthesis.
        """

        # leaf-internal-to-ambient CO2 partial pressure (ci/ca) ratio
        self.xi = np.sqrt((self.pmodel_params.beta_cost_ratio_c4 * rootzonestress *
                            (env.kmm + env.gammastar))
                          / (1.6 * env.ns_star))

        self.chi = (env.gammastar / env.ca + (1.0 - env.gammastar / env.ca) * self.xi 
                    / (self.xi + np.sqrt(env.vpd)))

        # These values need to retain any
        # dimensions of the original inputs - if ftemp_kphio is set to 1.0
        # (i.e. no temperature correction) then the dimensions of tc are lost.

        if self.shape == 1:
            self.mc = 1.0
            self.mj = 1.0
            self.mjoc = 1.0
        else:
            self.mc = np.ones(self.shape)
            self.mj = np.ones(self.shape)
            self.mjoc = np.ones(self.shape)

    def prentice14(self, env, rootzonestress):
        r"""This method calculates key variables as follows:

        Optimal :math:`\chi` is calculated following Equation 8 in
        :cite:`Prentice:2014bc`:

          .. math:: :nowrap:

            \[
                \begin{align*}
                    \chi &= \Gamma^{*} / c_a + (1- \Gamma^{*} / c_a)
                        \xi / (\xi + \sqrt D ), \text{where}\\
                    \xi &= \sqrt{(\beta (K+ \Gamma^{*}) / (1.6 \eta^{*}))}
                \end{align*}
            \]

        The :math:`\ce{CO2}` limitation term of light use efficiency
        (:math:`m_j`) is calculated following Equation 3 in :cite:`Wang:2017go`:

        .. math::

            m_j = \frac{c_a - \Gamma^{*}}
                       {c_a + 2 \Gamma^{*} + 3 \Gamma^{*}
                       \sqrt{\frac{1.6 D \eta^{*}}{\beta(K + \Gamma^{*})}}}

        Finally,  :math:`m_c` is calculated, following Equation 7 in
        :cite:`Stocker:2020dh`, as:

        .. math::

            m_c = \frac{c_i - \Gamma^{*}}{c_i + K},

        where :math:`K` is the Michaelis Menten coefficient of Rubisco-limited
        assimilation.
        """

        # leaf-internal-to-ambient CO2 partial pressure (ci/ca) ratio
        self.xi = np.sqrt((self.pmodel_params.beta_cost_ratio_c3 * rootzonestress *
                           (env.kmm + env.gammastar))
                          / (1.6 * env.ns_star))

        self.chi = (env.gammastar / env.ca +
                    (1.0 - env.gammastar / env.ca) * self.xi /
                    (self.xi + np.sqrt(env.vpd)))

        # Calculate m and mc and m/mc
        self.ci = self.chi * env.ca
        self.mj = (self.ci - env.gammastar) / (self.ci + 2 * env.gammastar)
        self.mc = (self.ci - env.gammastar) / (self.ci + env.kmm)
        self.mjoc = self.mj/self.mc

    def summarize(self, dp=2):
        """Prints a summary of the variables calculated within an instance
        of CalcOptimalChi including the mean, range and number of nan values.

        Args:
            dp: The number of decimal places used in rounding summary stats.

        Returns:
            None
        """

        attrs = [('xi', ' Pa ^ (1/2)'), 
                 ('chi', '-'), 
                 ('mc', '-'),
                 ('mj', '-'),
                 ('mjoc', '-')]
        summarize_attrs(self, attrs, dp=dp)


class JmaxLimitation:
    r"""This class calculates two factors (:math:`f_v` and :math:`f_j`) used to 
    implement :math:`V_{cmax}` and :math:`J_{max}` limitation of photosynthesis. 
    Three methods are currently implemented:

        * ``simple``: applies the 'simple' equations with no limitation. The
          alias ``none`` is also accepted.
        * ``wang17``: applies the framework of :cite:`Wang:2017go`.
        * ``smith19``: applies the framework of :cite:`Smith:2019dv`

    Note that :cite:`Smith:2019dv` defines :math:`\phi_0` as the quantum efficiency of 
    electron transfer, whereas :mod:`pyrealm.PModel` defines :math:`\phi_0` as the quantum 
    efficiency of photosynthesis, which is 4 times smaller. This is why the factors 
    here are a factor of 4 greater than Eqn 15 and 17 in :cite:`Smith:2019dv`.
    
    Arguments:

        optchi: an instance of :class:`CalcOptimalChi` providing the :math:`\ce{CO2}` 
            limitation term of light use efficiency (:math:`m_j`) and the  :math:`\ce{CO2}`
            limitation term for Rubisco assimilation (:math:`m_c`).
        method: method to apply :math:`J_{max}` limitation (default: ``wang17``,
            or ``smith19`` or ``none``)
        pmodel_params: An instance of :class:`~pyrealm.param_classes.PModelParams`.

    Attributes:
        f_j (float): :math:`J_{max}` limitation factor, calculated using the method.
        f_v (float): :math:`V_{cmax}` limitation factor, calculated using the method.
        omega (float): component of :math:`J_{max}` calculation (:cite:`Smith:2019dv`).
        omega_star (float):  component of :math:`J_{max}` calculation (:cite:`Smith:2019dv`).

    Examples:

        >>> env = PModelEnvironment(tc= 20, patm=101325, co2=400, vpd=1000) 
        >>> optchi = CalcOptimalChi(env)
        >>> simple = JmaxLimitation(optchi, method='simple')
        >>> simple.f_j
        1.0
        >>> simple.f_v
        1.0
        >>> wang17 = JmaxLimitation(optchi, method='wang17')
        >>> round(wang17.f_j, 5)
        0.66722
        >>> round(wang17.f_v, 5)
        0.55502
        >>> smith19 = JmaxLimitation(optchi, method='smith19')
        >>> round(smith19.f_j, 5)
        1.10204
        >>> round(smith19.f_v, 5)
        0.75442
    """

    # TODO - apparent incorrectness of wang and smith methods with _ca_ variation,
    #        work well with varying temperature but not _ca_ variation (or
    #        e.g. elevation gradient David Sandoval, REALM meeting, Dec 2020)

    def __init__(self, optchi: CalcOptimalChi,
                 method: str = 'wang17',
                 pmodel_params: PModelParams = PModelParams()
                 ):

        self.shape = check_input_shapes(optchi.mj)

        self.optchi = optchi
        self.method = method
        self.pmodel_params = pmodel_params
        self.f_j = None
        self.f_m = None
        self.omega = None
        self.omega_star = None

        all_methods = {'wang17': self.wang17,
                       'smith19': self.smith19,
                       'simple': self.simple,
                       'none': self.simple}

        # Catch method errors.
        if self.method == 'c4':
            raise ValueError('This class does not implement a fixed method for C4 '
                             'photosynthesis. To replicate rpmodel choose c4=True and '
                             'method="simple"')
        elif self.method not in all_methods:
            raise ValueError(f"JmaxLimitation: method argument '{method}' invalid.")

        # Use the selected method to calculate limitation factors
        this_method = all_methods[self.method]
        this_method()

    def __repr__(self):

        return (f"JmaxLimitation(shape={self.shape})")

    def wang17(self):
        r"""Calculate limitation factors following :cite:`Wang:2017go` The factor
        is described in Equation 49 of :cite:`Wang:2017go` and is the square root term
        at the end of that equation:

            .. math::
                :nowrap:

                \[
                    \begin{align*}
                    f_v &=  \sqrt{ 1 - \frac{c^*}{m} ^{2/3}} \\
                    f_j &=  \sqrt{\frac{m}{c^*} ^{2/3} -1 } \\
                    \end{align*}
                \]

        The variable :math:`c^*` is a cost parameter for maintaining :math:`J_{max}`
        and is set in `pmodel_params.wang_c`.

        """

        # Calculate √ {1 – (c*/m)^(2/3)} (see Eqn 2 of Wang et al 2017) and 
        # √ {(m/c*)^(2/3) - 1} safely, both are undefined where m <= c*.
        vals_defined = np.greater(self.optchi.mj, self.pmodel_params.wang17_c)

        self.f_v = np.sqrt(1 - (self.pmodel_params.wang17_c / self.optchi.mj) ** (2.0 / 3.0),
                           where = vals_defined)
        self.f_j = np.sqrt(( self.optchi.mj / self.pmodel_params.wang17_c) ** (2.0 / 3.0) - 1,
                           where = vals_defined)
        
        # Backfill undefined values
        if isinstance(self.f_v, np.ndarray):
            self.f_j[np.logical_not(vals_defined)] = np.nan
            self.f_v[np.logical_not(vals_defined)] = np.nan
        elif not vals_defined:
            self.f_j = np.nan
            self.f_v = np.nan

    def smith19(self):
        r"""Calculate limitation factors following :cite:`Smith:2019dv`:

        .. math::
            :nowrap:

            \[
                \begin{align*}
                f_v &=  \frac{\omega^*}{2\theta} \\
                f_j &=  \omega\\
                \end{align*}
            \]

        where, 

        .. math::
            :nowrap:

            \[
                \begin{align*}
                \omega &= (1 - 2\theta) + \sqrt{(1-\theta)
                    \left(\frac{1}{\frac{4c}{m}(1 - \theta\frac{4c}{m})}-4\theta\right)}\\
                \omega^* &= 1 + \omega - \sqrt{(1 + \omega) ^2 -4\theta\omega}
                \end{align*}
            \]

        given,

            * :math:`\theta`, (`pmodel_params.smith19_theta`) captures the curved relationship 
              between light intensity and photosynthetic capacity, and 
            * :math:`c`, (`pmodel_params.smith19_c_cost`) as a cost parameter for maintaining
              :math:`J_{max}`, equivalent to :math:`c^\ast = 4c` in the 
              :meth:`~pyrealm.pmodel.JmaxLimitation.wang17` method.
        """

        # Adopted from Nick Smith's code:
        # Calculate omega, see Smith et al., 2019 Ecology Letters  # Eq. S4
        theta = self.pmodel_params.smith19_theta
        c_cost = self.pmodel_params.smith19_c_cost

        # simplification terms for omega calculation
        cm = 4 * c_cost / self.optchi.mj
        v = 1 / (cm * (1 - self.pmodel_params.smith19_theta * cm)) - 4 * theta

        # account for non-linearities at low m values. This code finds
        # the roots of a quadratic function that is defined purely from
        # the scalar theta, so will always be a scalar. The first root
        # is then used to set a filter for calculating omega.

        cap_p = (((1 / 1.4) - 0.7) ** 2 / (1 - theta)) + 3.4
        aquad = -1
        bquad = cap_p
        cquad = -(cap_p * theta)
        roots = np.polynomial.polynomial.polyroots([aquad, bquad, cquad])

        # factors derived as in Smith et al., 2019
        m_star = (4 * c_cost) / roots[0].real
        omega = np.where(self.optchi.mj < m_star,
                         -(1 - (2 * theta)) - np.sqrt((1 - theta) * v),
                         -(1 - (2 * theta)) + np.sqrt((1 - theta) * v))

        # np.where _always_ returns an array, so catch scalars
        self.omega = omega.item() if np.ndim(omega) == 0 else omega

        self.omega_star = (1.0 + self.omega -  # Eq. 18
                           np.sqrt((1.0 + self.omega) ** 2 -
                                   (4.0 * theta * self.omega)))

        # Effect of Jmax limitation - note scaling here. Smith et al use
        # phi0 as as the quantum efficiency of electron transport, which is 
        # 4 times our definition of phio0 as the quantum efficiency of photosynthesis.
        # So omega*/8 theta and omega / 4 are scaled down here  by a factor of 4.
        self.f_v = self.omega_star / (2.0 * theta)
        self.f_j = self.omega 

    def simple(self):
        """This method allows the 'simple' form of the equations to be calculated 
        (:math:`f_v = f_j = 1`)
        """

        # Set Jmax limitation to unity - could define as 1.0 in __init__ and
        # pass here, but setting explicitly within the method for clarity.
        self.f_v = 1.0
        self.f_j = 1.0







# # subdaily Pmodel


# def memory_effect(values: np.ndarray, alpha: float = 0.067):
#     r"""
#     Vcmax and Jmax do not converge instantaneously to acclimated optimal
#     values. This function estimates how the actual Vcmax and Jmax track 
#     a time series of calculated optimal values assuming instant acclimation.

#     The estimation uses the paramater `alpha` (:math:`\alpha`) to control
#     the speed of convergence of the estimated values (:math:`E`) to the 
#     calculated optimal values (:math:`O`):

#     ::math

#         E_{t} = E_{t-1}(1 - \alpha) + O_{t} \alpha 

#     For :math:`t_{0}`, the first value in the optimal values is used so
#     :math:`E_{0} = O_{0}`.
#     """


#     # TODO - NA handling
#     # TODO - think about filters here - I'm sure this is a filter which
#     #        could generalise to longer memory windows.
#     # TODO - need a version that handles time slices for low memory looping
#     #        over arrays.

#     memory_values = np.empty_like(values, dtype=np.float)
#     memory_values[0] = values[0]

#     for idx in range(1, len(memory_values)):
#         memory_values[idx] = memory_values[idx - 1] * (1 - alpha) + values[idx] * alpha

#     return memory_values



# def interpolate_rates_forward(tk: np.ndarray, ha: float, 
#                               values: np.ndarray, values_idx: np.ndarray) -> np.ndarray:
#     """
#     This is a specialised interpolation function used for Jmax and Vcmax. Given
#     a time series of temperatures in Kelvin (`tk`) and a set of Jmax25 or
#     Vcmax25 values observed at indices (`values_idx`) along that time series,
#     this pushes those values along the time series and then rescales to the
#     observed temperatures.

#     The effect is that the plant 'sets' its response at a given point of the day
#     and then maintains that same behaviour until a similar reference time the
#     following day.

#     Note that the beginning of the sequence will be filled with np.nan values
#     unless values_idx[0] = 0.

#     Arguments:
#         tk: A time series of temperature values (Kelvin)
#         ha: An Arrhenius constant.
#         values: An array of rates at standard temperature predicted at points along tk.
#         values_idx: The indices of tk at which values are predicted.
#     """
    
#     v = np.empty_like(tk)
#     v[:] = np.nan

#     v[values_idx] = values
#     v = bn.push(v)

#     return v * calc_ftemp_arrh(tk=tk, ha=ha)
