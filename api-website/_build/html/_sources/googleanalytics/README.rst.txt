.. -*- restructuredtext -*-

===========================================
Google Analytics extension for Sphinx
===========================================

:author: Domen Kožar <domen@dev.si>


About
=====

This extensions allows you to track generated html files
with Google Analytics web service.


Installing from sphinx-contrib checkout
---------------------------------------

Checkout googleanalytics sphinx extension::

  $ git clone https://github.com/sphinx-contrib/googleanalytics

Change into the googleanalytics directory::

  $ cd googleanalytics

Install the module::

  $ python setup.py install


Enabling the extension in Sphinx_
---------------------------------

Just add ``sphinxcontrib.googleanalytics`` to the list of extensions in the ``conf.py``
file. For example::

    extensions = ['sphinxcontrib.googleanalytics']


Configuration
-------------

For now one optional configuration is added to Sphinx_. It can be set in
``conf.py`` file:

``googleanalytics_id`` <string>:
	UA id for your site, example::
		googleanalytics_id = 'UA-123-123-123'

``googleanalytics_enabled`` <bool>:
	True by default, use it to turn off tracking.


.. Links:
.. _gnuplot: http://www.gnuplot.info/
.. _Sphinx: http://sphinx.pocoo.org/

