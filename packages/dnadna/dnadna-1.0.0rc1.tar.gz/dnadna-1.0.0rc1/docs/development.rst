Development
###########

Setup
=====

Getting the source
------------------

DNADNA currently has two repositories, the public instance at
https://gitlab.com/mlgenetics/dnadna, and a private repository (where its
development was started) at
https://gitlab.inria.fr/ml_genetics/private/dnadna.  For the time being, the
public repository is a read-only mirror of the "master" branch of the
private repository, and to submit merge requests to the project you will
need to request access to the private repository.

The DNADNA source code can be cloned from git, with use of SSH encouraged
for project members:

.. code-block:: console

    $ git clone git@gitlab.inria.fr:ml_genetics/private/dnadna.git

or

.. code-block:: console

    $ git clone https://gitlab.inria.fr/ml_genetics/private/dnadna.git


Conda environments
------------------

As DNADNA uses `PyTorch <https://pytorch.org/>`_ which is a non-trivial
dependency to install, the easiest way to install and do development on
DNADNA is to use a `Conda <https://docs.conda.io/en/latest/>`_ environment
as described in the `installation documentation
<https://pytorch.org/get-started/locally/>`_ for PyTorch itself.

To make this easy, if you already have the ``conda`` command installed
locally, two ``environment.yml`` files for conda have been included in the
root of the source tree:

* ``environment.yml`` - default conda environment for dnadna; installs PyTorch
  with full CUDA support. This is the same as ``environment-cuda.yml``.

* ``environment-cpu.yml`` - conda environment for dnadna with CPU-only PyTorch
  installation, for use on development machines without CUDA support.

These can be used like:

.. code-block:: console

    $ conda env create

By default this will create a conda environment named "dnadna" with all the
minimal runtime and development dependencies installed and ready for use.
You can override the environment name by providing the
``--name <environment-name>`` flag to ``conda env create``.  To activate the
environment, run:

.. code-block:: console

    $ conda activate dnadna

(or replace "dnadna" with your environment name).

This *does not* install the ``dnadna`` package itself.  To do this, run:

.. code-block:: console

    $ pip install -e .

to install the package in "editable" mode for development, or without the
``-e`` to install a static copy of the package into the environment if you do
not intend to edit it.

Updating to a new version
-------------------------

To update to the latest version of the code:

.. code-block:: console

    $ git checkout master
    $ git pull

(or if you want to update to the latest version of a different branch,
checkout that branch first instead if "master").

Sometimes new dependencies may have been added, or some dependency versions
changed, so it is also good to make sure your conda environment is
up-to-date:

.. code-block:: console

    $ conda env update [-f <environment-cuda.yml|environment-cpu.yml>]

where they environment file only needs to be specified if not using the
default environment.

Finally, sometimes it is necessary to reinstall the package as well (e.g.
if the entrypoints have changed):

.. code-block:: console

    $ pip install -e .

Depending on what changed since you last updated, the safest process is to
do all of the above:

.. code-block:: console

    $ git checkout master && git pull && conda env update && pip install -e .


Running the tests
=================

This full test suite can be run like:

.. code-block:: console

    $ pytest -v

In this case the ``-v`` option provides verbose output; it can be omitted.

Running the tests is encouraged to do first thing after installation, to
ensure all the tests are working on your setup (if not, this is either a bug
in your setup or in the code, so please `open an issue
<https://gitlab.inria.fr/ml_genetics/private/dnadna/issues>`_ so that we can
check).

In addition you should check that your code complies with the style
recommendations made by flake8_. For
that, either use an editor where you can integrate ``flake8`` (such
as atom) or install ``flake8`` from command line and run:

.. code-block:: console

    $ flake8 dnadna tests

All code style recommendations are just that: a recommendation.  There will
always be exceptions, in which case you can ask the style checker to ignore
certain warnings/errors by adding a ``# noqa: NNN`` comment next to the
affected line; see `In-Line Ignoring Errors
<https://flake8.pycqa.org/en/latest/user/violations.html?highlight=noqa#in-line-ignoring-errors>`_.


Building and editing the docs
=============================

The documentation is built using the Sphinx_ documentation generator, with
most of the documentation pages written in the reStructuredText_ format.
See their documentation for full details on how to work with these tools.

To build the HTML docs, starting from the root of the repository, run:

.. code-block:: console

    $ cd docs/
    $ make html

