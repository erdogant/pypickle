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
from typing import Union
import pickletools
import tempfile

logger = logging.getLogger(__name__)

#%%
def get_risk_modules():
    """Risk modules.
    These modules can be used for code execution, filesystem manipulation, networking, or loading arbitrary code.

    Returns
    -------
    risky_modules : dict

    """
    risk_modules = [
        # Risky modules
        # 'os',               # Shell access, file system, environment manipulation
        'os.system',        # Execute shell commands
        'os.popen',         # Open pipe to or from command
        'os.execve',        # Execute a new program, replacing the current process
        'os.remove',        # Remove files (can delete data)
        'os.rmdir',         # Remove directories
        'os.makedirs',      # Make directories (can modify filesystem)
        'subprocess',       # Arbitrary system command execution
        'subprocess.Popen', # Start subprocess with pipe access
        'subprocess.call',  # Run system commands
        # 'sys',            # System-level operations
        'sys.exit',         # Exit interpreter
        'sys.modules',      # Manipulate loaded modules
        'sys.path',         # Modify import path (can load arbitrary code)

        # OS/platform-specific modules
        'nt',               # Windows native system calls (like os)
        'posix',            # Unix equivalent of nt

        # Other risky modules
        'importlib',        # Dynamic imports and module loading
        'socket',           # Network access, can open sockets
        'selectors',        # Low-level network/socket multiplexing
        'multiprocessing',  # Starts subprocesses and parallel processes
        'threading',        # Can spawn threads (potential concurrency hazards)
        'asyncio',          # Asynchronous tasks (can be misused)
        'ctypes',           # Load arbitrary C libraries (very risky)
        'platform',         # Access to detailed system info (potential info leak)
        'webbrowser',       # Can open URLs or trigger external browser actions
        'shutil',           # File operations, including deleting files
        'tempfile',         # Temporary files and directories (file system access)
        'glob',             # Wildcard filesystem access
        'pathlib',          # Filesystem path operations (safe if used carefully, but can be risky)
        'codecs',           # Decoding arbitrary formats (rare but possible exploits)

        # Specific risky functions in builtins (instead of blocking entire builtins module)
        'builtins.eval',        # Execute arbitrary code from string
        'builtins.exec',        # Execute arbitrary code dynamically
        'builtins.open',        # File open (can read/write files)
        'builtins.__import__',  # Dynamic import of modules
    ]

    return risk_modules


def get_critical_paths(custom_path=None):
    """Get critical paths.

    Cross-platform safety: Including all known critical paths is a defensive design.
    his approach makes your security policy more fail-safe and portable. It prevents users from accidentally saving into a sensitive path,
    even if the code is being executed in a cross-platform environment like Docker,  Networked/shared drives,  Remote SSH sessions,  CI pipelines.

    Parameters
    ----------
    custom_path : [str, list], optional
        User defined custom critical path is appended to the existing critical paths.

    Returns
    -------
    CRITICAL_PATHS : list

    """
    CRITICAL_PATHS = [
        # Universal Unix system directories
        "/bin", "/boot", "/dev", "/etc", "/lib", "/lib64",
        "/proc", "/root", "/sbin", "/sys", "/usr", "/var",

        # Sensitive user configuration
        os.path.expanduser("~/.ssh"),
        os.path.expanduser("~/.gnupg"),
        os.path.expanduser("~/.config"),
        os.path.expanduser("~/.local/share"),

        # macOS specific
        "/System",             # System-critical files
        "/Library",            # System-wide libraries
        "/Network",            # Network mounts
        "/private",            # Contains /etc, /var, etc. on macOS
        "/Volumes",            # Mounted disk volumes
        "/Applications",       # Installed apps
        "/usr/local/bin",      # Homebrew & CLI tools

        # Windows specific
        "C:\\Windows", "C:\\Windows\\System32", "C:\\Program Files",
        "C:\\Program Files (x86)", "C:\\ProgramData", "C:\\Recovery",
        os.path.expandvars("%APPDATA%"), os.path.expandvars("%LOCALAPPDATA%")
    ]

    if isinstance(custom_path, str): custom_path = [custom_path]
    if isinstance(custom_path, list):
        CRITICAL_PATHS = CRITICAL_PATHS + custom_path
    # Return
    return CRITICAL_PATHS

