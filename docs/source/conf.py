# -*- coding: utf-8 -*-
import os
import sys

# ЭТО САМОЕ ГЛАВНОЕ — правильные пути для Windows
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # корень проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))        # на всякий случай

project = 'Weather CLI'
copyright = '2025, Lexys'
author = 'Lexys'
release = '1.0'
language = 'ru'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

html_theme = 'sphinx_rtd_theme'
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_static_path = ['_static']