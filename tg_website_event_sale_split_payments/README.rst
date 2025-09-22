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

  * Security days

  * Last installment date

Minimum advance payment (absolute) setting
------------------------------------------

- If total payment amount is less than the value of this setting in the shop cart,
  then "Flexipay" button won't be shown.

- In Split payments popup deposit value should comply with value of this setting

Max installment date
--------------------

When customer decides to split payments, in order to limit max number of installments
the module makes sure that max installment date does not exceed the following values:

- "Last installment date" from settings minus security days

- start date of event in cart minus security days

- start date of rental start minus security days

"Flexipay" button visibility in payment page
--------------------------------------------

"Flexipay" button is not visible if one of the conditions is true:

- Total payment amount of cart is less than value of "Minimum advance payment (absolute)"

- Max installment date does not exceed 2 weeks

Max tier price
--------------

When splitting the payments, original ticket price can be replaced to "max tier price".

For example, we have ticket with the price 70 and max tier price 100.
Customer wants to buy 1 ticket and chooses split payments option.
In this case the full payment will be 100 instead of 70.
Additional price will be 30.

To set max tier price:

- Go to Main menu -> Event -> open any event

- In the Tickets section you can set "Max tier price" for tickets

Invoice creation for downpayments
---------------------------------

Instead of downpayment's product income account, original product accounts are used in the invoice lines.

If sale order has products with different accounts, then the lines are created for every account in downpayment invoices.

Usage
-----

- Go to `/event`, choose a non-free ticket

- Fill in the attendee data

- Navigate to payment page

- Click on 'Flexipay'

- In the first popup input

  * Initial payment

  * How many payments

  * Period

- Click 'Generate invoice plan'

- On the new popup review invoice plan and additional fee

- Click 'Confirm'

- RESULT: you will be navigated to portal invoice page. Invoice amount equals to given deposit value in the first popup

- RESULT: quotation is not confirmed yet

- In the portal invoice page pay the invoice

- RESULT: quotation is confirmed

- RESULT: attendee record is confirmed, field "Is fully paid" equals to false

- RESULT: invoices with other installments are created

- Pay all other invoices

- RESULT: in the attendee record field "Is fully paid" equals to true

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
