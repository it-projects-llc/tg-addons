==============================================
 Invoicing modifications for Tribal Gathering
==============================================

* Removes "Recipient Bank" from invoice report template

Duplicate to fiscal invoice
---------------------------

- Login as admin
- Enable developers mode
- Settings -> Users -> Groups
- Search for "Show Full Accounting Features" and open record
- Add admin user to this group
- Settings -> Users -> Groups
- Search for "Multi Companies" and open record
- Add admin user to this group

- Open any company form (Settings -> Users -> Company). Let is be "Company 1"
- In company form set fiscal company. For example "Company 2"
- In "Fiscal Company Mappings" add mappings
- Save

- In company switcher choose "Company 1" and add tick on "Company 2"
- Open or create any customer invoice, that is related to "Company 1"
- Make sure, that there are some products/services in "Invoice lines"
- Actions -> "Duplicate to fiscal invoice"
- RESULT: invoice related to "Company 2" is created

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
