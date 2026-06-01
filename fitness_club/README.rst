=======================
Fitness Club Management
=======================

Module for fitness club automation: members, subscriptions, trainers,
group classes, attendance and reporting — all in one Odoo app.

Features
========

* **Members** with personal data (gender, birthday, age) linked to a
  standard ``res.partner`` contact.
* **Tariff plans** with duration and price (Trial week, Monthly,
  Yearly demo plans included).
* **Subscriptions** with auto-computed end date, state machine
  (Draft → Active → Expired) and manual cancellation.
* **Trainers** linked to ``res.users`` so they can log in and see
  only their own classes via record rules.
* **Classes** with capacity tracking, calendar / kanban scheduling
  and auto status transition to ``Done`` once finished.
* **Attendances** with unique-pair constraint (one member can attend
  the same class only once) and active-subscription check.
* **Wizards**: mass-renew subscription, attendance report.
* **PDF report**: Member card with active subscription and attendance
  history, colored statuses.
* **Security**: two-level groups (User → Administrator) under a single
  ``Fitness Club`` privilege; four record rules for members and
  classes.
* **i18n**: Ukrainian translation included.

Installation
============

#. Copy ``fitness_club`` into your Odoo addons directory.
#. Update the Apps list and install the module from **Apps**.

Usage
=====

After installation a new top-level menu **Fitness Club** appears with
sub-menus:

* **Members** — kanban grouped by subscription status, list and form.
* **Classes** — calendar (default), kanban, list and form.
* **Subscriptions** — list, form, graph and pivot.
* **Attendances** — list, form, pivot and graph.
* **Configuration** — Plans, Trainers (Admin only).

Main workflows
--------------

* **Register a member** — create a new contact (or pick an existing
  partner) on the Members form. Phone and email are automatically
  taken from the partner.
* **Sell a subscription** — open a member, click **New** in the
  *Subscriptions* tab, pick a plan and start date.
* **Mass renew** — select several members in the list view → Actions
  → **Mass renew subscription**.
* **Schedule a class** — go to Classes, switch to calendar view,
  click on a date and create a new class.
* **Mark attendance** — open the class form and add participants in
  the *Participants* tab.
* **Print a member card** — open a member and select Print → Member
  Card; supports printing several at once.

Configuration
-------------

* **Plans** (Configuration → Plans) define duration and price.
* **Trainers** (Configuration → Trainers) hold the staff list; if a
  trainer is linked to a ``System User``, they will log in and see
  only their own classes.

Author
======

* Anna Khoroshylova

License
=======

LGPL-3
