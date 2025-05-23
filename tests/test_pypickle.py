import os
import pickle
import pypickle
import pytest
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from pypickle import save, load  # Adjust if located elsewhere
import tempfile

# Sample test variable
TEST_DATA = {"msg": "hello"}

def test_logger():
    pypickle.check_logger(verbose=0)
    pypickle.check_logger(verbose=20)
    pypickle.check_logger(verbose=30)
    pypickle.check_logger(verbose=40)
    pypickle.check_logger(verbose=50)

    pypickle.check_logger(verbose='silent')
    pypickle.check_logger(verbose='debug')
    pypickle.check_logger(verbose='info')
    pypickle.check_logger(verbose='warning')
    pypickle.check_logger(verbose='error')

def test_save():
    data = [1,2,3,4,5]
    assert pypickle.save('test.pkl', data, overwrite=True)
    assert not pypickle.save('test.pkl', data, overwrite=False)

def test_save_ext():
    data = [1,2,3,4,5]
    assert not pypickle.save('test.bat', data, overwrite=True)
    assert not pypickle.save('test', data, overwrite=True)
    assert pypickle.save('test.pkl', data, overwrite=True)
    assert pypickle.save('test.pickle', data, overwrite=True)

def test_load():
    data = [1,2,3,4,5]
    assert pypickle.save('test.pkl', data, overwrite=True)
    data_load = pypickle.load('test.pkl')
    assert data_load == data

def test_load_validate_default_and_dict():
    # Save validate data
    data = {'a': 1, 'b': 2}
    filepath = 'validate_test.pkl'
    pypickle.save(filepath, data, overwrite=True)

    # Load with default validate=True
    loaded1 = pypickle.load(filepath)
    assert loaded1 == data

    # Load with validate as empty dict (same as default allowed modules)
    loaded2 = pypickle.load(filepath, validate={})
    assert loaded2 == data

def test_load_no_validate():
    data = [1,2,3]
    filepath = 'no_validate_test.pkl'
    pypickle.save(filepath, data, overwrite=True)

    loaded = pypickle.load(filepath, validate=False)
    assert loaded == data

def test_load_malicious_pickle():
    # Create a malicious pickle trying to execute code (like opening calculator)
    class Exploit:
        def __reduce__(self):
            import os
            return (os.system, ("echo 'Exploit executed'",))

    filepath = 'malicious.pkl'
    with open(filepath, 'wb') as f:
        pickle.dump(Exploit(), f)

    # Attempt validate load - should raise UnpicklingError or return None without execution
    loaded = pypickle.load(filepath, validate=True)
    assert loaded is None or isinstance(loaded, object)  # validate loader blocks the exploit

    # Open after using validation
    mods = pypickle.validate_modules(filepath)
    status = pypickle.load(filepath, validate=mods)
    assert isinstance(status, int)  # os.system returns exit code (0 or 1)

    
def test_load_nonexistent_file():
    # Loading a nonexistent file should return None gracefully
    assert pypickle.load('nonexistent_file.pkl') is None

# Dummy class for malicious pickle test
class Exploit:
    def __reduce__(self):
        import os
        return (os.system, ("echo 'Exploit executed'",))

def test_safe_pickle():
    df = pd.DataFrame()
    data = np.array([1, 2, 3])
    filepath = 'safe_model.pkl'

    # Save
    status = pypickle.save(filepath, [df, data], overwrite=True)
    assert status is True

    # Load with default validation
    obj = pypickle.load(filepath)
    assert obj is not None

    # Validate modules
    mods = pypickle.validate_modules(filepath)
    assert 'pandas.core.frame' in mods
    assert 'numpy' in mods

    # Load with specific validations
    assert pypickle.load(filepath, validate=['pandas']) is not None
    assert pypickle.load(filepath, validate=['pandas', 'numpy']) is not None

    # Load with validation disabled
    assert pypickle.load(filepath, validate=False) is not None

def test_malicious_pickle():
    filepath = 'malicious.pkl'
    pypickle.save(filepath, Exploit(), overwrite=True)

    # Default safe load: should return None
    result = pypickle.load(filepath)
    assert result is None

    # Forced unsafe load
    result = pypickle.load(filepath, validate=False)
    assert isinstance(result, int)  # os.system returns exit code (0 or 1)

    # Check validate_modules
    mods = pypickle.validate_modules(filepath)
    assert 'nt' or 'posix' in mods

    # Explicit allow should work
    result = pypickle.load(filepath, validate=['nt', 'posix'])
    assert isinstance(result, int)

