"""
Formalisms exposed in the article for the BRIN model.
"""


def chilling_unit(temp_min, temp_max, q_10):
    """Computes the chilling unit of a given day.

    References:
        - eq6

    Args:
        temp_min (float): [°C] the minimum temperature of the day
        temp_max (float): [°C] the maximum temperature of the day
        q_10 (float): [?] coefficient

    Returns:
        (float): [-] the chilling unit
    """
    return q_10 ** (-temp_max / 10.) + q_10 ** (-temp_min / 10.)


def forcing_unit(temp_min, temp_max, temp_min_next_day, temp_0bc, temp_mbc):
    """Computes daily forcing temperature unit.

    Notes: Computation is based on the sum of hourly effective temperatures.

    References:
        - eq4
        - eq5

    Args:
        temp_min (float): [°C] the daily minimum temperature
        temp_max (float): [°C] the daily maximum temperature
        temp_min_next_day (float): [°C] daily minimum temperature next day
        temp_0bc (float): [°C] Base temperature
        temp_mbc (float): [°C] Maximum effective temperature

    Returns:
        (float): the daily action temperature
    """
    a_c = 0.
    for h in range(24):
        if h < 12:
            temp_h = temp_min + h * (temp_max - temp_min) / 12
        else:
            temp_h = temp_max - (h - 12) * (temp_max - temp_min_next_day) / 12

        if temp_h < temp_0bc:
            temp_h_eff = 0.
        elif temp_h < temp_mbc:
            temp_h_eff = temp_h - temp_0bc
        else:
            temp_h_eff = temp_mbc - temp_0bc

        a_c += temp_h_eff

    return a_c