The output can be found in the ``_build/html`` output, and can be opened in
your browser once built.  E.g.,

.. code-block:: console

    $ firefox _build/html/index.html

It is also possible to build the docs as a PDF, as long you have the
necessary :math:`\LaTeX` tools installed, by running ``make latexpdf``.
However, this has not been fully tested with DNADNA's docs, so the output
may not be perfect as of yet.

.. _Sphinx: https://www.sphinx-doc.org/en/2.0/
.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html

Sphinx/reST style guide
-----------------------

reStructuredText_ (reST) is a powerful markup language that has a little bit
of a learning curve.  It's a little bit like the simpler Markdown language
you may be familiar with, but predates it, and is much more extensible.  For
full reference on the language, see the link at the beginning of this
paragraph.

Headings
^^^^^^^^

Section headings in reST are written by writing the title of the heading,
and underlining it with some character, technically of your choosing, with
the same number of characters as the length of the title.  For example:

.. code-block:: rst

    Section Heading
    ===============

For extra emphasis, you may also add an overline:

.. code-block:: rst

    ==========================
    Emphasized Section Heading
    ==========================

Sub-section headings are simply determined by the order in which heading
underline characters are used.  There is not technically a prescribed order,
it just depends on the order in which heading characters first appear in the
document.  This takes a little getting used to, but it makes sense.  For
example:

.. code-block:: rst

    Section 1
    =========

    If this is the first heading in the document, the the = character is
    used for H1 headings.

    Section 1.1
    -----------

    reST sees that a new heading character has been used, - instead of =, so
    - becomes an H2 heading

    Section 2
    =========

    Now we've used = again, so reST recognizes that we've gone back up a
    heading level

    Sub-section 2.1
    ---------------

    Sub-sub-section 2.1.1
    ^^^^^^^^^^^^^^^^^^^^^

    As ^ has appeared for the first time in the document as a heading
    underline, it becomes the H3 heading.

The only rule is that heading levels must be consistent within a single
file; they do not have to be the same in every file in the documentation.
However, it's good to try to remain consistent throughout the documentation.
One commonly used order is ``#, =, -, ^, ", '`` for H1 through H6
respectively.  So try to use this order consistently throughout the
documentation to the extent possible.

Code and API links
^^^^^^^^^^^^^^^^^^

When writing anything "code-like", such as the names of commands, variables,
small in-line code samples, etc. please surround such text with
double-backquotes to display them in typewriter text, like:

.. code-block:: rst

    Use the command ``dnadna init`` to create a new training configuration
    file from a template.

This renders as:

    Use the command ``dnadna init`` to create a new training configuration
    file from a template.

This is unlike Markdown which uses only single-backquotes for this purpose.
In reST single-backquotes are used for a powerful feature of reST known as
`interpreted text`_.  Throughout this documentation, the primary purpose of
single-backticks is to reference API docs.  So when referencing the name of
Python objects such as a *class*, *method*, *function*, and in some cases
*class attributes* or *global variables* that are documented in the
:ref:`dnadna API docs <api>`, **use single backquotes** around the name.
This will produce a link to the API docs. For example:

.. code-block:: rst

    Writing `.SNPSample` produces a link the API docs for that class.

    In some cases, if there is ambiguity, you can also write the object's
    full import path like `dnadna.snp_sample.SNPSample`.  If you need to
    use the full import path, but you only want to display the final
    component of the path (i.e. the object name) you can prefix it with
    a ``~`` like: `~dnadna.snp_sample.SNPSample`.

    If a class's attributes are documented, you can also link to them like
    `.SNPSample.snp`.  If you are writing the docstring for an object in
    *the same module* you can omit the preceding ``.`` and just write
    ```SNPSample```.  Otherwise, if the object is not in the same module,
    this lookup will fail.  The ``.`` is a shorthand for "search all the
    API docs for the first object of that name" and may fail if there is
    ambiguity (in which case you can use the full path format).

    Finally, you can provide alternate display text for the link by writing
    it like `the SNPSample class <SNPSample>`, where the part in the ``<>``
    is the actual reference as in the previous examples, and the text before
    it is what is displayed in the page.

    This can be used to reference other API docs as well.  For example most
    objects in the Python standard library can be referenced this way:
    `str`, `pathlib.Path`, as well as several of DNADNA's other dependencies
    that are referenced in the documentation: `pytorch.Tensor`.

