.. highlight:: shell-session

Examples
========

Ligo-raven has a number of functions that can be called directly to perform searches or calculate joint ranking statistics. This will typically involve importing both functions from ligo-raven and gracedb-sdk:

>>> from ligo.raven import gracedb_events, search
>>> from gracedb_sdk import Client

Next we can specify the specific GraceDB instance you want to interact with:

>>> gracedb = Client('https://gracedb.ligo.org/api/')

+----------------+------------------------------------------+
| GraceDB server | URL                                      |
+================+==========================================+
| Production     | https://gracedb.ligo.org/api/            |
+----------------+------------------------------------------+
| Playground     | https://gracedb-playground.ligo.org/api/ |
+----------------+------------------------------------------+
| Test           | https://gracedb-test.ligo.org/api/       |
+----------------+------------------------------------------+

As a another reminder, remember to have an updated certificate to interact with GraceDB and run on your terminal::

    $ ligo-proxy-init albert.einstein

Performing searches
-------------------

There are two functions that can be used to perform searches:

    * :meth:`ligo.raven.search.query`
    * :meth:`ligo.raven.search.search`

where :meth:`query` returns any matching events found while :meth:`search` does this while also writing a log message to each event's GraceDB page.

Query
^^^^^

We can specify our parameters prior to running :meth:`query`:

>>> gpstime = 1240215503.01
>>> tl, th = -5, 1
>>> group = 'CBC'     # 'CBC', 'Burst', or 'Test'
>>> pipelines = []    # 'Fermi', 'Swift', 'INTEGRAL', 'AGILE', or 'SNEWS'
>>> searches = []     # 'GRB', 'SubGRB', 'SubGRBTargeted', or 'MDC'
>>> se_searches = []  # 'AllSky', 'BBH', 'IMBH', or 'MDC'
>>> results = search.query('Superevent', gpstime, tl, th, gracedb=gracedb,
>>>                        group=group, pipelines=pipelines,
>>>                        searches=searches, se_searches=se_searches)
>>> print(results['superevent_id'])
'S190425z'

See documentation on `GraceDB models`_ for all choices of parameters and examples of event dictionaries. Also note that there is a command line version of this function::

    $ raven_query -e Superevent -t 1240215503.01 -w -5 1 -g CBC

Search
^^^^^^

We can run :meth:`search` similarly by providing parameters of the event we are searching around:

>>> graceid = 'S190519ag'
>>> tl, th = -60, 600
>>> pipelines = ['Fermi']
>>> searches = ['GRB']
>>> se_searches = []
>>> results = search.search(graceid, tl, th, gracedb=gracedb,
>>>                         group=group, pipelines=pipelines,
>>>                         searches=searches, se_searches=se_searches)
>>> print(results['graceid'])
'E333396'

Again there is a command line version of this function::

    $ raven_search -i graceid -w -60 600 -p Fermi -s GRB

