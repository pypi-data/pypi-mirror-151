import logging
from typing import Optional

import click
import pystac.utils
from pystac import CatalogType

from stactools.drcog_lulc import stac

logger = logging.getLogger(__name__)


def create_drcog_lulc_command(cli):
    """Creates the stactools-drcog-lulc command line utility."""

    @cli.group(
        "drcog-lulc",
        short_help=("Commands for working with stactools-drcog-lulc"),
    )
    def drcog_lulc():
        pass

    @drcog_lulc.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.argument("destination")
    @click.option(
        "--asset-href",
        help="Optional asset to use to create an item, which will be included in the collection",
    )
    @click.option(
        "--validate/--no-validate",
        help="Validate the collection before saving",
        default=True,
    )
    def create_collection_command(
        destination: str,
        asset_href: Optional[str],
        validate: bool,
    ):
        """Creates a STAC Collection

        \b
        Args:
            destination (str): The destination directory
            asset_href (optional, str): Href of asset to create an item, which
                will be added to the collection
        """
        collection = stac.create_collection()
        if asset_href:
            item = stac.create_item(
                asset_href=pystac.utils.make_absolute_href(asset_href)
            )
            collection.add_item(item)
        collection.normalize_hrefs(destination)
        if validate:
            collection.validate_all()
        collection.make_all_asset_hrefs_relative()
        collection.save(catalog_type=CatalogType.SELF_CONTAINED)

        return None

    @drcog_lulc.command("create-item", short_help="Create a STAC item")
    @click.argument("source")
    @click.argument("destination")
    def create_item_command(source: str, destination: str):
        """Creates a STAC Item

        Args:
            source (str): HREF of the Asset associated with the Item
            destination (str): An HREF for the STAC Collection
        """
        item = stac.create_item(source)

        item.save_object(dest_href=destination)

        return None

    return drcog_lulc
