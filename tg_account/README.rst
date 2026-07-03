==============================================
 Invoicing modifications for Tribal Gathering
==============================================

* Removes "Recipient Bank" from invoice report template
* Allows to duplicate the invoice(s) by linking them to another company according
  to predefined mappings
* In company form adds option to show/hide fiscal related columns in invoice list like
  "Numero Fiscal" and "Factura Electronica"


Duplicate to fiscal invoice
---------------------------

- Login as admin
- Enable the developers mode
- Go to Settings -> Users -> Groups menu
- Search for "Show Full Accounting Features" and open record
- Add admin user to this group
- Go to Settings -> Users -> Groups menu
- Search for "Multi Companies" and open record
- Add admin user to this group

- Open any company form (in Settings -> Users -> Company menu). Let's call it
  "Company 1"
- In the company form set a so-called fiscal company. For example "Company 2"
- In the "Fiscal Company Mappings" tab add mappings for:

  - Journals
  - Accounts
  - Taxes
  - Payment Terms

- Save

- In the company switcher choose "Company 1" and add tick on "Company 2"
- Open or create any customer invoice that is related to "Company 1"
- Make sure, that there are some products/services in "Invoice lines"
- Click on Actions -> "Duplicate to fiscal invoice"
- RESULT: The invoice related to the "Company 2" is created according to the mappings

- Open or create other invoice that is related to "Company 1"
- Make sure, that there are some products/services in "Invoice lines"
- Go back to list of invoices

- Select 2 invoices: that one, that already has duplicated invoice and that one, that does not
- Click on Actions -> "Duplicate to fiscal invoice"

- RESULT: Dialog will appear:
- RESULT: first invoice appears in "Already duplicated" table

- Click on "Ignore and duplicate others"
- RESULT: duplicated invoice will created

Credits
=======

Contributors
------------

* `Eugene Molotov <https://github.com/em230418>`__
* `Ilmir Karamov <https://github.com/ilmir-k>`__

Sponsors
--------

* `Tribal Gathering <https://www.tribalgathering.com/>`__

Maintainers
-----------

* `IT-Projects LLC <https://it-projects.info>`__
