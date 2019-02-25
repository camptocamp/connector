.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Connector Jobs Sanity
======================

Fix jobs that are in a bad state

Configuration
=============

To configure this module, you need to:

Go to ir cron and setup cron named "Jobs Doctor".
You can add two parameter in args:
- A lookup delta in minutes for enqueued job (default 5)
- A lookup delta in minutes for started job   (default 180)

Usage
=====

To use this module, you need to:

#. Activate / Deactivate Jobs Doctor cron

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/102/9.0


Known issues / Roadmap
======================


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/{project_repo}/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Nicolas Bessi <nicolas.bessi@camptocamp.com>
* Mykhailo Panarin <m.panarin@mobilunity.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
