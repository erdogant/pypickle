# %%
import pypickle
print(dir(pypickle))
print(pypickle.__version__)

# %% Verbose test
import pypickle
pypickle.check_logger(verbose=0)
pypickle.check_logger(verbose=1)
pypickle.check_logger(verbose=2)
pypickle.check_logger(verbose=3)
pypickle.check_logger(verbose=4)
pypickle.check_logger(verbose=5)
pypickle.check_logger(verbose=6)

pypickle.check_logger(verbose=0)
pypickle.check_logger(verbose=20)
pypickle.check_logger(verbose=30)
pypickle.check_logger(verbose=40)
pypickle.check_logger(verbose=50)

from distfit import distfit
dfit = distfit(verbose='debug')
dfit.check_verbosity()

pypickle.check_logger(verbose='silent')
pypickle.check_logger(verbose='debug')
pypickle.check_logger(verbose='info')
pypickle.check_logger(verbose='warning')
pypickle.check_logger(verbose='error')


# %%
filepath = 'test.pkl'
data = [1,2,3,4,5]
status = pypickle.save(filepath, data, fix_imports=True, overwrite=True)

#%% Load file
data = pypickle.load(filepath, encoding="latin1")

# %%
