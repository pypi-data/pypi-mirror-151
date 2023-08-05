# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyinaturalist_convert']

package_data = \
{'': ['*']}

install_requires = \
['flatten-dict>=0.4.0,<0.5.0',
 'geojson>=2.5',
 'pyinaturalist>=0.17.0',
 'tablib>=3.0,<4.0',
 'tabulate>=0.8.9,<0.9.0']

extras_require = \
{'all': ['boto3>=1.20',
         'gpxpy>=1.4.2,<2.0.0',
         'openpyxl>=2.6',
         'pandas>=1.2',
         'pyarrow>=4.0',
         'python-dwca-reader>=0.15.0,<0.16.0',
         'xmltodict>=0.12'],
 'csv': ['pandas>=1.2'],
 'df': ['pandas>=1.2'],
 'docs': ['furo>=2022.2.14.1,<2023.0.0.0',
          'myst-parser>=0.17.0,<0.18.0',
          'sphinx>=4.2.0,<5.0.0',
          'sphinx-autodoc-typehints>=1.17,<2.0',
          'sphinx-copybutton>=0.5',
          'sphinx-inline-tabs>=2022.1.2b11,<2023.0.0',
          'sphinx-panels>=0.6.0,<0.7.0',
          'sphinxcontrib-apidoc>=0.3,<0.4'],
 'dwc': ['xmltodict>=0.12'],
 'feather': ['pandas>=1.2', 'pyarrow>=4.0'],
 'gpx': ['gpxpy>=1.4.2,<2.0.0'],
 'hdf': ['pandas>=1.2', 'tables>=3.6'],
 'odp': ['boto3>=1.20'],
 'parquet': ['pandas>=1.2', 'pyarrow>=4.0'],
 'xlsx': ['openpyxl>=2.6']}

setup_kwargs = {
    'name': 'pyinaturalist-convert',
    'version': '0.3.0',
    'description': 'Convert iNaturalist observation data to and from multiple formats',
    'long_description': "# pyinaturalist-convert\n[![Build status](https://github.com/JWCook/pyinaturalist-convert/workflows/Build/badge.svg)](https://github.com/JWCook/pyinaturalist-convert/actions)\n[![Codecov](https://codecov.io/gh/JWCook/pyinaturalist-convert/branch/master/graph/badge.svg?token=FnybzVWbt2)](https://codecov.io/gh/JWCook/pyinaturalist-convert)\n[![Docs](https://img.shields.io/readthedocs/pyinaturalist-convert/stable)](https://pyinaturalist-convert.readthedocs.io)\n[![PyPI](https://img.shields.io/pypi/v/pyinaturalist-convert?color=blue)](https://pypi.org/project/pyinaturalist-convert)\n[![Conda](https://img.shields.io/conda/vn/conda-forge/pyinaturalist-convert?color=blue)](https://anaconda.org/conda-forge/pyinaturalist-convert)\n[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/pyinaturalist-convert)](https://pypi.org/project/pyinaturalist-convert)\n\nThis package provides tools to convert iNaturalist observation data to and from a wide variety of useful formats.\nThis is mainly intended for use with the iNaturalist API\n(via [pyinaturalist](https://github.com/niconoe/pyinaturalist)), but also works with other data sources.\n\nComplete project documentation can be found at [pyinaturalist-convert.readthedocs.io](https://pyinaturalist-convert.readthedocs.io).\n\n# Formats\nImport formats currently supported:\n* CSV (From either [API results](https://www.inaturalist.org/pages/api+reference#get-observations)\n or the [iNaturalist export tool](https://www.inaturalist.org/observations/export))\n* JSON (from API results, either via `pyinaturalist`, `requests`, or another HTTP client)\n* [`pyinaturalist.Observation`](https://pyinaturalist.readthedocs.io/en/stable/modules/pyinaturalist.models.Observation.html) objects\n* Parquet\n\nImport formats with partial support:\n* [iNaturalist open data on Amazon](https://github.com/inaturalist/inaturalist-open-data)\n* [iNaturalist GBIF Archive](https://www.inaturalist.org/pages/developers)\n* [iNaturalist Taxonomy Archive](https://www.inaturalist.org/pages/developers)\n\nExport formats currently supported:\n* CSV, Excel, and anything else supported by [tablib](https://tablib.readthedocs.io/en/stable/formats/)\n* Feather, Parquet, and anything else supported by [pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html)\n* GeoJSON and GPX\n* Darwin Core\n\n# Installation\nInstall with pip:\n```bash\npip install pyinaturalist-convert\n```\n\nOr with conda:\n```bash\nconda install -c conda-forge pyinaturalist-convert\n```\n\nTo keep things modular, many format-specific dependencies are not installed by default, so you may need to install some\nmore packages depending on which formats you want. See\n[pyproject.toml]([pyproject.toml](https://github.com/JWCook/pyinaturalist-convert/blob/7098c05a513ddfbc254a446aeec1dfcfa83e92ff/pyproject.toml#L44-L50))\nfor the full list (TODO: docs on optional dependencies).\n\nTo install all of the things:\n```bash\npip install pyinaturalist-convert[all]\n```\n\n# Usage\n\n## Export\nGet your own observations and save to CSV:\n```python\nfrom pyinaturalist import get_observations\nfrom pyinaturalist_convert import *\n\nobservations = get_observations(user_id='my_username')\nto_csv(observations, 'my_observations.csv')\n```\n\nOr any other supported format:\n```python\nto_dwc(observations, 'my_observations.dwc')\nto_excel(observations, 'my_observations.xlsx')\nto_feather(observations, 'my_observations.feather')\nto_gpx(observations, 'my_observations.gpx')\nto_hdf(observations, 'my_observations.hdf')\nto_parquet(observations, 'my_observations.parquet')\ndf = to_dataframe(observations)\ngeo_obs = to_geojson(observations)\n```\n\n## Import\n<!-- TODO: more details -->\nLoad your observations from the iNat Export tool, convert to be consistent with\nAPI results, and save to Parquet:\n```python\ndf = load_csv_exports('my_observations.csv')\ndf.to_parquet('my_observations.parquet')\n```\n\n## Download\nDownload the complete research-greade observations dataset:\n```python\ndownload_dwca()\n```\n\nOr the complete taxonomy dataset:\n```python\ndownload_dwca_taxa()\n```\n\nLoad taxonomy and common name data into a full text search database:\n```python\nload_taxon_fts_table(languages=['english', 'german'])\n```\n\nAnd get lightning-fast autocomplete results from it:\n```python\nta = TaxonAutocompleter()\nta.search('aves')\nta.search('flughund', language='german')\n```\n\n# Planned and Possible Features\n* Convert to an HTML report\n* Convert to print-friendly format\n* Export to any [SQLAlchemy-compatible database engine](https://docs.sqlalchemy.org/en/14/core/engines.html#supported-databases)\n* Note: see [API Recommended Practices](https://www.inaturalist.org/pages/api+recommended+practices)\n  for details on which data sources are best suited to different use cases\n",
    'author': 'Jordan Cook',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JWCook/pyinaturalist_convert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
