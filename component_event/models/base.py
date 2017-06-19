# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

"""
Base Model
==========

Extend the 'base' Odoo Model to add Events related features.


"""

from odoo import api, models
from ..components.event import CollectedEvents
from ..core import EventWorkContext


class Base(models.AbstractModel):
    """ The base model, which is implicitly inherited by all models.

    Add an :meth:`_event` method to all Models. This method allows to
    trigger events.

    It also notifies the following events:

    * ``on_record_create``
    * ``on_record_multi``
    * ``on_record_unlink``


    """
    _inherit = 'base'

    def _event(self, name, model_name=None, collection=None,
               components_registry=None):
        """ Collect events for notifications

        Usage::

            @api.multi
            def button_do_something(self):
                for record in self:
                    # do something
                    self._event('on_do_something').notify('something')

        With this line, every listener having a ``on_do_something`` method
        with be called and receive 'something' as argument.

        See: :mod:`..components.event`

        :param name: name of the event, start with 'on_'
        :type model_name: str | unicode
        :param collection: optional collection  to filter on, only
                           listeners with similar ``_collection`` will be
                           notified
        :type model_name: :class:`odoo.models.BaseModel`
        :param components_registry: component registry for lookups,
                                    mainly used for tests
        :type components_registry:
            :class:`odoo.addons.components.core.ComponentRegistry`


        """
        if not self.env.registry.ready:
            # no event should be triggered before the registry has been loaded
            return CollectedEvents([])
        model_name = self._name
        if collection is not None:
            work = EventWorkContext(collection=collection,
                                    model_name=model_name,
                                    components_registry=components_registry)
        else:
            work = EventWorkContext(env=self.env, model_name=model_name,
                                    components_registry=components_registry)

        collecter = work._component_class_by_name('base.event.collecter')(work)
        return collecter.collect_events(name)

    @api.model
    def create(self, vals):
        record = super(Base, self).create(vals)
        self._event('on_record_create').notify(record, fields=vals.keys())
        return record

    @api.multi
    def write(self, vals):
        result = super(Base, self).write(vals)
        fields = vals.keys()
        for record in self:
            self._event('on_record_write').notify(record, fields=fields)
        return result

    @api.multi
    def unlink(self):
        result = super(Base, self).unlink()
        for record in self:
            self._event('on_record_unlink').notify(record)
        return result
