=====================================================
 eCommerce Rental modifications for Tribal Gathering
=====================================================

- In frontend enforces America/Panama timezone in rental date range widgets.
  In backend no timezone is enforced (default behavior).

Rental dates defaults
---------------------

- Settings -> Rental -> Rent online

- Set following fields:

  * Renting Default Start Date

  * Renting Default End Date

  * Renting Min Start Date

  * Renting Max End Date

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
