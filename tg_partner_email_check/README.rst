====================================
 Email Checker for Tribal Gathering
====================================

* Allows to register new user with email that is already used in the existing contact/partner, but without a user linked.
  The existing contact to be linked is chosen by largest credit amount (``pos_credit_notebook``) or by highest id (i.e. the last created one).

* If the "Filter duplicate email addresses" option is enabled, this module excludes the emails from duplicate checking if:

  - the contact type is "Invoice address"

  - the contact type is "Delivery address"

  - the email domain is included to "Partner Email Check Ignore" list (``Settings -> Technical -> Email -> Partner Email Check Ignore``)

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
