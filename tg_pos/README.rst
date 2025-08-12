==================================================
 Point of Sale modifications for Tribal Gathering
==================================================

* Allows to scan customer in payment screen (feature was implemented in point_of_sale module from 10.0)

* In POS loads all partners at once (feature existed in Odoo 10.0 - 16.0)
  No need to press "Search More" in partner list screen

* Added user group "Point of Sale - Show customer button"

* Added user group "Point of Sale - Show +/- in payment screen"

* Added user group "Point of Sale - Enable pricelist button".
  If user belongs to this group, pricelist button will be enabled, otherwise disabled.

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

Automatic invoice duplication
-----------------------------

- Make sure, you are able to manually create duplicated invoice.
  See "Duplicate to fiscal invoice" section from tg_account's readme

- Open Main menu -> Point of Sale -> Configuration -> Settings

- Choose POS

- Make sure, that POS belongs to company, where fiscal company is set

- Save

- Open Main menu -> Point of Sale

- Open POS, what was configured above

- Make order, set "Invoice" flag, validate order

- RESULT: order has been successfully validated

- Open Main menu -> Point of Sale -> Orders

- Open last order, click on "Invoice" smart button

- RESULT: "Duplicated Fiscal Invoice" field it set (see "Other Info" tab)

- Return back to POS

- Make order, set 100% discount, set "Invoice" flag, validate order

- RESULT: order has been successfully validated

- Open Main menu -> Point of Sale -> Orders

- Open last order, click on "Invoice" smart button

- RESULT: "Duplicated Fiscal Invoice" field it NOT set (see "Other Info" tab)

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
