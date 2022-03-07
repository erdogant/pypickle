# pypickle

[![Python](https://img.shields.io/pypi/pyversions/pypickle)](https://img.shields.io/pypi/pyversions/pypickle)
[![PyPI Version](https://img.shields.io/pypi/v/pypickle)](https://pypi.org/project/pypickle/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/pypickle/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/pypickle/month)](https://pepy.tech/project/pypickle/month)
[![Downloads](https://pepy.tech/badge/pypickle)](https://pepy.tech/project/pypickle)
[![DOI](https://zenodo.org/badge/278702058.svg)](https://zenodo.org/badge/latestdoi/278702058)
[![Sphinx](https://img.shields.io/badge/Sphinx-Docs-Green)](https://erdogant.github.io/pypickle/)
<!---[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)-->
<!---[![BuyMeCoffee](https://img.shields.io/badge/buymea-coffee-yellow.svg)](https://www.buymeacoffee.com/erdogant)-->


* pypickle is for saving data and loading the files in pickle format.

# 
**⭐️ Star this repo if you like it ⭐️**
# 


### [Documentation pages](https://erdogant.github.io/pypickle/)

On the [documentation pages](https://erdogant.github.io/pypickle/) you can find more information about ``pypickle`` with examples. 

# 

##### Install bnlearn from PyPI
```bash
pip install pypickle     # normal install
pip install -U pypickle  # update if needed
```

#### Import pypickle package
```python
import pypickle
```

#

### [Example: Saving](https://erdogant.github.io/pypickle/pages/html/Save_and_Load.html#saving)

#

### [Example: Loading](https://erdogant.github.io/pypickle/pages/html/Save_and_Load.html#loading)


```python
import pypickle
filepath = 'test.pkl'

# Some data
data = [1,2,3,4,5]

# Save
status = pypickle.save(filepath, data)

# Load file
data = pypickle.load(filepath)

```

### Contribute
* All kinds of contributions are welcome!

### Citation
Please cite pypickle in your publications if this is useful for your research. See column right for citation information.

### Maintainer
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)
* Contributions are welcome.
* If you wish to buy me a <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Coffee</a> for this work, it is very appreciated :)

