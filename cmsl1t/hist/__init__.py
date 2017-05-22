from exceptions import NotImplementedError


class BaseHistogram(object):
    def __init__(self, name, title):
        self.name = name
        self.title = title
        self.n_dimensions = None

    def set_n_axes(dims):
        self.n_axes = dims

    def fill(self, *vargs):
        raise NotImplementedError()
