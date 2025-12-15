===============
 Combo tickets
===============

Shuttle tickets - configuration
-------------------------------

- Main menu -> Events -> Choose exising or add new event

- In "Tickets" tab add tickets, if none exists

- In questions tab:

  * add generic questions like name, email

  * add question with type "Selection" and "Is shuttle" checked.

    For this question add answers and corresponding tickets.

    If you already have prepared shuttle events with tickets - you can use "Generate shuttle tickets" button

- Close question form

- Save

Shuttle tickets - usage
-----------------------

- Go to `/events`

- Click on "Register" button in event, that was used in configuration above,
  choose one ticket

- Fill all fields registration data

- Input non-empty answer for shuttle question

- RESULT: shuttle price warning will appear

- Input empty answer for shuttle question

- RESULT: shuttle price warning will disappear

- Input non-empty answer for shuttle question

- Proceed to cart

- RESULT: you will have at least 2 lines in cart.
  One is related to event, that you are registerting.
  Second one is related to shuttle event, that is used in shuttle question

Accomodation - configuration
----------------------------

- Main menu -> Events -> Choose exising or add new event

- In "Tickets" tab add tickets, if none exists

- In questions tab:

  * add generic questions like name, email

  * add question with type "Selection" and "Is accomodation" checked.

  * Press "Generate shuttle tickets" button

- Save

- Main menu -> Events -> Configuration -> Settings

- In "Shop - Combo Tickets" block set "Accomodation Category" value

Accomodation - usage
--------------------

- Go to `/events`

- Click on "Register" button in event, that was used in configuration above,
  choose one ticket with "Navigate to accomodation" enabled

- Fill in answers to questions

- Click on "Go to payment"

- Click "Checkout"

- RESULT: in payment page you will see "Choose accomodation" instead of payment button

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
