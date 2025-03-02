"""pypickle is to save and load variables from pickle files.

Name        : pypickle.py
Author      : E.Taskesen
Contact     : erdogant@gmail.com
Github      : https://github.com/erdogant/pypickle
Licence     : See licences

"""

import pickle
import os
import re
import logging

NAME_WIDTH = max(len(__name__), 12)  # Ensuring a minimum width of 12
logger = logging.getLogger('')
[logger.removeHandler(handler) for handler in logger.handlers[:]]
logging.basicConfig(
    format=f"%(asctime)s [%(name)-{NAME_WIDTH}s]> %(levelname)-8s> %(message)s",
    datefmt="%d-%m-%y %H:%M:%S",
    level=logging.INFO)
logger = logging.getLogger(__name__)


# %% Save pickle file
def save(filepath: str, var, overwrite: bool = False, fix_imports: bool = True, verbose: int = 20):
    """Save pickle file for input variables.

    Parameters
    ----------
    filepath : str
        Pathname to store pickle files.
    var : {list, object, dataframe, etc}
        Name of list or dict or anything else that needs to be stored.
    fix_imports : bool, (default=True)
        fix_imports are used for compatibility support for pickle stream generated by Python 2. If fix_imports is true, pickle will try to map the old Python 2 names to the new names used in Python 3.
    overwrite : bool, (default=False)
        Overwite file if exists.
    verbose : int, (default: 20)
        Print progress to screen. The default is 20.
        10:Debug, 20:Info, 30:Warn 40:Error, 60 or 0:Silent

    Returns
    -------
    Status of succes : bool [True,False].

    Example
    -------
    >>> import pypickle
    >>> filepath = './temp/test.pkl'
    >>> data = [1,2,3,4,5]
    >>> status = pypickle.save(filepath, data)

    """
    # Set logger
    set_logger(verbose)
    # Make empty pickle file
    if os.path.isdir(filepath):
        logger.info(f'Filepath {filepath} should be a file with a path and not directory.')
        return False
    if os.path.isfile(filepath) and not overwrite:
        logger.info(f'File already exists and is not overwritten: {filepath}')
        return False

    outfile = open(filepath, 'wb')
    # Write and close
    pickle.dump(var, outfile)
    outfile.close()

    if os.path.isfile(filepath):
        logger.info(f'Pickle file saved: {filepath}')
        out=True
    else:
        logger.info('Pickle file could not be saved: {filepath}')
    return out


# %% Load pickle file
def load(filepath: str, fix_imports: bool = True, encoding: str = "ASCII", errors: str = "strict", verbose: int = 3):
    """Load pickle files for input variables.

    Parameters
    ----------
    filepath : str
        Pathname to store pickle files.
    fix_imports : bool, (default=True)
        fix_imports are used for compatibility support for pickle stream generated by Python 2. If fix_imports is true, pickle will try to map the old Python 2 names to the new names used in Python 3.
    encoding : str, (default: "ASCII")
        encoding tell pickle how to decode 8-bit string instances pickled by Python 2.
        The encoding can be "bytes" to read these 8-bit string instances as bytes objects. Using encoding="latin1" is required for unpickling NumPy arrays and instances of datetime, date and time pickled by Python 2.
    errors : str, (default: "strict")
        errors tell pickle how to decode 8-bit string instances pickled by Python 2.
    verbose : int, optional
        Show message. A higher number gives more informatie. The default is 3.

    Returns
    -------
    Status of succes : bool [True,False].

    Example
    -------
    >>> import pypickle
    >>> filepath = 'test.pkl'
    >>> data = [1,2,3,4,5]
    >>> status = pypickle.save(filepath, data)
    >>> # Load file
    >>> data = pypickle.load(filepath)


    """
    out = None
    if os.path.isfile(filepath):
        logger.info('[pypickle] Pickle file loaded: {filepath}')
        pickle_off = open(filepath, "rb")
        out = pickle.load(pickle_off, fix_imports=fix_imports, encoding=encoding, errors=errors)
    else:
        logger.info('[pypickle] Pickle file does not exists: {filepath}')
    return out


# %% Clean filename
def clean(filename: str) -> str:
    """Clean the filename to make sure the file can be saved on disk.

    Description
    -----------
    The following characters are replaced from the filename: '&', ',', '?', '$', '!' '/', '\' with character: '_'

    Parameters
    ----------
    filename : str
        Filename.

    Returns
    -------
    TYPE: str
        filename

    Example
    -------
    >>> import pypickle
    >>> filename = 't/st.pkl'
    >>> data = [1,2,3,4,5]
    >>> filename = pypickle.clean(filename)
    >>> # Save
    >>> status = pypickle.save(filename, data)
    >>> # Load file
    >>> data = pypickle.load(filepath)

    """
    return re.sub(r'[|&|,|?|$|!|/|\\]', r'_', filename)


# %%
def check_logger(verbose: [str, int] = 'info'):
    """Check the logger."""
    set_logger(verbose)
    logger.debug('DEBUG')
    logger.info('INFO')
    logger.warning('WARNING')
    logger.critical('CRITICAL')


# %%
def get_logger():
    """Return logger status."""
    return logger.getEffectiveLevel()


# %%
def set_logger(verbose: [str, int] = 'info'):
    """Set the logger for verbosity messages.

    Parameters
    ----------
    verbose : [str, int], default is 'info' or 20
        Set the verbose messages using string or integer values.
        * [0, 60, None, 'silent', 'off', 'no']: No message.
        * [10, 'debug']: Messages from debug level and higher.
        * [20, 'info']: Messages from info level and higher.
        * [30, 'warning']: Messages from warning level and higher.
        * [50, 'critical']: Messages from critical level and higher.

    Returns
    -------
    None.

    > # Set the logger to warning
    > set_logger(verbose='warning')
    > # Test with different messages
    > logger.debug("Hello debug")
    > logger.info("Hello info")
    > logger.warning("Hello warning")
    > logger.critical("Hello critical")

    """
    # Convert old verbose to new
    verbose = convert_verbose_to_new(verbose)
    # Set 0 and None as no messages.
    if (verbose==0) or (verbose is None):
        verbose=60
    # Convert str to levels
    if isinstance(verbose, str):
        levels = {'silent': 60,
                  'off': 60,
                  'no': 60,
                  'debug': 10,
                  'info': 20,
                  'warning': 30,
                  'error': 50,
                  'critical': 50}
        verbose = levels[verbose]

    # Show examples
    logger.setLevel(verbose)


# %%
def convert_verbose_to_new(verbose):
    """Convert old verbosity to the new."""
    # In case the new verbosity is used, convert to the old one.
    if verbose is None: verbose=0
    if not isinstance(verbose, str) and verbose < 10:
        status_map = {
            'None': 'silent',
            0: 'silent',
            6: 'silent',
            1: 'critical',
            2: 'warning',
            3: 'info',
            4: 'debug',
            5: 'debug'}
        if verbose>=2: print('[pypickle]> WARNING use the standardized verbose status. The status [1-6] will be deprecated in future versions.')
        return status_map.get(verbose, 0)
    else:
        return verbose