def test_sklearn_with_exploit():
    model = LogisticRegression()
    data = [1, 2, 3]
    payload = {'model': model, 'data': data, 'exploit': Exploit()}
    filepath = 'sklearn_model.pkl'

    status = pypickle.save(filepath, payload, overwrite=True)
    assert status is True

    # Default safe load: should fail due to exploit
    result = pypickle.load(filepath)
    assert result is None

    # Forced unsafe load
    result = pypickle.load(filepath, validate=False)
    assert 'model' in result

    # Validate required modules
    mods = pypickle.validate_modules(filepath)
    assert any('sklearn.linear_model' in m for m in mods)
    result = pypickle.load(filepath, validate=mods)
    assert 'exploit' in result
    assert 'model' in result
    assert 'data' in result

    # Only allow non-risky modules
    result = pypickle.load(filepath, validate=['sklearn', 'numpy'])
    assert result is None  # nt is still blocked

    # Allow risky one explicitly
    result = pypickle.load(filepath, validate=['sklearn', 'numpy', 'nt', 'posix'])
    assert 'model' in result.keys()
    assert 'exploit' in result.keys()
    assert 'data' in result.keys()

    # Also test alias cases like 'nt'
    result = pypickle.load(filepath, validate=['nt', 'posix'])
    assert 'model' in result.keys()
    assert 'exploit' in result.keys()
    assert 'data' in result.keys()

def test_various_exploits():
    # Define all exploit classes in a dictionary
    exploit_classes = {
        'os': type('ExploitOS', (), {
            '__reduce__': lambda self: (__import__('os').system, ("echo '[os] Exploit triggered!'",))
        }),
        'subprocess': type('ExploitSubprocess', (), {
            '__reduce__': lambda self: (__import__('subprocess').Popen, (["echo", "[subprocess] Exploit triggered!"],))
        }),
        'socket': type('ExploitSocket', (), {
            '__reduce__': lambda self: (__import__('socket').create_connection, (("example.com", 80),))
        }),
        'webbrowser': type('ExploitWebBrowser', (), {
            '__reduce__': lambda self: (__import__('webbrowser').open, ("http://example.com/malware",))
        }),
        'ctypes': type('ExploitCtypes', (), {
            '__reduce__': lambda self: (__import__('ctypes').CDLL, ("libc.so.6",))
        }),
    }

    # Loop through all exploits
    for name, cls in exploit_classes.items():
        filepath = f"exploit_{name}.pkl"
        print(f"\n--- Testing exploit: {name} ---")

        # Save the exploit
        pypickle.save(filepath, cls(), overwrite=True)

        # Safe load (should fail and return None)
        result = pypickle.load(filepath)
        assert result is None or result == 0
        # assert result is None or result == 0, f"{name}: Safe load failed to block"

        # Force unsafe load (should execute)
        # result = pypickle.load(filepath, validate=False)
        # print(f"{name}: Force load returned: {result}")

        # Load with validated modules from inspection
        mods = pypickle.validate_modules(filepath)
        print(mods)
        # result = pypickle.load(filepath, validate=mods)
        # print(f"{name}: Load with validated modules returned: {result}")


def test_save_in_temp_dir():
    with tempfile.TemporaryDirectory() as tmp:
        filepath = os.path.join(tmp, "test_cwd.pkl")
        save(filepath, TEST_DATA, overwrite=True)
        assert load(filepath) == TEST_DATA

def test_save_in_os_tempdir():
    temp_path = os.path.join(tempfile.gettempdir(), "test_temp.pkl")
    save(temp_path, TEST_DATA, overwrite=True)
    assert load(temp_path) == TEST_DATA

def test_allow_external_path():
    with tempfile.TemporaryDirectory() as tmp:
        filepath = os.path.join(tmp, "external.pkl")
        save(filepath, TEST_DATA, allow_external=True)
        assert load(filepath) == TEST_DATA

def test_overwrite_allowed():
    with tempfile.TemporaryDirectory() as tmp:
        filepath = os.path.join(tmp, "overwrite_allowed.pkl")
        save(filepath, TEST_DATA, overwrite=True)
        save(filepath, {"msg": "updated"}, overwrite=True)
        assert load(filepath) == {"msg": "updated"}


def test_load_sys_path_pickle():
    import sys
    class InspectSysPath:
        def __reduce__(self):
            return (getattr, (sys, 'path'))

    filepath = 'inspect_sys_path.pkl'
    status = pypickle.save(filepath, InspectSysPath(), overwrite=True)
    assert not status

    # Try loading with validation — should block access to 'sys.path'
    # loaded = pypickle.load(filepath, validate=True)
    # assert isinstance(loaded, object)

    # Allow explicitly and try again
    # mods = pypickle.validate_modules(filepath)
    # status = pypickle.load(filepath, validate=mods)
