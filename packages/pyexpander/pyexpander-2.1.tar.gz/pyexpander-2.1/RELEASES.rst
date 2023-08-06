Release 1.9.1
-------------

Date: 2019-12-19

(Changes with respect to relase 1.9)

Bugfixes
++++++++

- Small fixes in the documentation.
- Bitbucket source repository is now deprecated
- In administration_tools README was renamed to README.rst

Release 1.9.2
-------------

Date: 2020-02-27

Internal changes
++++++++++++++++

- Administration scripts for the source repository at bitbucket were removed.
- Use https sourceforge URL.
- Package building now uses podman instead of docker.

Bugfixes
++++++++

- The test Makefile didn't always use the correct python version.
- The parser didn't accept all valid python string literals.
- Python2 scripts now call the python2 interpreter in their first line.
- administration_tools/show-version.sh now calls the correct python interpreter
  explicitly.

Release 1.10
------------

Date: 2020-04-02

Internal changes
++++++++++++++++

- Some pylint fixes in python3/pyexpander/lib.py.
- Small docstring changes in python3/pyexpander/lib.py to remove warnings when
  documentation is built.
- Package generation with docker was improved.
- Some improvements in setup.py and README.

Bugfixes
++++++++

- Print the filename when parseFile() raises an exception.

Documentation
+++++++++++++

- Use ReadTheDocs theme for documentation.

New/Changed functions
+++++++++++++++++++++

- Support of encodings for input and output was added.

Release 1.10.1
--------------

Date: 2020-04-03

Bugfixes
++++++++

- Small documentation fixes.

Release 1.10.2
--------------

Date: 2020-04-03

Documentation
+++++++++++++

- Improvements in the source code documentation.
- More improvements in the documentation.

Release 2.0
-----------

Date: 2021-06-02

Bugfixes
++++++++

- Fixed some tests regarding exceptions which didn't always work.

Internal changes
++++++++++++++++

- Scripts to generate debian and rpm packages with docker/podman were
  reorganized and improved. They are now similar to the scripts in
  StructuredData and sumo, two other of my projects.
- a RELEASES.rst file now documents changes between releases of pyexpander.

Major Changes
+++++++++++++

- Python 2 support was removed. This is a major change since all pyexpander
  statements now must be written in python 3 syntax. Pyexpander scripts that
  used python 2 before may have to be adapted.

Release 2.1
-----------

Date: 2022-05-19

Internal changes
++++++++++++++++

- Pylint warnings were removed at various places in the code.
- SETENV.sh and SETENV.bat enable to run pyexpander directly without install.
- An optimization for reading from stdin makes expander.py a bit shorter.
- Package building: removed fedora-32, fedora-33, added fedora-35.

Documentation
+++++++++++++

- Some documentation bugfixes
- Small update of administration_tools/README.rst.

Bugfixes
++++++++

- On windows the lineseparator was wrong, causing errors in some cases.
- Some exceptions were malformed.
- A missing include file now generates a better error message.

Major Changes
+++++++++++++

- Recursive macros are now fully supported.
- Spaces after a command and before the opening bracket are now allowed.
- Option 'expander.py --dump' prints the python list of strings.
- Variable '__file__' now always contains the current filename.
- File dependencies for "make" can now be created with "expander.py --deps".

