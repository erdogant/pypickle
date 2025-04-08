import pypickle

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
    assert data_load==data

# %%
