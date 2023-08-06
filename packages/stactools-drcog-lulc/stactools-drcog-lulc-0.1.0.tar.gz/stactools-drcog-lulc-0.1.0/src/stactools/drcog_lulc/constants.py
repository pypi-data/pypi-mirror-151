import datetime
from typing import Any, Dict

from pystac import (
    Extent,
    Link,
    MediaType,
    Provider,
    ProviderRole,
    SpatialExtent,
    Summaries,
    TemporalExtent,
)
from pystac.extensions.item_assets import AssetDefinition

ITEM_ID = "drcog-lulc-hr-pilot"
ITEM_DESCRIPTION = "DRCOG LULC at 1m resolution for year 2018"
MISSION = "DRCOG LULC"
EPSG = 26913
START_TIME = datetime.datetime.fromisoformat("2018-01-01T00:00:00+00:00")
END_TIME = datetime.datetime.fromisoformat("2018-12-31T23:59:59+00:00")
CLASSIFICATION_SCHEMA = (
    "https://stac-extensions.github.io/classification/v1.0.0/schema.json"
)

ASSET_PROPS: Dict[str, Any] = {
    "data": {
        "title": "DRCOG LULC",
        "description": "Denver Regional Council of Governments (DRCOG) Land Use Land Cover (LULC) classifications",  # noqa
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "roles": ["data"],
        "raster:bands": [
            {
                "description": "Classification values",
                "sampling": "area",
                "data_type": "uint8",
                "spatial_resolution": 1,
            }
        ],
        "classification:classes": [
            {"value": 1, "description": "Structures", "color_hint": "FF0000"},
            {"value": 2, "description": "Impervious Surfaces", "color_hint": "B2B2B2"},
            {"value": 3, "description": "Water", "color_hint": "00A9E6"},
            {
                "value": 4,
                "description": "Prairie/Grassland/Natural Ground Cover",
                "color_hint": "C7D79E",
            },
            {"value": 5, "description": "Tree Canopy", "color_hint": "267300"},
            {"value": 6, "description": "Turf/Irrigated Land", "color_hint": "70A800"},
            {"value": 7, "description": "Barren Land", "color_hint": "FFEBAF"},
            {"value": 8, "description": "Cropland", "color_hint": "FFAE42"},
        ],
    }
}

COLLECTION_ID = "drcog-lulc"
COLLECTION_TITLE = "DRCOG LULC 2018"
COLLECTION_DESCRIPTION = "In 2018, DRCOG partnered with the Babbitt Center for Land and Water Policy and the Chesapeake Conservancy's Conservation Innovation Center to create a pilot land use land cover data set covering 1000 square miles of the region. Input data sets included USDAs 1-meter National Agriculture Imagery Program (NAIP) 2017 aerial imagery and leaf-off aerial orthoimagery captured in March 2018 as part of the Denver Regional Aerial Photography Project (6-inch resolution everywhere except the mountainous regions to the west, which came in 1-foot resolution).Where available, high resolution planimetric data sets from DRCOG's Regional Planimetric Project were incorporated, reflecting ground conditions in 2016: building footprints, driveways and sidewalks, edge of pavement (including most roads), and parking lots."  # noqa
LICENSE = "proprietary"
LICENSE_LINK = Link(
    rel="license", target="https://drcog.org/legal-terms", title="DRCOG Legal Terms"
)
KEYWORDS = ["Land Cover", "Land Use", "NAIP", "USDA"]
PROVIDERS = [
    Provider(
        name="Denver Regional Council of Governments",
        roles=[
            ProviderRole.LICENSOR,
            ProviderRole.PRODUCER,
            ProviderRole.HOST,
            ProviderRole.PROCESSOR,
        ],
        url=(
            "https://drcog.org/services-and-resources/data-maps-and-modeling/"
            "regional-land-use-land-cover-project"
        ),
    )
]
EXTENT = Extent(
    SpatialExtent([[-104.867784, 39.549871, -104.641093, 39.667712]]),
    TemporalExtent([[START_TIME, END_TIME]]),
)
SUMMARIES = Summaries({"mission": [MISSION]})
ITEM_ASSETS = {
    "data": AssetDefinition(
        {
            "type": MediaType.COG,
            "title": ASSET_PROPS["data"]["title"],
            "description": ASSET_PROPS["data"]["description"],
            "raster:bands": ASSET_PROPS["data"]["raster:bands"],
            "classification:classes": ASSET_PROPS["data"]["classification:classes"],
            "roles": ASSET_PROPS["data"]["roles"],
        }
    )
}
REPORT_LINK = Link(
    rel="describedby",
    target="https://gis.drcog.org/rdc/supplemental/lulc_pilot_report.zip",
    title="Supplemental Information",
)
DATA_LINK = Link(
    rel="original",
    target="https://www.dropbox.com/s/0v2g1nqigm8604h/DRCOG_Final_Classification.zip?dl=0",
    title="DRCOG_Final_Classification",
)
