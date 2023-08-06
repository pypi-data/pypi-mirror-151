# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['requires']

package_data = \
{'': ['*']}

install_requires = \
['funkify>=0.4.0,<0.5.0', 'xtyping>=0.5.0']

setup_kwargs = {
    'name': 'requires',
    'version': '0.10.3',
    'description': 'Runtime imports and dependency utils',
    'long_description': '<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">\n<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>\n</a>\n\n\n# requires\n\n\n[![Wheel](https://img.shields.io/pypi/wheel/requires.svg)](https://img.shields.io/pypi/wheel/requires.svg)\n[![Version](https://img.shields.io/pypi/v/requires.svg)](https://img.shields.io/pypi/v/requires.svg)\n[![py_versions](https://img.shields.io/pypi/pyversions/requires.svg)](https://img.shields.io/pypi/pyversions/requires.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Install:** `pip install requires`\n\nDecorate that lets you\nRequire/Import dependencies at runtime.\n\nPython dependency management can be mind bottlingly complex. Optional dependencies are pretty common. Why not require the dependency at run time if a function requires said dependency?\n\nThis package has come in handy in lambda-land where you only get 250mb (on aws)!\n\n___\n\n## Usage:\n\n\n\n```python\n# This will fail\ndef uno():\n    return json.dumps({\'a\': 1, \'b\': 2})\n\ntry:\n    uno()\nexcept NameError as ne:\n    print("Error:", ne)\n```\n\n    Error: name \'json\' is not defined\n\n\n\n```python\n# This will not fail\nimport requires  # Module is callable! (checkout funkify for more info -- `pip install funkify`)\n\n@requires(\'json\')\ndef uno():\n    return json.dumps({\'a\': 1, \'b\': 2})\n\nuno()\n```\n\n\n\n\n    \'{"a": 1, "b": 2}\'\n\n\n\n\n```python\nimport requires\n\n@requires(\'from json import dumps\')\ndef uno():\n    return dumps({\'a\': 1, \'b\': 2})\n\nuno()\n```\n\n\n\n\n    \'{"a": 1, "b": 2}\'\n\n\n\n\n```python\ndef dos():\n    return dumps({\'a\': 1, \'b\': 2})\n\ndos()\n```\n\n\n\n\n    \'{"a": 1, "b": 2}\'\n\n\n\n\n```python\nimport requires\n\n@requires(_from=\'json\', _import=\'dumps\')\ndef dos():\n    return dumps({\'a\': 1, \'b\': 2})\n\ndos()\n```\n\n\n\n\n    \'{"a": 1, "b": 2}\'\n\n\n\n\n```python\nimport requires\n\n@requires(_import=\'rapidjson\', pip=\'python-rapidjson\', conda_forge=\'python-rapidjson\')\ndef tres():\n    return rapidjson.dumps({\'a\': 1, \'b\': 2})\n\ntres()  # Will err if not install with where to install instructions\n```\n\n\n\n\n    \'{"a":1,"b":2}\'\n\n\n\n\n```python\n# should error\ndef quatro():\n    return path.join(\'a\', \'b\')\n\ntry:\n    quatro()\nexcept NameError as ne:\n    print("ERROR:", ne)\n```\n\n    ERROR: name \'path\' is not defined\n\n\n\n```python\nfrom requires import Requirement\n\nos_path_req = Requirement(_import=\'path\', _from=\'os\')\n\n@os_path_req\ndef quatro():\n    return path.join(\'a\', \'b\')\n\nassert isinstance(quatro(), str)\n```\n\n## Enforcing requirements\n\n\n```python\nimport requires\n\ntry:\n    import alibrary\nexcept ModuleNotFoundError:\n    requirement = requires.Requirement(\n        _import=\'alibrary\',\n        pip=True,\n        conda_forge=\'alibrary-conda-listing\',\n        details="Install details"\n    )\ntry:\n    requirement.raise_error()\nexcept requires.RequirementError as err:\n    print("ERROR:")\n    print(err)\n```\n\n    ERROR:\n    Module/Package(s) not found/installed; could not import: `import alibrary`\n        pip install alibrary\n        conda install -c conda-forge alibrary-conda-listing\n        Install details\n\n\n## Less verbose version:\n\n```python\nimport requires\n\ntry:\n    import alibrary\nexcept ModuleNotFoundError:\n    requires.Requirement(\n        _import=\'alibrary\',\n        pip=True,\n        conda_forge=\'alibrary-conda-listing\',\n        details="Install details"\n    ).raise_error()\n```\n\n\n___\n\n## Future ideas?\n\n - Adding support for requiring particular package versions?\n - Auto install?\n - Allow non pip/conda/conda-forge locations?\n',
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs/tree/main/libs/requires',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
