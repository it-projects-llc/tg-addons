======================================================================
 Point of Sale - Coupons & Loyalty modifications for Tribal Gathering
======================================================================

Happy hours usage
-----------------

* Open Main menu -> Point of Sale -> Products -> Discount and Loyalty

* Create a record with following values:

  - Program name: any name

  - Program type: "Promotion"

  - Available on: "Point of Sale"

  - Are happy hours enabled: yes

  - Weekdays: choose weekdays

  - Happy hours: input period

  - Conditional rules:

    * minimum quantity: 0

    * minimum purchase: 0

    * Match all products

    * Grant 1 points per order

  - Rewards:

    * Reward type: "Discount"

    * Discount: any value

    * On: order

    * In exchange of: 1 points

* Open any POS, where loyalty program above is enabled in

* Add any product line:

* RESULT: if current time is in happy hours - discount from program above will be given

* RESULT: if current time is not in happy hours - discoutn from program above will not be given

NOTE: local browser time is used to determine if it is happy hour or not

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
