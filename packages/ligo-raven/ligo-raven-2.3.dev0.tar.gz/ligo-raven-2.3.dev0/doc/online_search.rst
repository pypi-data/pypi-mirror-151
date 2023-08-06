Online search
=============

Ligo-raven is currently used by `gwcelery`_ for online real-time analysis,
searching for coincidences between external events uploaded to GraceDB
via GCN and GW candidates represented by superevents.

This workflow is separated between the following tasks:

* `external_triggers.py`_
* `raven.py`_
* `external_skymaps.py`_

See the above links to documentation for further specific info.

Example online search
---------------------

This search can be broadly summarized to setting up a GCN listener
and triggering a coincidence search whenever a superevent or external event
is uploaded to GraceDB.

See this example `GCN listener`_ and the following GCN parser:

>>> from gwcelery.tasks import gcn, gracedb
>>> from lxml import etree
>>> # Put GCN listener handler before parser function
>>> gcn.handler(gcn.NoticeType.FERMI_GBM_FIN_POS)
>>> def handle_grb_gcn(payload):
>>>     """Handle GCN payload."""
>>>     # Process/filter GCN event
>>>     root = etree.fromstring(payload)
>>>     group = 'Test' if root.attrib['role'] == 'test' else 'External'
>>>     # Upload event
>>>     gracedb.create_event(filecontents=payload,
>>>                          pipeline='Fermi',
>>>                          search='GRB',
>>>                          group=group)

For `gwcelery`_, we use IGWN alert to trigger coincidence searches. See this
example `IGWN alert listener`_ and alert parser:

>>> from gwcelery.tasks import igwn_alert, raven
>>> # Put IGWN alert listener handler before parser function
>>> @igwn_alert.handler('superevent', 'external_fermi', shared=False)
>>> def handle_grb_igwn_alert(alert):
>>>     """Handle IGWN alert."""
>>>     # Determine GraceDB ID
>>>     graceid = alert['uid']
>>>     # launch searches for new events
>>>     if alert['alert_type'] == 'new':
>>>         if alert['object'].get('group') == 'External':
>>>             # launch separate CBC and Burst searches
>>>             raven.coincidence_search(graceid, alert['object'],
>>>                                      searches=['GRB'],
>>>                                      group='CBC')
>>>             raven.coincidence_search(graceid, alert['object'],
>>>                                      searches=['GRB'],
>>>                                      group='Burst')
>>>         elif 'S' in graceid:
>>>             # launch search based on group
>>>             group = alert['object'][''preferred_event_data']['group']
>>>             raven.coincidence_search(graceid, alert['object'],
>>>                                      searches=['GRB'],
>>>                                      group=group)

Responding to online alerts
---------------------------

If you plan to or are assigned to respond to real-time alerts during an
operating run, please familiarize yourself with the
`Follow-up Advocate Guide`_ and the operations of the Rapid Reponse Team
(RRT). This guide goes over the procedure with standard GW-only alerts and
will inform how to handle a coincident RAVEN alert.

When RAVEN finds a coincidence, the label **EM_COINC** is applied to both the
superevent and external event. The RRT will meet and a RAVEN expert is
expected to give insight to the event. A RAVEN expert is also expected to give
a recommendation about the event if it doesn't pass `publishing conditions`_,
indicated by the lack of a **RAVEN_ALERT** label. In that case, we should:

1. Check why the concidence didn't pass `publishing conditions`_.
   This may require uploading sky maps and calculating
   the joint FAR with sky map info if this didn't occur automatically or the
   external sky map isn't the latest.

2. If the external candidate is a sub-threshold GRB, you will need to contact
   the respective experiment leads to confirm whether this candidate is likely
   from a noise source or could be from an appropriate astrophysical source.

When RAVEN decides to automatically publish a coincidence, the label
**RAVEN_ALERT** is applied. At this point, we should confirm that the RAVEN
alert pipeline worked correctly:

1. Check that the **ADVREQ** and later the **GCN_PRELIM_SENT** labels have
   been applied, indicating that an alert has been triggered and sent.

2. Check the logs in the external coincidence for what RAVEN did
   and that these logs make sense.

3. Check that an external sky map has been uploaded, if applicable. Check
   whether the latest `coincidence_far.json` file contains a spatial FAR and
   a combined sky map has been made. If not, you may need to create or
   find the appropriate sky map and upload it to the external event with
   the label **EXT_SKYMAP_READY**.

4. Check that the latest VOEvent and circular text includes information about
   the coincidence. If not, an update alert may need to be issued to include
   this info using the `gwcelery dashboard`_.

.. warning:: Make sure you communicate properly with the RRT, both your opinions on a coicidence and any changes you may want to make.
             **Do not make changes to superevents or external events, create alerts, or send circulars without express permission from the RRT.**
             These alerts are monitored by the external astronomical community and mistakes could cost astronomers valuable resources and telescope time.

.. _`gwcelery`: https://igwn.readthedocs.io/projects/gwcelery/en/latest/
.. _`external_triggers.py`: https://igwn.readthedocs.io/projects/gwcelery/en/latest/gwcelery.tasks.external_triggers.html
.. _`raven.py`: https://igwn.readthedocs.io/projects/gwcelery/en/latest/gwcelery.tasks.raven.html
.. _`external_skymaps.py`: https://igwn.readthedocs.io/projects/gwcelery/en/latest/gwcelery.tasks.external_skymaps.html
.. _`GCN listener`: https://igwn.readthedocs.io/projects/gwcelery/en/latest/gwcelery.tasks.gcn.html
.. _`IGWN alert listener`: https://igwn.readthedocs.io/projects/gwcelery/en/latest/gwcelery.tasks.igwn_alert.html
.. _`Follow-up Advocate Guide`: https://emfollow.docs.ligo.org/followup-advocate-guide/
.. _`publishing conditions`: https://igwn.readthedocs.io/projects/gwcelery/en/latest/gwcelery.tasks.raven.html#gwcelery.tasks.raven.trigger_raven_alert
.. _`gwcelery dashboard`: https://emfollow.ligo.caltech.edu/gwcelery/
