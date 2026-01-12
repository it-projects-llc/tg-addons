===============
 Combo tickets
===============

Shuttle tickets - configuration
-------------------------------

- Go to Main menu -> Events -> Choose existing or add a new event

- In the "Tickets" tab add tickets, if none exist

- In the Questions tab:

  * add generic questions like name, email

  * add question with type "Selection" and "Is shuttle" checked.

    For this question add answers and corresponding tickets.

    If you already have prepared shuttle events with tickets, you can use "Generate shuttle tickets" button.

    After pressing the "Generate shuttle tickets" button, a wizard will open. Press "Add a line", and a new window will open, allowing you to select events to add to the Answers list.

    By checking the checkbox in the upper-left corner, you can select all events at once.

- Close question form

- Save

Shuttle tickets - usage
-----------------------

- Go to `/events`

- Click on "Get tickets" button in the event, that was used in the configuration above, then
  choose one ticket

- Fill in registration data and select a shuttle

- Pay for the registration for the event, if required

- RESULT: You will have at least 2 registrations.
  One is the event for which you have just registered.
  Second one is the shuttle event, that is used in the shuttle ticket question

Accommodation - configuration
-----------------------------

- Go to Main menu -> Events -> Choose existing or add a new event

- In the "Tickets" tab add tickets, if none exists

- In the Questions tab:

  * add generic questions like name, email

  * add question with the type "Selection" and the "Is Accommodation" checked.

    For this question add an answer and check the "Is Positive Accommodation Answer" checkbox.
    Pressing the "Generate Answers" button will automatically generate a single answer named "Yes" with a "Is Positive Accommdation Answer" checkbox already set.

- Set the price for the ticket

- Save

- Go to Main menu -> Events -> Configuration -> Settings

- In "Shop - Combo Tickets" section set the "Accommodation Category" value

Accommodation - usage
---------------------

- Go to `/events`

- Click on "Get tickets" button in the event, that was used in the configuration above, then
  choose one ticket with the question with the type "Selection" and "Is Accommodation" checked.

- Fill in answers to questions, in the question for accommodation, pick answer that was set as the "Is Positive Accommodation Answer".

- Click on "Go to payment"

- Click "Checkout"

- RESULT: in the payment page you will see "Choose accommodation" instead of the payment button.

  After the "Choose accommodation" button is pressed, you will be redirected to the shop page with a preselected category configured earlier in the "configuration" step.

  Once an accommodation product is added to the shopping cart, the order can be processed.

Credits
=======

Contributors
------------

* `Eugene Molotov <https://github.com/em230418>`__

* `Igor Makarenkov <https://github.com/SecretAgentNull>`__

Sponsors
--------

* `Tribal Gathering <https://www.tribalgathering.com/>`__

Maintainers
-----------

* `IT-Projects LLC <https://it-projects.info>`__
