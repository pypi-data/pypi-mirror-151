# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_xtdb']

package_data = \
{'': ['*']}

install_requires = \
['cytoolz>=0.11.2,<0.12.0',
 'edn-format>=0.7.5,<0.8.0',
 'pampy>=0.3.0,<0.4.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'py-xtdb',
    'version': '0.5.1',
    'description': 'Small functions for interacting with XTDB via requests http.',
    'long_description': '\n# Table of Contents\n\n1.  [py xtdb](#org7af26fd)\n    1.  [Install:](#org1b7708b)\n    2.  [Sample Usage:](#org951e586)\n    3.  [Try it out](#orgac23d56)\n    4.  [Why](#org6e949a7)\n\n\n<a id="org7af26fd"></a>\n\n# py xtdb\n\nSmall functions (and examples) for interacting with XTDB via requests http.\n\n<https://xtdb.com/docs/>\n\n\n<a id="org1b7708b"></a>\n\n## Install:\n\n    pip istall py-xtdb\n\nor\n\n    poetry add py-xtdb\n\n\n<a id="org951e586"></a>\n\n## Sample Usage:\n\n    q_results = query_edn(host="http://localhost:3001",\n                          data="""\n    {:query {:find [?id ?name ?address]\n             :keys [id name address]\n             :where [[?id :xt/id]\n                     [?id :name ?name]\n                     [?id :address ?address]]\n             :limit 2}}\n    \n        """)\n    \n    print(q_results)\n    \n    [{\'address\': \'4681 Billy Parkway Suite 747\\nNorth James, AR 25849\',\n      \'id\': 1,\n      \'name\': \'Mr. David Mills\'},\n     {\'address\': \'48596 Robert Walks\\nWest Angelview, CO 76011\',\n      \'id\': 2,\n      \'name\': \'Christopher Gregory\'}]\n\nIf you&rsquo;re looking to get query results into pandas fn \\`DataFrame\\` reads this\nsort of thing:\n\n    import pandas\n    \n    print(pandas.DataFrame(q_results))\n       id                 name                                            address\n    0   1      Mr. David Mills  4681 Billy Parkway Suite 747\\nNorth James, AR ...\n    1   2  Christopher Gregory       48596 Robert Walks\\nWest Angelview, CO 76011\n\n\n<a id="orgac23d56"></a>\n\n## Try it out\n\nIf you&rsquo;d like to try out xt and python you can clone this repo, install the\ndeps, start a local xt server, and walk through the jupyter notebooks in `/nb/`.\n\nHere&rsquo;s instructions/guidelines in more detail:\n\nFirst, clone this repo locally and change to said directory:\n\n    \n    git clone https://github.com/joefromct/py-xtdb\n    cd py-xtdb\n\nNow we need to start xtdb in a terminal so the jupyter notebook has something to\ntalk to.\n\nThe following command runs utilizing the \\`deps.edn\\` file which pulls in xt jars\nand runs with 2gb of memory.\n\n    # from same directory cloned above\n    clojure -X:xt\n\nYou&rsquo;ll see some metrics flash to the screen occasionally saying what XT is up\nto.  This is all setup with the file `xtdb.edn`.  You can see here that `xtdb.edn`\nspecifies `data` as the directory to store our database, and lucene full-text-search\nmodule(s).\n\nSo in summary, `deps.edn` pulls the dependencies you need, and `xtdb.edn`\nconfigures xt.\n\n-&#x2014;\n\nNext lets get a jupyterlab environment running.\n\nOpen another terminal to this same directory.\n\nHere, install python dependencies:\n\n    pip install -f requirements.txt\n\nor use poetry (picks up the pyproject.toml&#x2026; all same dir.)\n\n    poetry install\n\nNow we should hopefully have jupyterlab on our path. Start it up like so:\n\n    jupyter-lab nb/demo.ipynb\n\nFrom here you can step through the jupyter cells as per usual.\n\nHave a look [here](nb/demo.ipynb).\n\n\n<a id="org6e949a7"></a>\n\n## Why\n\nI&rsquo;m looking to make \\`xtdb\\` more accessible to a python-first team, primarily\nwith a focus on data science and/or data ingestion and document loading.\n\nSome shops prefer to process data in python, and ideally they would have a\ngentle pathway/introduction to xtdb.  This example has minimal clojure code, and\nall dependencies are driven just by `deps.edn` and `xtdb.edn`.\n\n',
    'author': 'joefromct',
    'author_email': 'joefromct@fastmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joefromct/py-xtdb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
