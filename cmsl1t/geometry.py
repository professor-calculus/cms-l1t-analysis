import logging

logger = logging.getLogger(__name__)


# detector regions in eta
eta_regions = {
    # barrel
    'B': lambda x: abs(x) < 1.479,
    # endcap
    'E': lambda x: abs(x) >= 1.479 and abs(x) <= 3.0,
    # barrel or endcap
    'BE': lambda x: abs(x) <= 3.0,
    # hadron forward
    'HF': lambda x: abs(x) > 3.0,
}

# could add aliases


def is_in_region(region, eta, regions=eta_regions):
    if region not in regions:
        msg = 'Unknown detector region {0}'.format(region)
        logger.error(msg)
        raise KeyError(msg)

    return regions[region](eta)
