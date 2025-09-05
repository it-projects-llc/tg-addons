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

  * Minimum advance payment (absolute)

Minimum advance payment (absolute) setting
------------------------------------------

- If in shop total payment amount is less then value of this setting,
  then "Split payments" button won't be shown.

- In split payments popup deposit value should comply with value of this setting


Max tier price
--------------

When splitting payments, original ticket price can be replaced to "max tier price".

For example we have ticket with price 70 and max tier price 100.
Customer wants to buy 1 ticket and chooses split payments.
In this case full payment will be 100 instead of 70.
Additional price will be 30.

To set max tier price:

- Main menu -> Event -> open any event

- In tickets section you can set "Max tier price" for ticket

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

- On new popup review invoice plan and additional fee

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
