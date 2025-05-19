import logging
from pypickle.pypickle import (
    save,
    load,
    clean,
    check_logger,
    validate_modules,
    get_risk_modules,
    get_critical_paths,
    is_critical_path,
    get_allowed_paths,
    )

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '2.0.1'

# Setup root logger
_logger = logging.getLogger('pypickle')
_log_handler = logging.StreamHandler()
_fmt = '[{asctime}] [{name}] [{levelname}] {msg}'
_formatter = logging.Formatter(fmt=_fmt, style='{', datefmt='%d-%m-%Y %H:%M:%S')
_log_handler.setFormatter(_formatter)
_log_handler.setLevel(logging.DEBUG)
_logger.addHandler(_log_handler)
_logger.propagate = False

# module level doc-string
__doc__ = """
pypickle
=====================================================================

Description
-----------
pypickle is for saving and loading files in pickle format.

Example
-------
>>> import pypickle
>>> filepath = 'test.pkl'
>>> data = [1,2,3,4,5]
>>> status = pypickle.save(filepath, data)
>>> # Load file
>>> data = pypickle.load(filepath)
>>> #
>>> # Clean the filename before saving to disk.
>>> filename = 't$st/.pkl'
>>> filename = pypickle.clean(filename)

References
----------
https://github.com/erdogant/pypickle

"""
