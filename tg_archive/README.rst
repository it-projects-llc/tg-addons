====================================
 Archive Tools for Tribal Gathering
====================================

* Adds "Attachment archive" link to following models:

  * account.invoice
  * account.voucher

Also this module includes shell scripts, that should be executed,
when it is required to move attachments to external service.

move_attachment usage
---------------------

* Grab ``GOOGLE_APPLICATION_CREDENTIALS``, ``COMPANY_FOLDER_ID`` for company

* Run odoo shell with environment values

.. code-block:: sh

   GOOGLE_APPLICATION_CREDENTIALS=xxx COMPANY_FOLDER_ID=yyy odoo-bin shell

* In python shell run this. As example we move invoices and bills attachments from company with id 3 and until 2024-06-30

.. code-block:: python

   from odoo.addons.tg_archive.tools.move_attachments import move_attachments
   move_attachments(env, 3, '2024-06-30')

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
