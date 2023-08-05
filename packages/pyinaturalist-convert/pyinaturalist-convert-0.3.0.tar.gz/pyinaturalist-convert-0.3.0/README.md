# pyinaturalist-convert
[![Build status](https://github.com/JWCook/pyinaturalist-convert/workflows/Build/badge.svg)](https://github.com/JWCook/pyinaturalist-convert/actions)
[![Codecov](https://codecov.io/gh/JWCook/pyinaturalist-convert/branch/master/graph/badge.svg?token=FnybzVWbt2)](https://codecov.io/gh/JWCook/pyinaturalist-convert)
[![Docs](https://img.shields.io/readthedocs/pyinaturalist-convert/stable)](https://pyinaturalist-convert.readthedocs.io)
[![PyPI](https://img.shields.io/pypi/v/pyinaturalist-convert?color=blue)](https://pypi.org/project/pyinaturalist-convert)
[![Conda](https://img.shields.io/conda/vn/conda-forge/pyinaturalist-convert?color=blue)](https://anaconda.org/conda-forge/pyinaturalist-convert)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/pyinaturalist-convert)](https://pypi.org/project/pyinaturalist-convert)

This package provides tools to convert iNaturalist observation data to and from a wide variety of useful formats.
This is mainly intended for use with the iNaturalist API
(via [pyinaturalist](https://github.com/niconoe/pyinaturalist)), but also works with other data sources.

Complete project documentation can be found at [pyinaturalist-convert.readthedocs.io](https://pyinaturalist-convert.readthedocs.io).

# Formats
Import formats currently supported:
* CSV (From either [API results](https://www.inaturalist.org/pages/api+reference#get-observations)
 or the [iNaturalist export tool](https://www.inaturalist.org/observations/export))
* JSON (from API results, either via `pyinaturalist`, `requests`, or another HTTP client)
* [`pyinaturalist.Observation`](https://pyinaturalist.readthedocs.io/en/stable/modules/pyinaturalist.models.Observation.html) objects
* Parquet

Import formats with partial support:
* [iNaturalist open data on Amazon](https://github.com/inaturalist/inaturalist-open-data)
* [iNaturalist GBIF Archive](https://www.inaturalist.org/pages/developers)
* [iNaturalist Taxonomy Archive](https://www.inaturalist.org/pages/developers)

Export formats currently supported:
* CSV, Excel, and anything else supported by [tablib](https://tablib.readthedocs.io/en/stable/formats/)
* Feather, Parquet, and anything else supported by [pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html)
* GeoJSON and GPX
* Darwin Core

# Installation
Install with pip:
```bash
pip install pyinaturalist-convert
```

Or with conda:
```bash
conda install -c conda-forge pyinaturalist-convert
```

To keep things modular, many format-specific dependencies are not installed by default, so you may need to install some
more packages depending on which formats you want. See
[pyproject.toml]([pyproject.toml](https://github.com/JWCook/pyinaturalist-convert/blob/7098c05a513ddfbc254a446aeec1dfcfa83e92ff/pyproject.toml#L44-L50))
for the full list (TODO: docs on optional dependencies).

To install all of the things:
```bash
pip install pyinaturalist-convert[all]
```

# Usage

## Export
Get your own observations and save to CSV:
```python
from pyinaturalist import get_observations
from pyinaturalist_convert import *

observations = get_observations(user_id='my_username')
to_csv(observations, 'my_observations.csv')
```

Or any other supported format:
```python
to_dwc(observations, 'my_observations.dwc')
to_excel(observations, 'my_observations.xlsx')
to_feather(observations, 'my_observations.feather')
to_gpx(observations, 'my_observations.gpx')
to_hdf(observations, 'my_observations.hdf')
to_parquet(observations, 'my_observations.parquet')
df = to_dataframe(observations)
geo_obs = to_geojson(observations)
```

## Import
<!-- TODO: more details -->
Load your observations from the iNat Export tool, convert to be consistent with
API results, and save to Parquet:
```python
df = load_csv_exports('my_observations.csv')
df.to_parquet('my_observations.parquet')
```

## Download
Download the complete research-greade observations dataset:
```python
download_dwca()
```

Or the complete taxonomy dataset:
```python
download_dwca_taxa()
```

Load taxonomy and common name data into a full text search database:
```python
load_taxon_fts_table(languages=['english', 'german'])
```

And get lightning-fast autocomplete results from it:
```python
ta = TaxonAutocompleter()
ta.search('aves')
ta.search('flughund', language='german')
```

# Planned and Possible Features
* Convert to an HTML report
* Convert to print-friendly format
* Export to any [SQLAlchemy-compatible database engine](https://docs.sqlalchemy.org/en/14/core/engines.html#supported-databases)
* Note: see [API Recommended Practices](https://www.inaturalist.org/pages/api+recommended+practices)
  for details on which data sources are best suited to different use cases