This renders as:

    Writing `.SNPSample` produces a link the API docs for that class.

    In some cases, if there is ambiguity, you can also write the object's
    full import path like `dnadna.snp_sample.SNPSample`.  If you need to
    use the full import path, but you only want to display the final
    component of the path (i.e. the object name) you can prefix it with
    a ``~`` like: `~dnadna.snp_sample.SNPSample`.

    If a class's attributes are documented, you can also link to them like
    `.SNPSample.snp`.  If you are writing the docstring for an object in
    *the same module* you can omit the preceding ``.`` and just write
    ```SNPSample```.  Otherwise, if the object is not in the same module,
    this lookup will fail.  The ``.`` is a shorthand for "search all the
    API docs for the first object of that name" and may fail if there is
    ambiguity (in which case you can use the full path format).

    Finally, you can provide alternate display text for the link by writing
    it like `the SNPSample class <.SNPSample>`, where the part in the ``<>``
    is the actual reference as in the previous examples, and the text before
    it is what is displayed in the page.

    This can be used to reference other API docs as well.  For example most
    objects in the Python standard library can be referenced this way:
    `str`, `pathlib.Path`, as well as several of DNADNA's other dependencies
    that are referenced in the documentation: `torch.Tensor`.

.. _interpreted text: https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html

Code blocks
^^^^^^^^^^^

To display multi-line code blocks with source code highlighting, there are a
few different options.  The two most common are as follows.

This simplest case is, if the previous line of text ends with a double-colon
``::``, that indicates that a code block follows.  The code block must be
indented:

.. code-block:: rst

    Here is some example Python code::

        >>> from dnadna.utils.tensor import nanmean
        >>> nanmean([1.0, 2.0, float('nan'), 3.0]).item()
        2.0

This renders as:

    Here is some example Python code::

        >>> from dnadna.utils.tensor import nanmean
        >>> nanmean([1.0, 2.0, float('nan'), 3.0]).item()
        2.0

In this case, Sphinx will attempt to guess the appropriate syntax highlighter
to use.  For syntactically correct Python examples this will usually work.
However, if you want to specify the language explicitly, you can use the
``.. code-block:: <language>`` directive_ like:

.. code-block:: rst

    Here is another Python example:

    .. code-block:: python

        >>> from dnadna.snp_sample import SNPSample
        >>> sample = SNPSample([[0, 1], [1, 0]], [0.2, 0.3])
        >>> sample.to_dict()
        {'SNP': ['01', '10'], 'POS': [0.2, 0.3]}

Which renders similarly as:

    .. code-block:: python

        >>> from dnadna.snp_sample import SNPSample
        >>> sample = SNPSample([[0, 1], [1, 0]], [0.2, 0.3])
        >>> sample.to_dict()
        {'SNP': ['01', '10'], 'POS': [0.2, 0.3]}

The highlight language can be any language supported by Pygments_.

.. _directive: https://www.sphinx-doc.org/en/2.0/usage/restructuredtext/directives.html#directive-code-block
.. _Pygments: https://pygments.org/docs/lexers/

Docstring format
^^^^^^^^^^^^^^^^

