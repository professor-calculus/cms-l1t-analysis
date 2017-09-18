from importlib import import_module
import os


def exists(module_name):
    try:
        import_module(module_name)
    except ImportError:
        if '.' not in module_name:
            return False
        # check if it is a member of a module instead
        tokens = module_name.split('.')
        module_name = '.'.join(tokens[:-1])
        try:
            m = import_module(module_name)
        except ImportError:
            return False
        return hasattr(m, tokens[-1])
    else:
        return True


def load_L1TNTupleLibrary(lib_name='L1TAnalysisDataformats.so'):
    import ROOT
    PROJECT_ROOT = os.environ.get('PROJECT_ROOT', os.getcwd())
    if lib_name not in ROOT.gSystem.GetLibraries():
        path_to_lib = os.path.join(PROJECT_ROOT, 'build', lib_name)
        ROOT.gSystem.Load(path_to_lib)
        assert (lib_name in ROOT.gSystem.GetLibraries())
