import pypickle

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
