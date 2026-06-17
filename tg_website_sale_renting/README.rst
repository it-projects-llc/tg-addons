=====================================================
 eCommerce Rental modifications for Tribal Gathering
=====================================================

- In frontend enforces America/Panama timezone in rental date range widgets.
  In backend no timezone is enforced (default behavior).

- Allows to rent from today

Rental dates
------------

- Settings -> Rental -> Rent online

- Set following fields:

  * Renting Default Start Date

  * Renting Default End Date

  * Renting Min Start Date

  * Renting Max End Date

Also renting min start date and max end dates can be overriden in product form.

Note: in one cart you cannot mix products with default renting dates and product with specific renting dates

Usage
-----

After settings fields above:

- Navigate to shop (/shop)

- Choose existing renting product

- RESULT: default dates are set from config

- Choose other date range

- RESULT: minimal start date is set from config

- RESULT: maximal end date is set from config

Credits
=======

Contributors
------------

* `Eugene Molotov <https://github.com/em230418>`__

Sponsors
--------

* `Tribal Gathering <https://www.tribalgathering.com/>`__

Maintainers
-----------

* `IT-Projects LLC <https://it-projects.info>`__