def get_allowed_paths(custom_path=None):
    # Define allowed base directories
    ALLOWED_SAVE_PATHS = [
        os.path.abspath(os.getcwd()),           # Current working dir
        os.path.expanduser("~"),                # User's home dir
        tempfile.gettempdir()                   # OS temp dir
    ]

    if isinstance(custom_path, str): custom_path = [custom_path]
    if isinstance(custom_path, list):
        ALLOWED_SAVE_PATHS = ALLOWED_SAVE_PATHS + custom_path
    # Return
    return ALLOWED_SAVE_PATHS

#%%
def is_safe_path(path: str) -> bool:
    """Safely check if path is within allowed base directories, even across drives."""
    # Default save paths
    allowed_dirs = get_allowed_paths()
    abs_path = os.path.abspath(path)

    for base in allowed_dirs:
        try:
            base_path = os.path.abspath(base)
            common = os.path.commonpath([abs_path, base_path])
            if common == base_path:
                return True
        except ValueError:
            # Happens if paths are on different drives on Windows
            continue
    return False


def is_critical_path(filepath: str) -> bool:
    """
    Check if a given filepath points to or is nested inside a critical system path,
    unless it falls under explicitly allowed subpaths.

    Parameters
    ----------
    filepath : str
        The target path to check.
    critical_paths : list or None
        List of system-critical base paths to protect.
    allowed_subpaths : list or None
        List of subpaths that are considered safe even if under a critical path.

    Returns
    -------
    bool
        True if the filepath is within a critical path (and not explicitly allowed).

    Notes
    -----
    - Handles cross-platform path resolution.
    - Allows exceptions for safe subdirectories like temp folders.

    Examples
    --------
    >>> import pypickle
    >>> import os
    >>> pypickle.is_critical_path("C:\\Users\\User\\AppData\\Local\\Temp\\myfile.pkl")
    False
    >>> pypickle.is_critical_path("C:\\Windows\\System32\\config.sys")
    True
    """
    allowed_subpaths = get_allowed_paths()
    # default critical paths
    critical_paths = get_critical_paths()

    if critical_paths is None:
        return False

    abs_path = os.path.abspath(filepath)

    # Skip check if explicitly allowed
    if allowed_subpaths:
        for allowed in allowed_subpaths:
            try:
                allowed_abs = os.path.abspath(allowed)
                if os.path.commonpath([abs_path, allowed_abs]) == allowed_abs:
                    return False
            except ValueError:
                continue

    # Block if under critical
    for crit in critical_paths:
        try:
            crit_path = os.path.abspath(crit)
            if os.path.commonpath([abs_path, crit_path]) == crit_path:
                logger.warning(f'[BLOCKED]: Filepath: [{filepath}] is under critical path: [{crit}]')
                return True
        except ValueError:
            continue

    return False


def is_known_extension(filepath: str, allowed_extensions=None) -> bool:
    """
    Check if the file has an allowed extension.

    Parameters
    ----------
    filepath : str
        The file path to validate.
    allowed_extensions : list or None
        List of allowed file extensions (with dot), e.g., ['.pkl', '.pickle', '.joblib'].
        If None, defaults to common pickle-related formats.

    Returns
    -------
    bool
        True if the extension is in the allowed list, False otherwise.

    Examples
    --------
    >>> is_known_extension("data.pkl")
    True
    >>> is_known_extension("config.yaml")
    False
    >>> is_known_extension("model.joblib", ['.joblib'])
    True
    """
    if allowed_extensions is None:
        allowed_extensions = ['.pkl', '.pickle', '.pklz', '.pbz2']

    _, ext = os.path.splitext(filepath)
    return ext.lower() in allowed_extensions


