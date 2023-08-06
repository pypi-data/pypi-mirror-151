# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fuzzy_graph_coloring']
install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'networkx>=2.6.3,<3.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pygad>=2.16.3,<3.0.0']

setup_kwargs = {
    'name': 'fuzzy-graph-coloring',
    'version': '0.1.3',
    'description': 'fuzzy-graph-coloring is a Python package for calculating the fuzzy chromatic number and coloring of a graph with fuzzy edges.',
    'long_description': 'fuzzy-graph-coloring\n********************\n\nfuzzy-graph-coloring is a Python package for calculating\nthe fuzzy chromatic number and coloring of a graph with fuzzy edges.\nIt will create a coloring with a minimal amount of incompatible edges\nusing a genetic algorithm (:code:`genetic_fuzzy_color`) or a greedy-k-coloring (:code:`greedy_k_color`)\ncombined with a binary search (:code:`alpha_fuzzy_color`).\n\nIf you don\'t know which one to use, we recommend :code:`alpha_fuzzy_color`.\nIf you are looking for a networkX coloring but with a given k, use :code:`greedy_k_color`.\n\nSee repository https://github.com/ferdinand-dhbw/fuzzy-graph-coloring\nSee the paper that accompanied the project https://github.com/ferdinand-dhbw/fuzzy-graph-coloring/blob/main/docs/KoenigRheinerFGCStudentResearchProject2022.pdf\n\nQuick-Start\n===========\nInstall package: :code:`pip install fuzzy-graph-coloring`\nConsider the following graph:\n\n.. image:: https://raw.githubusercontent.com/ferdinand-dhbw/fuzzy-graph-coloring/main/docs/images/uncolored-graph.png\n   :width: 500\n\nTry simple code:\n\n.. code-block::\n\n   import fuzzy-graph-coloring as fgc\n\n   TG2 = nx.Graph()\n   TG2.add_edge(1, 2, weight=0.4)\n   TG2.add_edge(1, 3, weight=0.7)\n   TG2.add_edge(1, 4, weight=0.8)\n   TG2.add_edge(2, 4, weight=0.2)\n   TG2.add_edge(2, 5, weight=0.9)\n   TG2.add_edge(3, 4, weight=0.3)\n   TG2.add_edge(3, 6, weight=1.0)\n   TG2.add_edge(4, 5, weight=0.3)\n   TG2.add_edge(4, 6, weight=0.5)\n   TG2.add_edge(5, 6, weight=0.7)\n   TG2.add_edge(5, 7, weight=0.8)\n   TG2.add_edge(5, 8, weight=0.5)\n   TG2.add_edge(6, 7, weight=0.7)\n   TG2.add_edge(7, 8, weight=0.6)\n\n   print(fgc.alpha_fuzzy_color(TG2, 3, return_alpha=True, fair=True))\n\nResult: :code:`{5: 0, 6: 1, 1: 2, 7: 2, 2: 1, 3: 0, 4: 0, 8: 1} 0.9285714285714286 0.4`\n\n(Tuple of coloring, score [(1-DTI)], and alpha [of alpha-cut])\n\n.. image:: https://raw.githubusercontent.com/ferdinand-dhbw/fuzzy-graph-coloring/main/docs/images/colored-graph.png\n   :width: 500\n\nBibliography\n============\nThe project uses a lot of the by Keshavarz created basics:\nE. Keshavarz, "Vertex-coloring of fuzzy graphs: A new approach," Journal of Intelligent & Fuzzy Systems, vol. 30, pp. 883-893, 2016, issn: 1875-8967. https://doi.org/10.3233/IFS-151810\n\nLicense\n=======\nThis project is licensed under GNU General Public License v3.0 (GNU GPLv3). See :code:`LICENSE` in the code repository.\n\n\nSetup development environment\n=============================\n1. Get poetry https://python-poetry.org/docs/\n2. Make sure, Python 3.8 is being used\n3. :code:`poetry install` in your system shell\n4. :code:`poetry run pre-commit install`\n\nRun pre-commit\n--------------\n:code:`poetry run pre-commit run --all-files`\n\nRun pytest\n----------\n:code:`poetry run pytest .\\tests`\n\nCreate documentation\n--------------------\n:code:`.\\docs\\make html`\n',
    'author': 'Ferdinand Koenig and Jonas Rheiner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ferdinand-dhbw/fuzzy-graph-coloring',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
