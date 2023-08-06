# stactools-drcog-lulc

- Name: drcog-lulc
- Package: `stactools.drcog_lulc`
- PyPI: https://pypi.org/project/stactools-drcog-lulc/
- Owner: @pholleway
- Dataset homepage: https://drcog.org/services-and-resources/data-maps-and-modeling/regional-land-use-land-cover-project
- STAC extensions used:
  - [classification](https://github.com/stac-extensions/classification/)
  - [item-assets](https://github.com/stac-extensions/item-assets)
  - [proj](https://github.com/stac-extensions/projection)
  - [raster](https://github.com/stac-extensions/raster)
  - [scientific](https://github.com/stac-extensions/scientific)

DRCOG provides the original data in a geodatabase. GDAL, a translator library for raster and vector geospatial data formats, was utilized to generate a cloud optimized GeoTIFF (COG).

This repository will assist you in the generation of STAC files for 2018 Denver Regional Council of Goverments (DRCOG) high resolution Land Use Land Cover (LULC) dataset.

## Examples

### STAC objects

- [Collection](examples/collection.json)
- [Item](examples/drcog-lulc-hr-pilot/drcog-lulc-hr-pilot.json)

### Command-line usage

To create a STAC `Item`:

```bash
stac drcog-lulc create-item tests/data-files/drcog_lulc_hr_pilot_1m.tif item.json
```

To create a STAC `Collection` from a list of DRCOG asset hrefs:

```bash
stac drcog-lulc create-collection examples --asset-href tests/data-files/drcog_lulc_hr_pilot_1m.tif
```

The above `create-collection` command is exactly how the contents of the `examples` directory are generated.

Use `stac drcog-lulc --help` to see all subcommands and options.
