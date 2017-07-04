from rootpy.ROOT import gPad


class BasePlotter(object):
    """
    A Base class to be used by the various plotters
    """

    def set_plot_output_cfg(self, outdir, fmt):
        """
        Store the output directory and image formats
        """
        self.output_dir = outdir
        self.output_format = fmt

    def get_output_image(self, name):
        return "{}/{}.{}".format(self.output_dir, name, self.output_format)

    def save_canvas(self, canvas=None, name=None):
        if not canvas:
            canvas = gPad.func()
        if not name:
            name = canvas.GetName()
        out_path = "{}/{}.{}".format(self.output_dir, name, self.output_format)
        canvas.SaveAs(out_path)

    def build(self):
        """
        Create the histograms that this plotter needs.

        This is not done in an init function so that we can by-pass this in the
        case where we reload things from disk
        """
        raise NotImplementedError("build() needs to be implemented")

    def from_root(self, filename):
        """
        Reload histograms from existing files on disk.

        Might be called multiple times, in which case histograms should be
        merged together with existing ones
        """
        raise NotImplementedError("from_root() needs to be implemented")

    def to_root(self, filename):
        """
        Has to be overloaded by users code.

        Write histograms to a root file.
        """
        raise NotImplementedError("to_root() needs to be implemented")

    def fill(self):
        """
        Has to be overloaded by users code.

        Fill the histograms with event data. The actual arguments passed to
        this function is up to the derived code.
        """
        raise NotImplementedError("fill() needs to be implemented")

    def draw(self):
        """
        Has to be overloaded by users code.

        Draw the histograms on a canvas.
        Can produce multiple output plots.
        Use self.save_canvas() to actually save the plot
        """
        raise NotImplementedError("draw() needs to be implemented")
