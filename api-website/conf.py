# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..')) #Source path


# -- Project information -----------------------------------------------------

project = 'SalesGPT'
copyright = '2024, Filip-Michalsky'
author = 'Filip-Michalsky'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              #"sphinxcontrib.googleanalytics",
              'sphinxcontrib.gtagjs'
]

#googleanalytics_id = "GTM-NX3SZD79"

gtagjs_ids = [
    'GTM-NX3SZD79',
]

GOOGLE_TAG_MANAGER_SNIPPET = """
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({
'gtm.start': new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-NX3SZD79');</script>
<!-- End Google Tag Manager -->
"""


# 2. Create a setup() function if you don't already have one.
#    (If you do, just add to your existing setup() function.)
def setup(app):
    # 3. Tell Sphinx to add your JS code. Sphinx will insert
    #    the `body` into the html inside a <script> tag:
    app.add_js_file(None, body=GOOGLE_TAG_MANAGER_SNIPPET)# Add any paths that contain templates here, relative to this directory.


templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    'custom.css',  # add your custom CSS file here
]