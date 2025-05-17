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



pypickle is for saving data and loading the files in pickle format. ⭐️**Star it if you like it**⭐️

---

### Key Features

| Feature | Description |
|--------|-------------|
| [**Load**](https://erdogant.github.io/pypickle/pages/html/Parametric.html) | Load your pickle files. |
| [**Save**](https://erdogant.github.io/pypickle/pages/html/Save_and_Load.html#saving) | Save your files into pickle format. |

---

For security reasons, pickle files are validated by checking the inner modules before loading. Twenty modules are classified as high-risk (see [here](https://erdogant.github.io/pypickle/pages/html/Save_and_Load.html#risk-modules)) and can not be loaded without validation.

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
Setting up and maintaining bnlearn has been possible thanks to users and contributors. Thanks to:

<p align="left">
  <a href="https://github.com/erdogant/pypickle/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=erdogant/pypickle" />
  </a>
</p>

### Maintainer
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)
* Contributions are welcome.
* Yes! This library is entirely **free**, but it runs on coffee! :) Feel free to support with a <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Coffee</a>.

<a href="https://www.buymeacoffee.com/erdogant"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=erdogant&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


