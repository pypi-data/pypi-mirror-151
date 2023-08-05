![geomapiLogo](public/source/_static/geomapi_logo_B.png)
# GeomAPI

A joint API to standardize geomatic data storage and processing.

[[_TOC_]]

## Installation

Use the package manager [pip](https://pypi.org/project/geomapi) to install geomapi.

```bash
pip install geomapi
```

## Documentation

You can read the full API reference here:
[Documentation](https://geomatics.pages.gitlab.kuleuven.be/research-projects/geomapi/html/index.html)

## Usage

The main use of this API is importing standardized RDF data into easy to use python classes.
These python classes have a number of fuctions to analyse, edit and combine the most common types of data including:
- Images (pinhole or panoramic)
- Meshes
- Point clouds
- BIM models

## Development

Testing the package is done in the tests folder with:
```py
from context import geomapi
```

## Licensing

The code in this project is licensed under GNU license.
