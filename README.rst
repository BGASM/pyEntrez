Welcome to pyEntrez
===================
|CodeFactor| |MIT| |python| |fix| |Feature|



Purpose
-------
**pyEntrez** aims to be a user-friendly suite of Biopython’s Entrez
tools that may be accessed from either the commandline in a script/arg
function, or from a persistent Text User Interface (TUI). The current
implementation will extend to the full use of Entrez for publication
browsing, and will offer features to automatically send query results to
a database of the user’s choice as well as facilitate database
manipulation.

Planned features include data interpretation with toolsets such as
Pandas. As well as incorporating text analysis and machine learning to
flag abstracts that are pertinent to the research conducted by the user.

Unplanned, but interesting, features would be to incorporate the rest of
the tools offered by Biopython in a one-stop shop.

The current implementation has been developed in Python 3 Win10 but
should work with Linux based OS (maybe with minor modifications in terms
of printing and error handling.)

Motivation
----------

As a novice programmer in the medical science realm, I wanted to see if I could implement a suite of tools that could pull all of the Entrez functionality together under one  script, as well as manipulate the data pulled. I envision this script allowing for a much more rapid acquisition of relevant data for systemic reviews and meta-analysis, which is a process limited by the amount of research assistants and hours available to scrape and read abstracts.


API Reference
-------------
`Read the Docs`_

.. _Read the Docs: https://pyentrez.readthedocs.io/en/main/index.html

Credits
-------

Powered by:

`pyCUI Python Command Line UI library`_

.. _pyCUI Python Command Line UI library: https://github.com/jwlodek/py_cui 



`Biopython library`_

.. _Biopython library: https://github.com/biopython/biopython 


License
-------

MIT © William Slattery 2020

 

.. |MIT| image:: https://img.shields.io/github/license/BGASM/pyentrez?style=plastic

.. |CodeFactor| image:: https://www.codefactor.io/repository/github/bgasm/pyentrez/badge?style=plastic
   :target: https://www.codefactor.io/repository/github/bgasm/pyentrez

.. |python| image:: https://img.shields.io/badge/Made%20with-Python-brightgreen?style=plastic
   :target: https://www.python.org/   

.. |fix| image::  https://img.shields.io/github/issues/BGASM/pyEntrez/fix?color=purple&style=plastic
   :target: https://github.com/BGASM/pyEntrez/issues?q=is%3Aopen+is%3Aissue+label%3Afix

.. |Feature| image:: https://img.shields.io/github/issues/BGASM/pyEntrez/Feature?color=green&style=plastic
   :target: https://github.com/BGASM/pyEntrez/issues?q=is%3Aopen+is%3Aissue+label%3AFeature