# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from datetime import timedelta

from openerp import api, fields, models
from openerp.addons.connector.session import ConnectorSession


class ConnectorQueueGarbageCollector(models.TransientModel):
    """Fix jobs that are in a bad state"""
    _name = "connector.queue.garbage.collector"

    @api.model
    def requeue_stuck_jobs(self, in_queue_delta=5, started_delta=180):
        """Fix jobs that are in a bad states
        :param in_queue_delta: lookup time in minutes for jobs
                                that are in enqueued state

        :param started_delta: lookup time in minutes for jobs
                                that are in enqueued state
        """
        self.treat(
            self.get_stuck_jobs_to_requeue(
                in_queue_delta=in_queue_delta,
                started_delta=started_delta
            )
        )
        jobs = self.get_stuck_jobs_to_requeue(
            in_queue_delta=in_queue_delta,
            started_delta=started_delta
        )
        for job in jobs:
            job.requeue()
        return True

    @api.multi
    def get_stuck_jobs_to_requeue(self, in_queue_delta, started_delta):
        job_model = self.env['queue.job']
        now = fields.datetime.now()
        queue_dl = now - timedelta(minutes=in_queue_delta)
        started_dl = now - timedelta(minutes=started_delta)
        stuck_jobs = job_model.search(
            [('date_enqueued', '<=', fields.Datetime.to_string(queue_dl)),
             ('state', '=', 'enqueued')]
        )
        stuck_jobs += job_model.search(
            [('date_started', '<=', fields.Datetime.to_string(started_dl)),
             ('state', '=', 'started')]
        )
        return stuck_jobs