# %% Save pickle file
def save(filepath: str,
         var,
         overwrite: bool = False,
         fix_imports: bool = True,
         allow_external: bool = False,
         verbose: str = 'info',
         ):
    """
    Save pickle file for input variables.
    Before saving, there are various security checks:
    * The filepath should be inside the safe paths (user and temp directories). However, this can be overwritten using the allow_external parameter.
    * It is not allowed to save pkl files into (critical) system paths.
    * Extention must be ['.pkl', '.pickle', '.pklz', '.pbz2'] to prevent overwriting other file-types
    * filepaths are checked on traversal

    Security Mechanisms and Purpose
    | Mechanism                       | Purpose                                                       |
    | ------------------------------- | ------------------------------------------------------------- |
    | `allow_external=True`           | Explicit user opt-in to save outside allowed safe directories |
    | System path check               | Prevents saving in critical system paths                      |
    | Extention check                 | Only save with extention: '.pkl', '.pickle', '.pklz', '.pbz2' |
    | Path traversal check            | Prevents directory traversal exploits like `../../etc/passwd` |
    | Audit logs for external saves   | Enables monitoring and traceability of risky saves            |

    Parameters
    ----------
    filepath : str
        Pathname to store pickle file.
    var : object
        Any Python object (list, dict, DataFrame, etc.) to be stored.
    overwrite : bool, optional (default=False)
        Whether to overwrite the file if it already exists.
    fix_imports : bool, optional (default=True)
        Fixes imports for compatibility with Python 2 pickle streams.
    allow_external : bool, optional (default=False)
        Allow saving outside predefined safe directories (explicit opt-in). The safe paths are: user and temp directories.
    verbose : str or int, optional (default='info')
        Logging verbosity level: 'debug', 'info', 'warn', 'error', 'silent'.

    Returns
    -------
    bool
        True if the file was saved successfully, False otherwise.

    Example
    -------
    >>> import pypickle
    >>> import os
    >>> import tempfile
    >>>
    >>> filepath = r'c:/temp/test.pkl'
    >>> data = [1,2,3,4,5]
    >>> status = pypickle.save(filepath, data)
    >>> status = pypickle.save(filepath, data, allow_external=True)
    >>> status = pypickle.save(filepath, data, allow_external=True, overwrite=True)
    >>> #
    >>> filepath = r'c:/temp/test.bat'
    >>> data = [1,2,3,4,5]
    >>> status = pypickle.save(filepath, data)
    >>> #
    >>> filepath = os.path.join(tempfile.gettempdir(), "test.pkl")
    >>> status = pypickle.save(filepath, data)
    >>> status = pypickle.save(filepath, data, overwrite=True)
    >>> #
    >>> filepath = r'd:/repos/test.pkl'
    >>> status = pypickle.save(filepath, data)
    >>> status = pypickle.save(filepath, data, overwrite=True)
    >>> status = pypickle.save(filepath, data, overwrite=True, allow_external=True)
    >>> #
    >>> filepath = r'C://test.pkl'
    >>> data = [1,2,3,4,5]
    >>> status = pypickle.save(filepath, data)
    >>> status = pypickle.save(filepath, data, allow_external=True, overwrite=True)
    >>> #
    >>> filepath = "C:\\Users\\User\\AppData\\Local\\Temp\\myfile.pkl"
    >>> data = [1,2,3,4,5]
    >>> status = pypickle.save(filepath, data)
    >>> status = pypickle.save(filepath, data, allow_external=True)

    """
    # Set logger
    set_logger(verbose)

    if not is_known_extension(filepath):
        logger.warning(f"[BLOCKED]: Extention must be of type ['.pkl', '.pickle', '.pklz', '.pbz2']: [{filepath}] is not allowed.")
        return False

    if is_critical_path(filepath):
        logger.warning(f'[BLOCKED]: Unsafe save attempt blocked: {filepath} is in a critical path.')
        return False

    if not is_safe_path(filepath):
        if not allow_external:
            logger.warning(f'[BLOCKED]: Unsafe [save] attempt blocked: [{filepath}] not in allowed directories.')
            return False
        else:
            logger.warning(f'[OVERRIDE]: Unsafe [save] allowed by user override: [{filepath}]')

    # Check if directory exists
    if os.path.isdir(filepath):
        logger.error(f'[FAILED]: File not saved. Filepath is a directory, expected a file: [{filepath}]')
        return False

    if os.path.isfile(filepath) and not overwrite:
        logger.warning(f'[FAILED]: File not saved. File already exists: [{filepath}]')
        return False

    try:
        with open(filepath, 'wb') as outfile:
            pickle.dump(var, outfile, fix_imports=fix_imports)
        logger.info(f'Pickle file saved: [{filepath}]')
        return True
    except Exception as e:
        logger.error(f'[FAILED]: pickle file is not saved: [{filepath}]. Error: {e}')
        return False