Any Python class, method, or function can have a *docstring* by placing a
Python string (typically in triple-quoted ``"""Block"""`` format:

.. code-block:: python

    class MyClass:
        """Documentation for MyClass"""

        def my_method(self):
            """Documentation for MyClass.my_method."""

The Python language itself does not make any prescriptions for how the
contents of docstrings are formatted beyond the conventions *recommended*
by `PEP 257`_.  Many conventions exist for how the contents of docstrings
should be formatted.

DNADNA follows many other scientific Python packages in using the
`numpydoc`_ style for docstrings.  This specifies a convention for
formatting docstrings so that function and class constructor arguments, as
well as attributes, are nicely formatted when rending API docs.  See the
numpydoc documentation for a full description of the format.

Python does not normally have a syntax for providing docstrings to
module-level variables and class attributes.  However, has two syntaxes for
this to choose between.  The first uses comments like:

.. code-block:: python

    #: This is documentation for the following variable.
    THE_ANSWER = 42

or you can use a more docstring-like syntax by putting a string directly
after the variable assignment:

.. code-block:: python

    THE_ANSWER = 42
    """This is documentation for the above variable."""

    class MyClass:
        """The class's docstring."""

        foo = 'bar'
        """This is documentation for the above class attribute."""

We prefer the latter format, as it is more consistent with how other objects
in Python are documented, although some people find it a bit jarring to put
documentation for a variable below its assignment, instead of above.


Releasing
=========

Release instructions for DNADNA developers.

.. todo::

    Most of this process can and should be automated with a combination
    of tooling (e.g. `zest.releaser`_) and a CI job to run on tags.

DNADNA uses `setuptools_scm`_ which sets the package version from the latest
git tag.  So creating a release is mostly a matter of tagging a new version
in git.  However, there are some additional steps to perform before creating
a new release.

1. Determine what the next version should be keeping in mind the basic
   guidelines (if not the full exact specification) of `Semantic
   Versioning`_.  To summarize:

   * Increment the PATCH version if releasing only bug fixes.

   * Increment the MINOR version if the release also contains new features
     that are backwards-compatible with the previous MINOR version.

   * Increment the MAJOR version when making backwards-incompatible changes
     (or sometimes for marking reasons ;)

   Also make sure to conform to `PEP 440`_ in the version formatting.

2. *Strongly* consider creating a *release candidate*.  In this case the
   release version will be the same as the one you are planning to make,
   but with ``rc0`` appended.  E.g. ``1.1.0rc0``.  This allows testing the
   entire release process end-to-end and ensuring that everything works.
   If, after the first release candidate, further changes are needed, you
   can make a second release candidate with ``rc1`` and so on.  After a
   successful release candidate you can make the final release just by
   creating a new git tag from the same commit as the last RC (see the next
   steps on tagging).

3. Edit the ``CHANGELOG.md`` file to ensure that the version is correct in
   the heading for the upcoming release, and change the string
   ``(unreleased)`` to the release date like ``(YYYY-MM-dd)``.

   Commit this change with the message "Preparing to release version X.Y.Z"
   where of course "X.Y.Z" should be replaced with the actual version.

4. Tag the release in git by running::

       $ git tag -s X.Y.Z -m "release version X.Y.Z"

   replacing "X.Y.Z" with the actual version.  Make sure to
   `sign <https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work>` the
   tag with ``-s``.

5. Create a source tarball and wheel:

   .. note::

       First run ``pip install build twine`` if you don't have the ``build``
       or ``twine`` packages installed.

   Run:

   .. code-block:: console

       $ python -m build --sdist --wheel

   And verify that the packages are up-to-spec using twine:

   .. code-block:: console

       $ twine check dist/*{.tar.gz,.whl}

6. Now you can upload the source and wheel packages to PyPI using twine--you
   will have to provide your PyPI username and password, and have write
   access to the `dnadna`_ project on PyPI:

   .. code-block:: console

       $ twine upload dist/*{.targ.gz,.whl}

7. Build and upload the conda package.  For this you will need to have
   ``conda-build`` installed, as well as the Anaconda client:

   .. code-block:: console

       $ conda install conda-build anaconda-client

   .. note::

       To upload the conda package you will also need an account on
       anaconda.org with maintainer permissions to the `mlgenetics
       organization`_.

   If you haven't done so already, log in to your anaconda.org account:

   .. code-block:: console

       $ anaconda login

   Now build and upload the package using ``conda build``:

   .. code-block:: console

       $ conda build --user mlgenetics -c conda-forge -c pytorch -c bioconda conda/

   .. note::

       Annoyingly, much like when installing a conda package that has
       dependencies from multiple channels, it is also necessary to specify
       the correct channels when running ``conda build``.  This can also
       be avoided by adding them to your default channels list.

8. After release, bump the chanelog to the next planned release version by
   prepending a new sub-section to the previous release's sub-section like::

       X.Y.Z (unreleased)
       ------------------

       * Nothing changed yet

   Where X.Y.Z is typically the next patch version; this can be changed
   later if it's decided the next release will be a minor/major version
   bump.  Commit this change.


.. _PEP 257: https://www.python.org/dev/peps/pep-0257/
.. _numpydoc: https://numpydoc.readthedocs.io/en/latest/format.html
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _zest.releaser: https://zestreleaser.readthedocs.io/en/latest/
.. _setuptools_scm: https://github.com/pypa/setuptools_scm/
.. _Semantic Versioning: https://semver.org/#summary
.. _PEP 440: https://peps.python.org/pep-0440/
.. _dnadna: https://pypi.org/project/dnadna/
.. _mlgenetics organization: https://anaconda.org/mlgenetics
