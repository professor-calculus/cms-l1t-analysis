import os


class BaseAnalyzer(object):
    """
    A Base class to be used by the various analyzers
    """
    def __init__(self, name, config, **kwargs):
        self.name = name
        self.output_folder = config.get('output', 'folder')
        self.config = config
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        self.all_plots = []

    def prepare_for_events(self, reader):
        """
        Can be overloaded in the derived class.
        Called once, after the input trees have been prepared.

        returns:
          Should return True if everything was prepared ok.
          If anything else is returned, processing will stop
        """
        return True

    def process_event(self, entry, event):
        """Should not really be overloaded in the derived class"""
        return self.fill_histograms(entry, event)

    def fill_histograms(self, entry, event):
        """
        Has to be overloaded by users code.

        Called once per input event in the tuples.

        parameters:
         - entry -- the index of the entry being read in
         - event -- the event data read in from the tuples

        returns:
          Should return True if histograms were filled without problem.
          If anything else is returned, processing of the trees will stop
        """
        raise NotImplementedError("fill_histograms needs to be implemented")
        return True

    def write_histograms(self):
        """
        Called after all events have been read, so that histograms can be
        written to file).  Note that plots should not be drawn here, since this
        method will not be called if we are running off previously filled
        histograms.

        returns:
          Should return True if histograms were written without problem.
          If anything else is returned, processing of the trees will stop
        """
        for hist in self.all_plots:
            hist.to_root(self.get_histogram_filename())
        return True

    def make_plots(self):
        """
        Called after all events have been read to convert histograms to actual
        plots Might be called on existing files of histograms (ie. without
        reading tuples in again)

        returns:
          Should return True if plots were produced without problem.
          If anything else is returned, processing of the trees will stop
        """
        for plot in self.all_plots:
            plot.draw()
        return True

    def finalize(self):
        """
        Can be overloaded in the derived class if needed.

        Called at the very end of the code to tidy things up before the
        programs quits
        """
        return True

    def get_histogram_filename(self):
        output_file = "{}_histograms.root".format(self.name)
        return os.path.join(self.output_folder, output_file)

    def add_plotter(self, plotter):
        self.all_plots.append(plotter)
