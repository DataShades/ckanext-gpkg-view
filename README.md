[![Tests](https://github.com/DataShades/ckanext-gpkg-view/actions/workflows/test.yml/badge.svg)](https://github.com/DataShades/ckanext-gpkg-view/actions/workflows/test.yml)

# ckanext-gpkg-view

Simple preview for GeoPackage files.

## Features

- Preview GeoPackage files as GeoJSON
- Cache GeoJSON to avoid re-reading the file on subsequent views

## Requirements

- CKAN 2.10+
- GeoPackage files
- Python 3.8+

## Installation

Use `pypi` to install the extension:

    pip install ckanext-gpkg-view

Or install from source:

    git clone https://github.com/DataShades/ckanext-gpkg-view.git
    cd ckanext-gpkg-view
    pip install -e .


## Config settings

List of config settings:

```yaml
version: 1
groups:
  - annotation: ckanext-gpkg-view
    options:
      - key: ckanext.gpkg_view.max_file_size
        description: Maximum file size for GPKG files
        default: 25600000 # 25MB
        type: int
        editable: true

      - key: ckanext.gpkg_view.cache_duration
        description: Cache duration for GPKG files
        default: 21600 # 6 hours
        type: int
        editable: true

      - key: ckanext.gpkg_view.cache_enabled
        description: Enable caching for GPKG files
        default: true
        type: bool
        editable: true

      - key: ckanext.gpkg_view.simplify_tolerance
        description: |
          The simplification tolerance in the units of the coordinate reference
          system (CRS). Higher = more simplification. 0 = no simplification.
        default: 0
        type: int
        editable: true
```


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
