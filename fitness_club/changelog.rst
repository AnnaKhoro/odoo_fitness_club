Changelog
=========

19.0.1.4.0
-----------------------
* i18n: Ukrainian translation (``i18n/uk.po``).
* Documentation: ``README.rst``, ``changelog.rst``, module description
  page (``static/description/index.html`` with banner image).
* Docstrings added to all classes and key methods.

19.0.1.3.0
----------
* Tests for every model (8 test cases): plan creation, member age,
  trainer class count, subscription dates / state, class state
  auto-transition, manual cancel, attendance uniqueness, mass-renew
  wizard.
* Class status auto-transitions to ``Done`` once the end datetime
  passes; manual ``Cancel`` override available.
* Extended demo data: 9 partners, 6 members, 3 trainers, 6
  subscriptions, 6 classes, 8 attendances.

19.0.1.2.0
----------
* Member card PDF report with colored statuses for visit history,
  active subscription block and attendance table; A4 paperformat,
  one member per page.
* Member and Trainer now link to ``res.partner`` (display name comes
  from the partner, contact data is shared).

19.0.1.1.0
----------
* Wizards: mass renew subscription (called from Members list);
  attendance report (called from Members or Trainers list/form).
* Views: kanban for Members (grouped by subscription status),
  calendar + kanban for Classes, pivot + graph for Attendances and
  Subscriptions; rich search views with filters and group-by.
* Inheritance of ``res.partner`` (fitness memberships block) and
  ``res.users`` (linked trainer profile).

19.0.1.0.0
----------
* Initial release.
* Six models: ``fitness.plan``, ``fitness.trainer``,
  ``fitness.member``, ``fitness.subscription``, ``fitness.class``,
  ``fitness.attendance``.
* Two-level security: ``Fitness Club / User`` and
  ``Fitness Club / Administrator`` under a single privilege; four
  record rules (members and classes scoped per group).
* Tariff plans loaded as master data; demo data for all models.
