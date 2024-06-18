# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import django

sys.path.insert(0, os.path.abspath('../../BlogStudentsBUT'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'BlogStudentsBUT.settings'

django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = 'WWW.BLOGBUT.PL'
copyright = 'Politechnika Bialostocka 2024'
author = 'Maksim Vasiukhnevich, Aliaksei Tutski'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

tml_theme = 'sphinx_book_theme'h
html_static_path = ['_static']
