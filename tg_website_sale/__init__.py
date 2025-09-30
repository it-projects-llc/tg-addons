from . import models
from . import controllers

import importlib

if (
    importlib.util.find_spec("odoo.addons.website_sale_renting_product_configurator")
    is not None
):
    # importing enterprise module
    # without adding it as dependency
    from . import website_sale_renting_fix
