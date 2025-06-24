=====================================
 Split payments for Online ticketing
=====================================

Configuration
-------------

- Main menu -> Website -> Configuration -> Settings

- Go to "Shop - Split Payment" section

- Change following settings for your needs

  * Minimum advance payment (%)

  * Maximum advance payment (%)

  * Maximum number of installments

Usage
-----

- Go to `/event`, choose non-free ticket

- Fill in attendee data

- Navigate to payment page

- Click on 'Split payment'

- In first popup input

  * Initial payment

  * How many payments

  * Period

- Click 'Generate invoice plan'

- On new popup review invoice plan

- Click 'Confirm'

- RESULT: you will be navigated to portal invoice page. Invoice amount equals to given deposit value in first popup

- RESULT: quotation is not confirmed yet

- In portal invoice page pay the invoice

- RESULT: quotation is confirmed

- RESULT: attendee record is confirmed, field "Is fully paid" equals to false

- RESULT: invoices with other installments are created

- Pay all other invoices

- RESULT: in attendee record field "Is fully paid" equals to true

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