.. warning:: Be careful of using the :meth:`search` function on the prodution instance of GraceDB (https://gracedb.ligo.org/api/) since it will upload log messages to GraceDB. If you are just performing an offline search then use :meth:`query` instead.

.. _`GraceDB models`: https://gracedb.ligo.org/documentation/models.html#what-characterizes-an-event

Calculating joint FARs
----------------------

There are also two functions that calculate a joint candidate's FAR:

    * :meth:`ligo.raven.search.coinc_far`
    * :meth:`ligo.raven.search.calc_signif_gracedb`

where :meth:`coinc_far` returns the joint FAR while :meth:`calc_signif_gracedb` does this while also writing a log message to each event's GraceDB page. These functions are otherwise completely identical, so we will only show an example with :meth:`coinc_far`.

Coinc_far
^^^^^^^^^

We can calculate the temporal joint far by:

>>> se_id = 'S200202ar'
>>> ext_id = 'E362082'
>>> tl, th = -60, 600
>>> result = coinc_far(se_id, ext_id, tl, th, grb_search='GRB',
>>>                    incl_sky=False, gracedb=gracedb)
>>> print(result)
{'temporal_coinc_far': 6.015243892694064e-09,
 'spatiotemporal_coinc_far': None,
 'skymap_overlap': None,
 'preferred_event': 'G362081',
 'external_event': 'E362082'}

We can include sky map information by specifying sky map filenames and by setting `incl_sky` to True:

>>> se_fitsfile = 'cWB.fits.gz'
>>> ext_fitsfile = 'fermi_skymap.fits.gz'
>>> incl_sky = True
>>> result = coinc_far(se_id, ext_id, tl, th, grb_search='GRB',
>>>                    se_fitsfile=se_fitsfile, ext_fitsfile=ext_fitsfile,
>>>                    incl_sky=incl_sky, gracedb=gracedb)
>>> print(result)
{'temporal_coinc_far': 6.015243892694064e-09,
 'spatiotemporal_coinc_far': 4.6630916924509334e-09,
 'skymap_overlap': 1.2899690354431859,
 'preferred_event': 'G362081',
 'external_event': 'E362082'}

There are additional other options for use offline. For instance, we can use a different rate for external triggers compared to the default by passing `em_rate`:

>>> em_rate = 1e-6
>>> result = coinc_far(se_id, ext_id, tl, th, grb_search='GRB',
>>>                    em_rate=em_rate,
>>>                    se_fitsfile=se_fitsfile, ext_fitsfile=ext_fitsfile,
>>>                    incl_sky=incl_sky, gracedb=gracedb)
>>> print(result)
{'temporal_coinc_far': 6.1192494e-10,
 'spatiotemporal_coinc_far': 4.743718052036537e-10,
 'skymap_overlap': 1.2899690354431859,
 'preferred_event': 'G362081',
 'external_event': 'E362082'}

There is also a command line version::

    $ raven_coinc_far -s S200202ar -e E362082 -w -60 600

.. warning:: Be careful of using the :meth:`calc_signif_gracedb` function on the prodution instance of GraceDB (https://gracedb.ligo.org/api/) since it will upload log messages to GraceDB. If you are just performing an offline search then use :meth:`coinc_far` instead.

Calculating association statistics
----------------------------------

Finally, there are two functions to assess whether two candidates are associated:

    * :meth:`ligo.raven.search.skymap_overlap_integral`
    * :meth:`ligo.raven.search.odds_ratio`

where :meth:`skymap_overlap_integral` compares how much two sky maps overlap similar to a Bayes factor while :meth:`odds_ratio` compares whether two events are coincidence versus being uncorrelated.

Skymap_overlap_integral
^^^^^^^^^^^^^^^^^^^^^^^

The overlap between two sky maps can be computed after loading them:

>>> from ligo.skymap.io import read_sky_map
>>> gw_skymap, h = read_sky_map('bayestar.fits.gz')
>>> grb_skymap, h = read_sky_map('gbuts_healpix_systematic.fit')
>>> result = search.skymap_overlap_integral(gw_skymap, grb_skymap)
>>> print(result)
32.28672531038014

We can also use multi-ordered (MOC) sky maps by passing the UNIQ ordering:

>>> gw_skymap_moc = read_sky_map('bayestar.multiorder.fits', moc=True)
>>> grb_skymap_moc = read_sky_map('gbuts_healpix_systematic.multiorder.fits',
>>>                               moc=True)
>>> result = search.skymap_overlap_integral(gw_skymap_moc['PROBDENSITY'],
>>>                                         grb_skymap_moc['PROBDENSITY'],
>>>                                         se_uniq=gw_skymap_moc['UNIQ'],
>>>                                         ext_uniq=grb_skymap_moc['UNIQ'])
>>> print(result)
32.286582585154505

There is also a command line version::

    $ raven_skymap_overlap -i bayestar.fits.gz gbuts_healpix_systematic.fit

Odds_ratio
^^^^^^^^^^

The odds ratio can be computed for GW170817-GRB 170817A by:

>>> from astropy import units as u
>>> skymap_overlap = 32.28672531038014
>>> tl, th = -1, 5
>>> bayes_gw = 0
>>> bayes_grb = 0
>>> r_c = .14 / u.yr
>>> r_gw = .8 / u.yr
>>> r_grb = 40 / u.yr
>>> r_n_gw = 1 / u.hr
>>> r_n_grb = 0 / u.s
>>> result = search.odds_ratio(skymap_overlap, tl, th
>>>                            bayes_gw=bayes_gw, bayes_grb=bayes_grb,
>>>                            r_c=r_c, r_gw=r_gw, r_grb=r_grb,
>>>                            r_n_gw=r_n_gw, r_n_grb=r_n_grb)
>>> print(result.value)
869806.35

using rates for O2 from `Howell et al.`_ Note that the default rates are for O4.

.. _`Howell et al.`: https://arxiv.org/abs/1811.09168 
