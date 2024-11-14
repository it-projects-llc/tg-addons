==================================================
 Point of Sale modifications for Tribal Gathering
==================================================

* Allows to scan customer in payment screen (feature was implemented in point_of_sale module from 10.0)

* Added user group "Point of Sale - Show customer button"

* Added user group "Point of Sale - Show +/- in payment screen"

* Contact's barcode does not depend on company (as it was in odoo 10.0)

* Option to display specific products in POS (using POS Shop feature)

POS Shop usage
--------------

* Open Main menu -> Point of Sale -> Configuration -> POS Shops

* Create record, set name and add some products

* Open Main menu -> Point of Sale -> Configuration -> Settings

* Choose "POS"

* Set "Shop" value to recently created shop record

* Save

* Open Main menu -> Point of Sale

* Open POS, where shop setting was recently set

* RESULT: only products from shop are shown

Credits
=======

Contributors
------------

* `Eugene Molotov <https://github.com/em230418>`__

* `Odoo S.A. <https://github.com/odoo>`__

Sponsors
--------

* `Tribal Gathering <https://www.tribalgathering.com/>`__

Maintainers
-----------

* `IT-Projects LLC <https://it-projects.info>`__
