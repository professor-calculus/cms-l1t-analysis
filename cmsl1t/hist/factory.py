from cmsl1t.hist import BaseHistogram
import logging
from importlib import import_module


logger = logging.getLogger(__name__)


def build_hist(self, histogram, name, title, *vargs, **kwargs):
    histograms=[]
    for hist in BaseHistogram.__subclasses__():
        if hist.__name__ == histogram:
            histogram.append(hist)
    try:
        hist = import_module("rootpy.plotting."+histogram)
        if hist:
            histograms.append(hist)
    except ImportError:
        pass
    if len(histograms) == 0:
        msg = "Error: No valid histogram type called: '{0}'"
        logger.error(msg.format(histogram))
        return None
    elif len(histogram) > 1:
        msg = "Error: Multiple histogram types are called: '{0}'"
        logger.error(msg.format(histogram))
        return None

    hist = histograms[0](name, title, *vargs, **kwargs)
    return hist
