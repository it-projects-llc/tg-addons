====================================
 eCommerce Rental Period Attributes
====================================

Introduces "Can be rented via attributes" option in product.


Configuration
-------------

* Main menu -> Sales -> Configuration -> Products -> Attributes

* Create attribute with following fields:

  - Variants Creation Mode: Never

  - Is period: Yes

  - Attribute values: several attribute values that will be displayed to customer.
    It expected that human readable dates will be used.
    It is also suggested to input default start/end dates, which will be used for initial start/end value of period attributes in product form.

* Main menu -> Sales -> Products

* Create product with following fields:

  - Name: any. For example "Projector"

  - Can be Rented via attributes: yes

  - Sales price: any

  - In "Attributes & Variants" section:

    - Add recently created attribute with values

    - Press "Configure"

    - For every attributes set "start date", "end date" and optionally "Value Price Extra"

Usage
-----

- Open `/shop`, find "Projector" product page

- Choose period attribute, add to cart and go to cart page

- RESULT: Price without tax will be "Sales price" from product + "Value Price Extra" from chosen attribute

- Press "Checkout"

- RESULT: Rental period will be based on attribute

- Pay this cart

- As sales administrator go to "Main Menu" -> "Rental" -> Schedule

- Edit filters to see range, that includes period of recently payed cart

- RESULT: you will see rental entry with recently payed cart

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