# %% Load Function
def load(filepath: str,
         fix_imports: bool = True,
         encoding: str = "ASCII",
         errors: str = "strict",
         validate: Union[bool, list] = True,
         verbose: str = 'info',
         ):
    """
    Load a pickle file from disk, with optional security restrictions.
    pickle files are directly loaded if all modules are in the allowlist. If the pickle file contains unknown modules, the modules needs to be validated using the validate parameter.
    pickle files that contain risky modules, i.e., those that can automatically make changes on the system or start (unwanted) applications are not allowed unless specifically specified using the validate parameter.

    | Module Type        | Allowed? | How to Change Behavior                         |
    | ------------------ | -------- | ---------------------------------------------- |
    | Unknown            | V        | Allowed unless in risky list                   |
    | Risky (`os`, etc.) | X        | Must be explicitly added via `validate=['nt']` |
    | Custom safe        | V        | If included in `validate` param                |

    Parameters
    ----------
    filepath : str
        Path to the pickle file.
    fix_imports : bool
        Compatibility for loading Python 2 pickles in Python 3.
    encoding : str
        Encoding for legacy Python 2 pickles.
    errors : str
        Error handling for decoding.
    validate : bool or list, default=True
        - True: Validate with default safe module list.
        - False: Disable all validation (use at own risk).
        - list: ['nt', 'sklearn', 'pandas'] : modules that are allowed based on name prefixes.
    verbose : str
        Verbosity level (not used here, placeholder).

    Returns
    -------
    object or None
        The loaded Python object or None if loading fails.

    Examples
    --------
    >>> # Example 1
    >>> import pypickle
    >>> filepath = 'model.pkl'
    >>> data = [1, 2, 3]
    >>> status = pypickle.save(filepath, data, overwrite=True)
    >>> # Load with validation (default)
    >>> data = pypickle.load(filepath)
    >>> data = pypickle.load(filepath, validate=False)
    >>> #
    >>> # Example 2
    >>> # Load without validation (not recommended)
    >>> data = pypickle.load(filepath, validate=False)
    >>> #
    >>> # Example 3
    >>> # Load without validation: exploit that start calculator
    >>> data = pypickle.load(r'malicious.pkl')
    >>> data = pypickle.load(r'malicious.pkl', validate=False)
    >>> mods = pypickle.validate_modules(r'malicious.pkl')
    >>> data = pypickle.load(r'malicious.pkl', validate=mods)
    >>> #
    >>> # Example 4
    >>> # Sklearn example
    >>> from sklearn.linear_model import LogisticRegression
    >>> model=LogisticRegression()
    >>> status = pypickle.save('model.pkl', model, overwrite=True)
    >>> pypickle.load('model.pkl', validate=False)
    >>> pypickle.load('model.pkl', validate=True)
    >>> #
    >>> # Example 5
    >>> mods = pypickle.validate_modules('model.pkl')
    >>> pypickle.load('model.pkl', validate=mods)
    >>> pypickle.load('model.pkl', validate='sklearn')
    >>> #

    """
    # Set the logger
    set_logger(verbose)
    # Check validate
    if isinstance(validate, str): validate = [validate]
    # User custom allow list (empty but maybe for future usage)
    allowlist = []

    # Check file
    if not os.path.isfile(filepath):
        logger.info(f'Pickle file does not exist: [{filepath}]')
        return None

    # Loading
    logger.info(f"Loading Pickle file: [{filepath}]")
    if isinstance(validate, list) or validate is True:
        # Add custom modules to the defaults
        user_modules = validate + allowlist if isinstance(validate, list) else None
        # Validate and then load
        return load_and_validate(filepath, fix_imports, encoding, errors, user_modules)
    else:
        # Load without validation
        return load_pickle(filepath, fix_imports, encoding, errors)


# %% Unsafe Loader (No Validation)
def load_pickle(filepath, fix_imports=True, encoding="ASCII", errors="strict"):
    """Load a pickle file without validation."""
    with open(filepath, "rb") as f:
        return pickle.load(f, fix_imports=fix_imports, encoding=encoding, errors=errors)


