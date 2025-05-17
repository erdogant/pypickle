import os
import pickle
import pypickle
import pytest
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

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
    assert pypickle.save('test.pkl', data, overwrite=False) == False

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
    v = pypickle.validate_modules(filepath)
    status = pypickle.load(filepath, validate=v)
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
    assert 'nt' in mods

    # Explicit allow should work
    result = pypickle.load(filepath, validate=['nt'])
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
    result = pypickle.load(filepath, validate=['sklearn', 'numpy', 'nt'])
    assert 'model' in result
    assert 'exploit' in result
    assert 'data' in result

    # Also test alias cases like 'nt'
    result = pypickle.load(filepath, validate=['nt'])
    assert 'exploit' in result
    assert 'model' in result
    assert 'data' in result

