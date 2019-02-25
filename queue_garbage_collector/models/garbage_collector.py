# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from datetime import timedelta

from openerp import api, fields, models
from openerp.addons.connector.queue.job import job
from openerp.addons.connector.session import ConnectorSession


@job
def cron_checkup(session, model_name, in_queue_delta=5, started_delta=180):
    """Fix jobs that are in a bad states
    :param in_queue_delta: lookup time in minutes for jobs
                            that are in enqueued state

    :param started_delta: lookup time in minutes for jobs
                            that are in enqueued state
    """
    obj = session.env[model_name]
    obj.treat(
        obj.get_jobs_to_requeue(
            in_queue_delta=in_queue_delta,
            started_delta=started_delta
        )
    )
    return True


class ConnectorQueueGarbageCollector(models.TransientModel):
    """Fix jobs that are in a bad state"""
    _name = "connector.queue.garbage.collector"

    @api.model
    def set_cleanup_job(self):
        session = ConnectorSession.from_env(self.env)
        cron_checkup.delay(
            session,
            self._name,
        )

    @api.multi
    def get_jobs_to_requeue(self, in_queue_delta, started_delta):
        job_object = self.env['queue.job']
        now = fields.datetime.now()
        queue_dl = now - timedelta(minutes=in_queue_delta)
        started_dl = now - timedelta(minutes=started_delta)
        sick_jobs = job_object.search(
            [('date_enqueued', '<=', fields.Datetime.to_string(queue_dl)),
             ('state', '=', 'enqueued')]
        )
        sick_jobs += job_object.search(
            [('date_started', '<=', fields.Datetime.to_string(started_dl)),
             ('state', '=', 'started')]
        )
        return sick_jobs

    @api.multi
    def treat(self, jobs):
        self.requeue(jobs)

    @api.multi
    def requeue(self, jobs):
        for job_ in jobs:
            job_.requeue()
