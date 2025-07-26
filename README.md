# pypickle

[![Python](https://img.shields.io/pypi/pyversions/pypickle)](https://img.shields.io/pypi/pyversions/pypickle)
[![PyPI Version](https://img.shields.io/pypi/v/pypickle)](https://pypi.org/project/pypickle/)
![GitHub Repo stars](https://img.shields.io/github/stars/erdogant/pypickle)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/pypickle/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/pypickle)](https://pepy.tech/project/pypickle)
[![Downloads](https://pepy.tech/badge/pypickle/month)](https://pepy.tech/project/pypickle/)
[![DOI](https://zenodo.org/badge/278702058.svg)](https://zenodo.org/badge/latestdoi/278702058)
[![Sphinx](https://img.shields.io/badge/Sphinx-Docs-Green)](https://erdogant.github.io/pypickle/)
<!---[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)-->
<!---[![BuyMeCoffee](https://img.shields.io/badge/buymea-coffee-yellow.svg)](https://www.buymeacoffee.com/erdogant)-->



``pypickle`` is a user-friendly Python library for saving and loading data using the pickle format. Unlike the standard ``pickle`` module, ``pypickle`` puts safety first—offering built-in validation, extension checks, and protection against common exploits.
Whether you're persisting models, storing session data, or sharing files, ``pypickle`` makes serialization easy *and* more secure.
Ideal for developers who care about both convenience and peace of mind.
⭐️ **Star it if you like it** ⭐️

---

### Key Features

| Feature | Description |
|--------|-------------|
| [**Load**](https://erdogant.github.io/pypickle/pages/html/Parametric.html) | Load your pickle files. |
| [**Save**](https://erdogant.github.io/pypickle/pages/html/Save_and_Load.html#saving) | Save your files into pickle format. |
| [**is_critical_path**](https://erdogant.github.io/pypickle/pages/html/pypickle.pypickle.html#pypickle.pypickle.is_critical_path) | Check whether filepath is critical. |
| [**get_critical_paths**](https://erdogant.github.io/pypickle/pages/html/pypickle.pypickle.html#pypickle.pypickle.get_critical_paths) | Get critical paths. |
| [**get_risk_modules**](https://erdogant.github.io/pypickle/pages/html/pypickle.pypickle.html#pypickle.pypickle.get_risk_modules) | Get risk modules. |
| [**get_allowed_paths**](https://erdogant.github.io/pypickle/pages/html/pypickle.pypickle.html#pypickle.pypickle.get_allowed_paths) | Get allowed paths. |

---

For security reasons, pickle files are validated by checking the inner modules before loading. Twenty modules are classified as high-risk (see [here](https://erdogant.github.io/pypickle/pages/html/save.html#security-mechanisms-save)) and can not be loaded without validation.

| Module Type           | Allowed? | How to Change Behavior                                                  |
|-----------------------|----------|--------------------------------------------------------------------------|
| Unknown               | ✅       | Allowed unless in high-risk list                                            |
| Custom safe           | ✅       | If included in `validate` param                                         |
| Risky (`os`, etc.)    | ❌       | Must be explicitly added via `validate=['nt']` or `validate=False`      |

---

### Resources and Links
- **Documentation:** [Website](https://erdogant.github.io/pypickle)
- **Bug Reports and Feature Requests:** [GitHub Issues](https://github.com/erdogant/pypickle/issues)

---

##### Install pypickle from PyPI
```bash
pip install pypickle     # normal install
pip install -U pypickle  # update if needed
```

#### Import pypickle package
```python
import pypickle
```

#

#### [Example: Saving](https://erdogant.github.io/pypickle/pages/html/Save_and_Load.html#saving)

```python
import pypickle
filepath = 'test.pkl'

# Some data
data = [1,2,3,4,5]

# Save
status = pypickle.save(filepath, data)

```

#

#### [Example: Loading](https://erdogant.github.io/pypickle/pages/html/Save_and_Load.html#loading)

```python

# Load file
data = pypickle.load(filepath)

```

---


### Contributors
Special thanks to the contributors!

<p align="left">
  <a href="https://github.com/erdogant/pypickle/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=erdogant/pypickle" />
  </a>
</p>

### Maintainer
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)
* Contributions are welcome.
* Yes! This library is entirely **free** but it runs on coffee! :) Feel free to support with a <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Coffee</a>.

[![Buy me a coffee](https://img.buymeacoffee.com/button-api/?text=Buy+me+a+coffee&emoji=&slug=erdogant&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/erdogant)



