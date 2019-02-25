# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Connector Jobs Garbage Collector",
    "version": "9.0.1.0.0",
    "summary": """Fix jobs that are in a bad state""",
    "author": "Camptocamp SA, "
              "Odoo Community Association (OCA)",
    "category": "connector",
    "data": [
        "data/ir_cron.xml",
    ],
    "depends": [
        "connector",
    ],
    "website": "https://github.com/OCA/connector",
    "license": "AGPL-3",
    "installable": True,
}
