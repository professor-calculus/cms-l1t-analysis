from __future__ import print_function
import yaml
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
TODAY = datetime.now().timetuple()


def get_unique_out_dir(outdir=None, revision=1):
    full_outdir = outdir + "-rev_{rev}".format(rev=revision)
    if os.path.isdir(full_outdir):
        return get_unique_out_dir(outdir, revision + 1)
    return full_outdir


def resolve_file_paths(paths):
    from cmsl1t.utils.root_glob import glob
    all_files = []
    for p in paths:
        all_files.extend(glob(p))
    return all_files


class ConfigParser(object):
    SECTIONS = ['general', 'input', 'analysis', 'output']

    def __init__(self):
        self.config = {}
        self.config_errors = []

    def read(self, input_file):
        cfg = yaml.load(input_file)
        self._read_config(cfg)

    def _read_config(self, cfg):
        cfg['general'] = dict(version=cfg['version'], name=cfg['name'])
        del cfg['version'], cfg['name']

        input_files = cfg['input']['files']
        input_files = resolve_file_paths(input_files)
        cfg['input']['files'] = input_files
        self.config = cfg
        self.__fill_output_template()

        if not self.is_valid():
            msg = '\n'.join(self.config_errors)
            logger.exception(msg)
            raise IOError(msg)

    def sections(self):
        return self.config.keys()

    def options(self, section):
        return self.config[section].keys()

    def get(self, section, option):
        return self.config[section][option]

    def is_valid(self):
        results = [self.validate_sections()]
        results += [self.validate_input_files()]
        return all(results)

    def validate_sections(self):
        expectedSections = sorted(ConfigParser.SECTIONS)
        sections = sorted(self.config.keys())
        hasValidSections = expectedSections == sections
        if hasValidSections is not True:
            msg = 'Configuration has missing or invalid sections.\n'
            msg += self.__section_format(self.__compare_sections(expectedSections, sections))
            self.config_errors += [msg]
        return hasValidSections

    def __section_format(self, sections):
        section_template = ['  - {}' for _ in sections]
        section_template = '\n'.join(section_template)
        return section_template.format(*sections)

    def __compare_sections(self, expected, current):
        expected = set(expected)
        current = set(current)
        missing = expected.difference(current)
        invalid = current.difference(expected)
        decorated_sections = []
        for e in expected:
            if e in missing:
                decorated_sections.append(e + ' (missing)')
            else:
                decorated_sections.append(e)
        for i in invalid:
            decorated_sections.append(i + ' (invalid)')
        return sorted(decorated_sections)

    def validate_input_files(self):
        input_files = self.config['input']['files']
        if not input_files:
            msg = "Could not find any existing files.\n"
            msg += "Given files:\n"
            msg += '\n'.join(self.config['input']['files'])
            self.config_errors += [msg]
        return input_files != []

    def __repr__(self):
        return self.config.__repr__()

    def __fill_output_template(self):
        cfg = self.config
        template = os.path.join(*cfg['output']['template'])

        date = '{y}{m:02d}{d:02d}'.format(
            y=TODAY.tm_year, m=TODAY.tm_mon, d=TODAY.tm_mday)
        sample_name = cfg['input']['sample']['name']
        trigger_name = cfg['input']['trigger']['name']
        run_number = cfg['input']['run_number']

        ouput_folder = template.format(
            date=date, sample_name=sample_name, trigger_name=trigger_name,
            run_number=run_number)
        cfg['output']['folder'] = get_unique_out_dir(ouput_folder)


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config/demo.yaml')
    print(config)
    print()
    print('Sections', config.sections())
    for section in config.sections():
        print('Section', section, 'has options', config.options(section))
        for option in config.options(section):
            print('>> {} = {}'.format(option, config.get(section, option)))
    print()
    print(config.is_valid())
