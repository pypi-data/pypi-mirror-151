# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_tsegsearch']

package_data = \
{'': ['*'], 'sphinx_tsegsearch': ['static/*', 'templates/*']}

modules = \
['tiny_segmenter', 'search']
install_requires = \
['install_requires', 'install_requires']

setup_kwargs = {
    'name': 'sphinx-tsegsearch',
    'version': '1.1.1',
    'description': 'Sphinx extension to split searchword with TinySegmenter',
    'long_description': "sphinx-tsegsearch\n===================\n\nA Sphinx extension for tokenize japanese query word with TinySegmenter.js\n\nThis extension tweaks searchtools.js of sphinx-generated html document\nto tokenize Japanese composite words.\n\nSince Japanese is an agglutinative language, query word for document search\nusually becomes composite form like 'システム標準' (system standard).\nThis makes difficult to search pages containing phrase such as\n'システムの標準', '標準システム', because TinySegmenter.py (Sphinx's default\nJapanese index tokenizer) tokenizes 'システム' and '標準' as indexes.\n\nsphinx-tsegsearch patches searchtools.js to override query tokinization\nstep so that query input is re-tokenized by TinySegmenter.js (original\nJavaScript implementation of TinySegmenter).\nAs a result, roughly say, this tiny hack improves recall of Japanese\ndocument search in exchange of precision.\n\nUsage:\n\n#. Add 'sphinx_tsegsearch' in conf.extensions\n#. Rebuild document.\n",
    'author': 'Yasushi Masuda',
    'author_email': 'whosaysni@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whosaysni/sphinx-tsegsearch/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
