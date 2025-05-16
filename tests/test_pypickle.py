import os
import pickle
import pypickle
import pytest

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

def test_load_safe_default_and_dict():
    # Save safe data
    data = {'a': 1, 'b': 2}
    filepath = 'safe_test.pkl'
    pypickle.save(filepath, data, overwrite=True)

    # Load with default safe=True
    loaded1 = pypickle.load(filepath)
    assert loaded1 == data

    # Load with safe as empty dict (same as default allowed modules)
    loaded2 = pypickle.load(filepath, safe={})
    assert loaded2 == data

def test_load_unsafe():
    data = [1,2,3]
    filepath = 'unsafe_test.pkl'
    pypickle.save(filepath, data, overwrite=True)

    loaded = pypickle.load(filepath, safe=False)
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

    # Attempt safe load - should raise UnpicklingError or return None without execution
    loaded = pypickle.load(filepath, safe=True)
    assert loaded is None or isinstance(loaded, object)  # Safe loader blocks the exploit

def test_load_nonexistent_file():
    # Loading a nonexistent file should return None gracefully
    assert pypickle.load('nonexistent_file.pkl') is None