# %% Secure Pickle Loader
def load_and_validate(filepath, fix_imports=True, encoding="ASCII", errors="strict", validate_modules=None):
    """
    Securely validate pickle file contents and load it only if safe.

    Parameters
    ----------
    filepath : str
        Path to the pickle file.
    validate_modules : list or None
        List of allowed module prefixes (e.g. ['sklearn', 'numpy']).
    fix_imports : bool
    encoding : str
    errors : str

    Returns
    -------
    object or None
        The unpickled object or None if loading failed or unsafe.
    """
    try:
        # 1. Validate using custom unpickler (does not return the object, only checks)
        with open(filepath, "rb") as f:
            ValidateUnpickler(f, validate_modules=validate_modules, risky_modules=get_risk_modules()).load()
        # 2. If successful, load pickle file
        return load_pickle(filepath, fix_imports, encoding, errors)

    except pickle.UnpicklingError as e:
        # logger.error(f"UnpicklingError: The modules in the pickle file are not validated or are marked as risky.")
        logger.error(f"UnpicklingError: {e}")
    except (AttributeError, ModuleNotFoundError, EOFError, ImportError) as e:
        logger.error(f"Pickle loading failed: {e.__class__.__name__}: {e}")
    except Exception as e:
        # logger.exception("An unexpected error occurred while validating the pickle file.")
        logger.error(f"UnpicklingError: {e}")
    return None


#%%
class ValidateUnpickler(pickle.Unpickler):
    """
    Unpickler that blocks risky modules but allows user-specified modules even if they would normally be blocked.

    """
    def __init__(self, file, validate_modules=None, risky_modules=None):
        super().__init__(file)
        self.validate_modules = validate_modules if validate_modules else []
        self.risky_modules = risky_modules if risky_modules is not None else get_risk_modules()


    def find_class(self, module, name):
        full_name = f"{module}.{name}"
        # If module is explicitly validated by the user, allow it
        if any(module == allowed or module.startswith(f"{allowed}.") for allowed in self.validate_modules):
            mod = __import__(module, fromlist=[name])
            return getattr(mod, name)

        # Block risky modules/functions
        for risky in self.risky_modules:
            if '.' in risky:
                # risky is a full function name like 'os.remove'
                if full_name == risky:
                    raise pickle.UnpicklingError(f"[BLOCKED] Function '{full_name}' is considered risky. Use validate=['{module}'] to allow.")
            else:
                # risky is a module prefix like 'glob' or 'tempfile'
                if module == risky or module.startswith(f"{risky}."):
                    raise pickle.UnpicklingError(f"[BLOCKED] Module '{module}' is considered risky. Use validate=['{module}'] to allow.")

        # Otherwise allow
        mod = __import__(module, fromlist=[name])
        return getattr(mod, name)


# %% Utility: Get list of modules in pickle
def validate_modules(filepath: str) -> list:
    """
    Extract unique module names from a pickle file.

    Parameters
    ----------
    filepath : str
        Path to the pickle file.
    warn : bool
        Print warnings for risky modules (like os, subprocess).

    Returns
    -------
    list
        List of required module name prefixes (e.g. ['sklearn', 'numpy']).
    """
    modules = set()
    stack = []

    if not os.path.isfile(filepath):
        logger.error('File does not exist: [{filepath}]')
        return

    # Get risk modules
    risky_modules = get_risk_modules()
    modules_set = list({item.split('.')[0] for item in risky_modules if '.' in item})

    with open(filepath, 'rb') as f:
        for opcode, arg, _ in pickletools.genops(f):
            if opcode.name in {'BINUNICODE', 'SHORT_BINUNICODE', 'UNICODE'}:
                stack.append(arg)
            elif opcode.name == 'GLOBAL' and isinstance(arg, str):
                try:
                    module, _ = arg.strip().split(' ')
                    modules.add(module)
                    if module in risky_modules:
                        logger.warning(f"Risky module: {module}")
                except Exception:
                    continue
            elif opcode.name == 'STACK_GLOBAL':
                if len(stack) >= 2:
                    name = stack.pop()
                    module = stack.pop()
                    full_name = f"{module}.{name}"
                    if module in modules_set:
                        modules.add(full_name)
                    else:
                        modules.add(module)
                    if full_name in risky_modules:
                        logger.warning(f"Risky function: {full_name}")

    return sorted(modules)


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
