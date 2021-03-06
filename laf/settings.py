import os
import configparser
from .timestamp import Timestamp

NAME = 'LAF-Fabric'
VERSION = '4.5.1'
APIREF = 'http://laf-fabric.readthedocs.org/en/latest/texts/API-reference.html'
FEATDOC = 'http://shebanq-doc.readthedocs.org/en/latest/texts/welcome.html'
MAIN_CFG = 'laf-fabric.cfg'
DEFAULT_DATA_DIR = 'laf-fabric-data'

class Settings(object):
    '''Manage the configuration.

    The directory structure is built as a set of names in an environment dictionary. 
    The method ``setenv`` builds a new structure based on user choices.
    Local settings can be passed as arguments to object creation, or in a config file in the current directory,
    or in a config file in the user's home directory.
    It is possible to save these settings in the latter config file.
    '''
    _myconfig = {
        'data_dir': None,                  # data directory (possibly containing compiled laf)
        'output_dir': None,                # output directory (containing task results)
        'm_source_dir': None,              # directory containing original, uncompiled laf resource
        'm_source_subdir': 'laf',          # subdirectory of main laf resource
        'a_source_subdir': 'annotations',  # subdirectory of annotation add-ons
        'bin_subdir': 'bin',               # subdirectory of compiled data
        'bin_ext': 'bin',                  # file extension for binary files
        'text_ext': 'txt',                 # file extension for text files
        'log_name': '__log__',             # base name for log files
        'compile_name': 'compile__',       # extension name for log files of compile process
        'primary_data': 'primary_data',    # name of the primary data file in the compiled data
        'empty': '--',                     # name of empty annox
        'header': '_header_.xml',          # name of laf header file in annox
    }
    _env_def = {
        'source':                '{source}',
        'annox':                 '{annox}',
        'task':                  '{task}',
        'zspace':                '{zspace}',
        'empty':                 '{empty}',
        'data_dir':              '{data_dir}',
        'output_dir':            '{output_dir}',
        'source_data':           '{data_dir}/{source}/mql/{source}',
        'bin_dir':               '{data_dir}/{source}/{bin_subdir}',
        'm_source_dir':          '{m_source_dir}/{source}/{m_source_subdir}',
        'm_source_path':         '{m_source_dir}/{source}/{m_source_subdir}/{source}.txt.hdr',
        'a_source_dir':          '{m_source_dir}/{source}/{a_source_subdir}/{annox}',
        'a_source_path':         '{m_source_dir}/{source}/{a_source_subdir}/{annox}/{header}',
        'compiled_file':         '{log_name}{compile_name}.{text_ext}',
        'm_compiled_dir':        '{data_dir}/{source}/{bin_subdir}',
        'm_compiled_path':       '{data_dir}/{source}/{bin_subdir}/{log_name}{compile_name}.{text_ext}',
        'primary_compiled_path': '{data_dir}/{source}/{bin_subdir}/{primary_data}',
        'a_compiled_dir':        '{data_dir}/{source}/{bin_subdir}/A/{annox}',
        'a_compiled_path':       '{data_dir}/{source}/{bin_subdir}/A/{annox}/{log_name}{compile_name}.{text_ext}',
        'z_compiled_dir':        '{data_dir}/{source}/{bin_subdir}/Z/{zspace}',
        'task_dir':              '{output_dir}/{source}/{task}',
        'log_path':              '{output_dir}/{source}/{task}/{log_name}{task}.{text_ext}',
    }

    def __init__(self, data_dir, laf_dir, output_dir, save, verbose):
        stamp = Timestamp(verbose=verbose)
        self.stamp = stamp
        stamp.Nmsg('This is {} {}\nAPI reference: {}\nFeature doc: {}\n'.format(NAME, VERSION, APIREF, FEATDOC))
        strings = configparser.ConfigParser(inline_comment_prefixes=('#'))
        cw_dir = os.getcwd()
        home_dir = os.path.expanduser('~')
        global_config_dir = "{}/{}".format(home_dir, DEFAULT_DATA_DIR)
        global_config_path = "{}/{}".format(global_config_dir, MAIN_CFG)
        local_config_path = MAIN_CFG
        default_data_dir = global_config_dir
        default_laf_dir = global_config_dir
        config_data_dir = None
        config_laf_dir = None
        config_output_dir = None
        the_config_path = None
        for config_path in (local_config_path, global_config_path):
            if os.path.exists(config_path):
                the_config_path = config_path
                break
        if the_config_path != None:
            with open(the_config_path, "r", encoding="utf-8") as f: strings.read_file(f)
            if 'locations' in strings:
                if 'data_dir' in strings['locations']: config_data_dir = strings['locations']['data_dir']
                if 'laf_dir' in strings['locations']: config_laf_dir = strings['locations']['laf_dir']
                if 'output_dir' in strings['locations']: config_output_dir = strings['locations']['output_dir']
        the_data_dir = data_dir or config_data_dir or default_data_dir
        the_laf_dir = laf_dir or config_laf_dir or the_data_dir
        the_output_dir = output_dir or config_output_dir
        the_data_dir = \
            the_data_dir.replace('.', cw_dir, 1) if the_data_dir.startswith('.') else the_data_dir.replace('~', home_dir, 1) if the_data_dir.startswith('~') else the_data_dir
        the_laf_dir = \
            the_laf_dir.replace('.', cw_dir, 1) if the_laf_dir.startswith('.') else the_laf_dir.replace('~', home_dir, 1) if the_laf_dir.startswith('~') else the_laf_dir
        the_output_dir = \
            the_output_dir.replace('.', cw_dir, 1) if the_output_dir.startswith('.') else the_output_dir.replace('~', home_dir, 1) if the_output_dir.startswith('~') else the_output_dir
        if not os.path.exists(the_data_dir):
            stamp.Imsg("CREATING new DATA_DIR {}".format(the_data_dir))
            try:
                if not os.path.exists(the_data_dir): os.makedirs(the_data_dir)
            except os.error as e:
                raise FabricError("could not create data directory {}".format(the_data_dir), stamp, cause=e)
        if not os.path.exists(the_output_dir):
            stamp.Imsg("CREATING new OUTPUT_DIR {}".format(the_output_dir))
            try:
                if not os.path.exists(the_output_dir): os.makedirs(the_output_dir)
            except os.error as e:
                raise FabricError("could not create output directory {}".format(the_output_dir), stamp, cause=e)
        self._myconfig.update({'data_dir': the_data_dir, 'm_source_dir': the_laf_dir, 'output_dir': the_output_dir})
        if save:
            strings['locations'] = {'data_dir': the_data_dir, 'laf_dir': the_laf_dir, 'output_dir': the_output_dir}
            if not os.path.exists(global_config_path):
                stamp.Imsg("CREATING new GLOBAL CONFIG FILE {}".format(global_config_path))
                try:
                    if not os.path.exists(global_config_dir): os.makedirs(global_config_dir)
                except os.error as e:
                    raise FabricError("could not create global config directory {}".format(global_config_dir), stamp, cause=e)
            with open(global_config_path, "w", encoding="utf-8") as f: strings.write(f)
        self.env = {}
        self.zspace = ''

    def setenv(self, source=None, annox=None, task=None, zspace=None):
        if source == None: source = self.env.get('source')
        if annox == None: annox = self.env.get('annox')
        if task == None: task = self.env.get('task')
        if zspace == None: zspace = self.env.get('zspace')
        for e in self._env_def: self.env[e] = self._env_def[e].format(source=source, annox=annox, task=task, zspace=zspace, **self._myconfig)


