from rootpy.io.pickler import dump, load
# no pickles without dill
import dill

def to_root(obj, output_file):
    '''
        Saves the obj into a ROOT file
    '''
    if not output_file.endswith('.root'):
        output_file += '.root'
    dump(obj, output_file)


def from_root(input_file):
    '''
        Loads the obj from a ROOT file
    '''
    return load(input_file, use_proxy=False)
