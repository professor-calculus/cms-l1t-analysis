import numpy as np
from exceptions import RuntimeError
from math import pi, degrees
twopi = 2 * pi


def get_resolution_function(resolution_type):
    if resolution_type.lower() == "energy":
        return resolution_energy
    elif resolution_type.lower() == "phi":
        return resolution_phi
    elif resolution_type.lower() == "eta":
        return resolution_eta
    elif resolution_type.lower() == "position_1d":
        return resolution_position_1D
    elif resolution_type.lower() == "position_2d":
        return resolution_position_2D
    msg = "Cannot find method for requested resolution_type, " + resolution_type
    raise RuntimeError(msg)


def resolution_energy(online, offline):
    return _resolution_div_offline(online, offline)


def resolution_phi(online, offline):
    """
    delta_phi = phi_on - phi_off 
    but then wrap delta_phi, so abs(delta_phi) < pi 
    and make sure the sign implies the same direction (anti-clockwise from on to off is positive)
    """
    delta_phi = _resolution_no_div(online, offline)
    if delta_phi > pi: 
        delta_phi -= twopi
    delta_phi_other = delta_phi % twopi 
    delta_phi_ret = delta_phi if delta_phi_other > pi else delta_phi_other
    return delta_phi_ret


def resolution_eta(online, offline):
    return _resolution_no_div(online, offline)


def resolution_position_1D(online, offline):
    return _resolution_no_div(online, offline)


def resolution_position_2D(online, offline):
    return np.linalg.norm(np.array(online) - np.array(offline))


def _resolution_div_offline(online, offline):
    return (online - offline) / float(offline) if offline != 0 else float("NaN")


def _resolution_div_online(online, offline):
    return (online - offline) / float(online) if online != 0 else float("NaN")


def _resolution_no_div(online, offline):
    return online - offline
