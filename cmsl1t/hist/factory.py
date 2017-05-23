from cmsl1t.hist import BaseHistogram
import logging
import rootpy.plotting.hist as rootpy_hists


logger = logging.getLogger(__name__)


def build_hist(hist_type, *vargs, **kwargs):
    histograms = []
    for hist in BaseHistogram.__subclasses__():
        if hist.__name__ == hist_type:
            histograms.append(hist)
    if hasattr(rootpy_hists, hist_type):
        histograms.append(getattr(rootpy_hists, hist_type))
    if len(histograms) == 0:
        msg = "Error: No valid histogram type called: '{0}'"
        logger.error(msg.format(hist_type))
        return None
    elif len(histograms) > 1:
        msg = "Error: Multiple histogram types are called: '{0}'"
        logger.error(msg.format(hist_type))
        return None

    hist = histograms[0](*vargs, **kwargs)
    return hist
