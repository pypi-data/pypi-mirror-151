# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ngsildclient',
 'ngsildclient.api',
 'ngsildclient.api.helper',
 'ngsildclient.model',
 'ngsildclient.model.helper',
 'ngsildclient.utils']

package_data = \
{'': ['*']}

install_requires = \
['geojson>=2.5.0,<3.0.0', 'requests>=2.26.0,<3.0.0', 'rich>=12.4.1,<13.0.0']

setup_kwargs = {
    'name': 'ngsildclient',
    'version': '0.1.9',
    'description': 'A Python library that helps building NGSI-LD entities and interacting with a NGSI-LD Context Broker',
    'long_description': '# The ngsildclient library\n\n[![NGSI-LD badge](https://img.shields.io/badge/NGSI-LD-red.svg)](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.02.01_60/gs_CIM009v010201p.pdf)\n[![SOF support badge](https://nexus.lab.fiware.org/repository/raw/public/badges/stackoverflow/fiware.svg)](http://stackoverflow.com/questions/tagged/fiware)\n<br>\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Read the Docs](https://img.shields.io/readthedocs/ngsildclient)](https://ngsildclient.readthedocs.io/en/latest/index.html)\n<br>\n[![deploy status](https://github.com/Orange-OpenSource/python-ngsild-client/workflows/CI/badge.svg)](https://github.com/Orange-OpenSource/python-ngsild-client/actions)\n[![PyPI](https://img.shields.io/pypi/v/ngsildclient.svg)](https://pypi.org/project/ngsildclient/)\n[![Python version](https://img.shields.io/pypi/pyversions/ngsildclient)](https://pypi.org/project/ngsildclient/)\n\n\n## Overview\n\n **ngsildclient** is a Python library that helps building NGSI-LD entities and allows to interact with a NGSI-LD Context Broker.\n\n The library primary purpose is to **ease and speed up the development of a NGSI Agent** and is also **useful for Data Modeling in the design stage**.\n\n## Key Features\n\n### Build NGSI-LD entities\n\nThe task of building a large NGSI-LD compliant entity is tedious, error-prone and results in a significant amount of code. \n\n**ngsildclient** provides primitives to build and manipulate NGSI-LD compliant entities without effort, in respect with the [ETSI specifications](https://www.etsi.org/committee/cim).\n\n### Implement the NGSI-LD API\n\n**ngsildclient** provides a NGSI-LD API Client implementation.\n\nActing as a Context Producer/Consumer **ngsildclient** is able to send/receive NGSI-LD entities to/from the Context Broker for creation and other operations.\n\nThe library wraps a large subset of the API endpoints and supports batch operations, queries, subscriptions.\n\n## Where to get it\n\nThe source code is currently hosted on GitHub at :\nhttps://github.com/Orange-OpenSource/python-ngsild-client\n\nBinary installer for the latest released version is available at the [Python\npackage index](https://pypi.org/project/ngsildclient).\n\n```sh\npip install ngsildclient\n```\n\n## Installation\n\n**ngsildclient** requires Python 3.9+.\n\nOne should use a virtual environment. For example with pyenv.\n\n```sh\nmkdir myagent && cd myagent\npyenv virtualenv 3.10.2 myagent\npyenv local myagent\npip install ngsildclient\n```\n\n## Getting started\n\nThe following code snippet builds a NGSI-LD entity related to a measure of air quality in Bordeaux then sends it to the Context Broker.\n\n```python\nfrom ngsildclient import Entity, Client\n\ne = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T09:00:00Z")\ne.tprop("dateObserved").gprop("location", (44.84044, -0.5805))\ne.prop("PM2.5", 12, unitcode="GP").prop("PM10", 18, unitcode="GP")\ne.prop("NO2", 8, unitcode="GP").prop("O3", 83, unitcode="GP")\ne.rel("refDevice", "Device:AirProbe42")\nwith Client() as client:\n    client.upsert(e)\n```\n\nThe corresponding JSON-LD [payload](https://github.com/Orange-OpenSource/python-ngsild-client/blob/master/samples/gettingstarted.json) has been generated.\n\n## Documentation\n\nUser guide is available on [Read the Docs](https://ngsildclient.readthedocs.io/en/latest/index.html).\n\n## License\n\n[Apache 2.0](LICENSE)\n',
    'author': 'fbattello',
    'author_email': 'fabien.battello@orange.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Orange-OpenSource/python-ngsild-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
