# pypickle

[![Python](https://img.shields.io/pypi/pyversions/pypickle)](https://img.shields.io/pypi/pyversions/pypickle)
[![PyPI Version](https://img.shields.io/pypi/v/pypickle)](https://pypi.org/project/pypickle/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/pypickle/blob/master/LICENSE)
[![BuyMeCoffee](https://img.shields.io/badge/buymea-coffee-brown.svg)](https://www.buymeacoffee.com/erdogant)
[![Downloads](https://pepy.tech/badge/pypickle/month)](https://pepy.tech/project/pypickle/month)
[![Downloads](https://pepy.tech/badge/pypickle)](https://pepy.tech/project/pypickle)
<!---[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)-->


* pypickle is for saving and loading files in pickle format.

### Installation
* Install pypickle from PyPI (recommended). pypickle is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 

```bash
pip install pypickle     # normal install
pip install -U pypickle  # update if needed
```

#### Import pypickle package
```python
import pypickle
```

#### Example:
```python
import pypickle
filepath = 'tes1t.pkl'

# Some data
data = [1,2,3,4,5]

# Save
status = pypickle.save(filepath, data)

# Load file
data = pypickle.load(filepath)

```
#### References
* https://github.com/erdogant/pypickle

### Maintainer
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)
* Contributions are welcome.
* If you wish to buy me a <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Coffee</a> for this work, it is very appreciated :)
	Star it if you like it!
