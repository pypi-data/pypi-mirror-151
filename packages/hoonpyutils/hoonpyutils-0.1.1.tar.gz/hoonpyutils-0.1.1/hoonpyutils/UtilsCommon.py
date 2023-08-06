#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Merged to golden code at 2018.10.11 by Hoon.
"""
import os
import sys
import logging
import configparser
from logging import handlers as log_handlers
import datetime
import unicodedata
import glob
import json
import csv
import shutil
import traceback

try:
    # noinspection PyUnresolvedReferences
    import numpy as np
except Exception as e:
    print(" @ Warning: numpy import error in UtilsCommon - " + str(e))
try:
    # noinspection PyUnresolvedReferences
    from tqdm import tqdm
except Exception as e:
    print(" @ Warning: tqdm import error in UtilsCommon - " + str(e))

'''
try:
    if sys.platform == 'darwin':
       """
        import matplotlib
        matplotlib.use('TkAgg')
except all as e:
    print(e)
try:
    if sys.platform == 'darwin':
        import tkinter
        root = tkinter.Tk()
        screen_width  = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        """
       screen_width = 1440
       screen_height = 900
    else:
        from screeninfo import get_monitors
        screen_width  = get_monitors()[0].width
        screen_height = get_monitors()[0].height
    screen_width = 1920 if screen_width > 1920 else screen_width
except Exception as e:
    print('exception for screen info : {}'.format(e))
    screen_width = 1920
    screen_height = 1080
    print(" @ Warning in getting screen width and height...\n")
'''

if sys.platform == 'darwin':
    screen_width = 1440
    screen_height = 900
else:
    screen_width = 1920
    screen_height = 1080

_this_folder_ = os.path.dirname(os.path.abspath(__file__))

IMG_EXTENSIONS = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tif', 'tiff']
VIDEO_EXTENSIONS = ['mp4', 'avi', 'mkv']
AUDIO_EXTENSIONS = ['mp3']
META_EXTENSION = ['meta', 'json']
DEV_NULL = open(os.devnull, 'w')
HANGUL_FONT = os.path.join(_this_folder_, "./Fonts/SourceHanSerifK-Regular.otf")


class LoggerWrapper:

    def info(self): pass

    def error(self): pass


def get_stdout_logger(logger=None):
    if logger is None:
        logger = LoggerWrapper()
        logger.info = print
        logger.error = print
    return logger


def get_ini_parameters(ini_fname, cmt_delimiter="###", exit_=False):
    ini = configparser.ConfigParser()
    if not os.path.isfile(ini_fname):
        if exit_:
            print(" @ Error: file not found, {}, in get_ini_parameters method.".format(ini_fname))
            sys.exit(1)
        else:
            print(" % Warning: file not found, {}, in get_ini_parameters method.".format(ini_fname))
            return None
    ini.read(ini_fname, encoding='utf-8')
    return remove_comments_in_ini(ini, cmt_delimiter=cmt_delimiter)


def is_string_nothing(string):
    if string == '' or string is None:
        return True
    else:
        return False


def is_json(my_json):
    try:
        json.loads(my_json)
        return True
    except ValueError:
        return False


def get_datetime(fmt="%Y-%m-%d-%H-%M-%S"):
    """ Get datetime with format argument.
    :param fmt:
    :return:
    """
    return datetime.datetime.now().strftime(fmt)


def setup_logger(logger_name,
                 log_prefix_name,
                 level=logging.INFO,
                 folder='.',
                 filename=None,
                 backup_count=0,
                 logger_=True,
                 stdout_=True):
    """ Setup logger supporting two handlers of stdout and file.
    :param logger_name:
    :param log_prefix_name:
    :param level:
    :param folder:
    :param filename:
    :param backup_count:
    :param logger_:
    :param stdout_:
    :return:
    """

    if not logger_:
        logger = LoggerWrapper()
        logger.info = print
        logger.error = print
        return logger

    if not os.path.exists(folder):
        os.makedirs(folder)

    # dt = get_datetime()[:-2].replace(":","-")
    dt = get_datetime().replace(":", "-")
    log_file = os.path.join(*folder.split('/'), log_prefix_name + dt + '.log') if filename is None else filename
    log_setup = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(name)-10s | %(asctime)s.%(msecs)03d | %(levelname)-7s | %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    # log 파일이 무한정 커지는 것을 방지하고, 서버 시작후 부터 일자별로 최대 backup_count(기본=0) 일까지 저장하도록 한다.
    if backup_count > 0:
        file_handler = log_handlers.TimedRotatingFileHandler(log_file,
                                                             backupCount=backup_count,
                                                             when='midnight')
    else:
        file_handler = logging.FileHandler(log_file, mode='a')

    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y%m%d.bak"
    stream_handler = None
    if stdout_:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
    log_setup.setLevel(level)
    log_setup.addHandler(file_handler)
    if stdout_ and stream_handler:
        log_setup.addHandler(stream_handler)
    return logging.getLogger(logger_name)


def setup_logger_with_ini(ini, logging_=True, stdout_=True):
    if logging_ is True:
        backup_count = 0
        if 'backup_count' in ini:
            backup_count = int(ini['backup_count'])

        logger = setup_logger(ini['name'],
                              ini['prefix'],
                              folder=ini['folder'],
                              filename=None,  # 'test.log',
                              backup_count=backup_count,
                              logger_=logging_,
                              stdout_=stdout_)
        return logger
    else:
        return get_stdout_logger()


def config_logger(logger_ini, logging_, stdout_):
    if logging_ is True:
        return setup_logger_with_ini(logger_ini, logging_=logging_, stdout_=stdout_)
    else:
        return get_stdout_logger()


def check_directory_existence(in_dir, exit_=False, create_=False, print_=True):
    """
    Check if a directory exists or not. If not, create it according to input argument.

    :param in_dir:
    :param exit_:
    :param create_:
    :param print_:
    :return:
    """
    if os.path.isdir(in_dir):
        return True
    else:
        if create_:
            try:
                os.makedirs(in_dir)
            except all:
                print(" @ Error: make_dirs in check_directory_existence routine...\n")
                sys.exit()
        else:
            if print_:
                print("\n @ Warning: directory not found, {}.\n".format(in_dir))
            if exit_:
                sys.exit()
        return False


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def make_dir(folder, remove_=True):
    if os.path.exists(folder):
        if remove_:
            shutil.rmtree(folder)
            os.makedirs(folder)
    else:
        os.makedirs(folder)


def check_file_existence(fname, print_=False, exit_=False, logger=get_stdout_logger()):
    """
    Check if a file exists or not.

    :param fname:
    :param print_:
    :param exit_:
    :param logger:
    :return True/False:
    """
    if not os.path.isfile(fname):
        if print_ or exit_:
            # noinspection PyArgumentList
            logger.error("\n @ Warning: file not found, {}.\n".format(fname))
        if exit_:
            sys.exit()
        return False
    else:
        return True


def check_file_extensions(filename, extensions, print_=False, exit_=False):
    """
    Check if a file exists or not.

    :param filename:
    :param extensions:
    :param print_:
    :param exit_:
    :return True/False:
    """
    file_ext = os.path.splitext(filename)[1][1:]
    if file_ext not in extensions:
        if exit_:
            print("\n @ Error: file, {}, is not in {}.\n".format(filename, ', '.join(extensions)))
            sys.exit(1)
        if print_:
            print("\n ! Warning: file, {}, is not in {}.".format(filename, ', '.join(extensions)))
        return False
    else:
        return True


def get_filenames_in_a_directory(dir_name):
    """
    Get names of all the files in a directory.

    :param dir_name:
    :return out_filenames:
    """
    filenames = os.listdir(dir_name)
    out_filenames = []
    for filename in filenames:
        if os.path.isfile(os.path.join(dir_name, filename)):
            out_filenames.append(filename)

    return out_filenames


def transpose_list(in_list):
    """
    Transpose a 2D list variable.

    :param in_list:
    :return:
    """
    try:
        len(in_list[0])
        return list(map(list, zip(*in_list)))
    except TypeError:
        return in_list


def check_string_in_class(class_name, sub_string):
    for attr in dir(class_name):
        if sub_string in attr:
            print(attr)


def get_filenames(dir_path, prefixes=('',), extensions=('',), recursive_=True, print_=True, exit_=False):
    """
    Find all the files starting with prefixes or ending with extensions in the directory path.
    ${dir_path} argument can accept file.

    :param dir_path:
    :param prefixes:
    :param extensions:
    :param recursive_:
    :param print_:
    :param exit_:
    :return:
    """
    if os.path.isfile(dir_path):
        if os.path.splitext(dir_path)[1][1:] in extensions:
            return [dir_path]
        else:
            return []

    filenames = glob.glob(dir_path + '/**', recursive=recursive_)
    for i in range(len(filenames) - 1, -1, -1):
        # print(i)
        basename = os.path.basename(filenames[i])
        if not (os.path.isfile(filenames[i]) and
                basename.startswith(tuple(prefixes)) and
                basename.endswith(tuple(extensions))):
            del filenames[i]

    if len(filenames) == 0:
        if print_:
            print(" @ Error: no file detected in {}".format(dir_path))
        if exit_:
            sys.exit(1)

    return filenames


def check_box_boundary(box, sz):
    box[0] = 0 if box[0] < 0 else box[0]
    box[1] = 0 if box[1] < 0 else box[1]
    box[2] = sz[0] if box[2] > sz[0] else box[2]
    box[3] = sz[1] if box[3] > sz[1] else box[3]
    return box


def get_bool_from_ini(ini_param):
    """
    Get boolean value from M$ INI style configuration.

    :param ini_param:
    :return: True, False, or None.
    """
    if not isinstance(ini_param, str):
        return None
    if ini_param.lower() in ['0', 'off', 'false']:
        return False
    elif ini_param.lower() in ['1', 'on', 'true']:
        return True
    else:
        return None


def remove_comments_in_ini_section(ini_section, cmt_string='###'):
    """
    Remove comments in ini section
    where comment is the sentence starting the special string combination such as '###'

    :param ini_section:
    :param cmt_string:
    :return:
    """
    ini_out = ini_section
    for key in ini_section:
        ini_out[key] = ini_section[key].split(cmt_string)[0]
    return ini_out


def remove_comments_in_ini(ini, cmt_delimiter='###'):
    """
    Remove comments in ini file,
    where comment is text strings starting with comment delimiter.

    :param ini:
    :param cmt_delimiter:
    :return:
    """
    for section in ini.sections():
        for key in ini[section]:
            ini[section][key] = ini[section][key].split(cmt_delimiter)[0].strip()
    return ini


def split_fname(fname):
    """
    Split the filename into folder, core name, and extension.

    :param fname:
    :return:
    """
    abs_fname = os.path.abspath(fname)
    folder = os.path.dirname(abs_fname)
    base_fname = os.path.basename(abs_fname)
    split = os.path.splitext(base_fname)
    core_fname = split[0]
    ext = split[1]
    return folder, core_fname, ext


def copy_folder_structure(src_path, tar_path):
    dir_names = glob.glob(src_path + '/*/', recursive=True)
    for dir_name in dir_names:
        # tar_name = os.path.join(tar_path, dir_name[len(src_path):])
        tar_name = dir_name.replace(src_path, tar_path)
        # print(tar_name)
        if not os.path.isdir(tar_name):
            os.mkdir(tar_name)
    return True


def to_dict(obj):
    if not hasattr(obj, "__dict__"):
        return obj
    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue
        element = []
        if isinstance(val, list):
            for item in val:
                element.append(to_dict(item))
        else:
            element = to_dict(val)
        result[key] = element
    return result


class JsonConvert(object):
    mappings = {}

    @classmethod
    def class_mapper(cls, d):
        for keys, cl in cls.mappings.items():
            if keys.issuperset(d.keys()):  # are all required arguments present?
                return cl(**d)
        else:
            # Raise exception instead of silently returning None
            raise ValueError('Unable to find a matching class for object: {!s}'.format(d))

    @classmethod
    def complex_handler(cls, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))

    @classmethod
    def register(cls, in_class):
        cls.mappings[frozenset(tuple([attr for attr, val in cls().__dict__.items()]))] = in_class
        return cls

    @classmethod
    def to_json(cls, obj):
        return json.dumps(obj.__dict__, default=cls.complex_handler, indent=4)

    @classmethod
    def from_json(cls, json_str):
        return json.loads(json_str, object_hook=cls.class_mapper)

    @classmethod
    def to_file(cls, obj, path):
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines([cls.to_json(obj)])
        return path

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'r') as f:
            result = cls.from_json(f.read())
        return result


# noinspection PyPep8Naming
def Float(x, digit=3):
    return int(x * pow(10, digit)) / pow(10, digit)


def read_csv_file(csv_file, delimiter=','):
    """ Read csv file

    :param csv_file:
    :param delimiter:
    :return:
    """
    mtx = []
    with open(csv_file, "r", encoding='utf8') as f:
        for row in csv.reader(f, delimiter=delimiter):
            row = [x.strip() for x in row]
            mtx.append(row)
    return mtx


def get_dict_from_csv_file(csv_file, delimiter=',', int_key_=False, exit_=False):
    """ Get dict from csv file

    :param csv_file:
    :param delimiter:
    :param int_key_:
    :param exit_:
    :return:
    """
    _dict = {}
    if os.path.isfile(csv_file):
        with open(csv_file, "r", encoding='utf8') as f:
            for row in csv.reader(f, delimiter=delimiter):
                key = int(row[0]) if int_key_ else row[0]
                _dict[key] = row[1].strip()
    else:
        print(f" @ ERROR: file not found in get_dict_from_csv_file, {csv_file}")
        if exit_:
            sys.exit(1)
    return _dict


def write_list_to_csv(dataset, filename):
    if filename:
        with open(filename, 'w') as f:
            for row_dat in dataset:
                f.write(','.join([str(x) for x in row_dat]) + '\n')
    pass


def print_and_write(msg, console=True, filename=''):
    if console:
        print(msg)
    if filename:
        with open(filename, 'a') as fid:
            fid.write(msg)
    pass


def to_str(string_dat):
    if isinstance(string_dat, str):
        string_dat = string_dat.encode('utf-8')
    return string_dat


def to_unicode(unicode_dat):
    if isinstance(unicode_dat, str):
        # noinspection PyUnresolvedReferences
        unicode_dat = unicode_dat.decode('utf-8')
    return unicode_dat


def unicode_normalize(string):
    return string if string is None else unicodedata.normalize('NFC', string)


def split_path(path, max_depth=20):
    (head, tail) = os.path.split(path)
    return split_path(head, max_depth - 1) + [tail] \
        if max_depth and head and head != path \
        else [head or tail]


def normalize_box(box, w, h):
    ww = float(w)
    hh = float(h)
    shape = np.array(box).shape
    if shape[0] == (1, 4):
        out = [box[0] / ww, box[1] / hh, box[2] / ww, box[3] / hh]
    elif shape == (1, 8):
        out = [box[0] / ww, box[1] / hh, box[2] / ww, box[3] / hh,
               box[4] / ww, box[5] / hh, box[6] / ww, box[7] / hh]
    elif shape[0] == 2:
        out = [[p[0] / ww, p[1] / hh] for p in box]
    else:
        print(" @ Error: box shape is not defined, {}.".format(str(shape)))
        out = box

    if isinstance(box, np.ndarray):
        return np.array(out)
    else:
        return out


class ToObj:
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [ToObj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, ToObj(b) if isinstance(b, dict) else b)


def trunc(val, ref):
    return int(val / ref) * ref


def abs_norm_path(path):
    return os.path.normpath(os.path.abspath(path))


def make_new_folder(folder, force_=True):
    if os.path.isdir(folder):
        if force_:
            shutil.rmtree(folder, ignore_errors=True)
            os.makedirs(folder)
    else:
        os.makedirs(folder)


def get_leaf_folders(root_folder, tqdm_=False):
    leaf_folders = []
    if tqdm_:
        for root, dirs, files in tqdm(os.walk(root_folder)):
            if not dirs:
                leaf_folders.append(root)
    else:
        for root, dirs, files in os.walk(root_folder):
            if not dirs:
                leaf_folders.append(root)

    return leaf_folders


def make_dir_from_fname(fname):
    folder = os.path.dirname(os.path.abspath(fname))
    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)


check_file = check_file_existence
isfile = check_file_existence
check_folder = check_directory_existence


def get_time_diff(time_arr):
    text = ''
    for i in range(len(time_arr) - 1):
        text += f"{time_arr[i + 1] - time_arr[i]:.3f} | "

    return text


def get_key_from_value(_dict, val):
    try:
        return list(_dict.keys())[list(_dict.values()).index(val)]
    except Exception as _e:
        print(traceback.format_exc() + str(_e))
        return None


def concatenate_values_with_same_keys_in_dicts(dict_list):
    res = dict()
    for _dict in dict_list:
        for _key in _dict:
            if _key in res:
                res[_key] += (_dict[_key])
            else:
                res[_key] = _dict[_key]
    return res


def pause():
    return input("Press the <ENTER> key to continue...")
