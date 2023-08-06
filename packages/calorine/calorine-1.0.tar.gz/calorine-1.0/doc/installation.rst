Installation
============

.. note::

    This page only concerns installation of :program:`calorine`.
    If you want to install :program:`GPUMD`, please consult the `GPUMD documenation <https://gpumd.zheyongfan.org/>`_

Installation via `pip`
----------------------

Stable versions of :program:`calorine` are provided via `PyPI <https://pypi.org/project/calorine/>`_.
This implies that :program:`calorine` can be installed using `pip` via::

    pip3 install calorine --user

The `PyPI` package is provided as a `source distribution <https://packaging.python.org/glossary/#term-Source-Distribution-or-sdist>`_.
As a result, the C++ code has to be compiled as part of the installation, which requires a C++11 compliant compiler to be installed on your system, e.g., `GCC 4.8.1 and above <https://gcc.gnu.org/projects/cxx-status.html#cxx11>`_ or `Clang 3.3 and above <https://clang.llvm.org/cxx_status.html>`_.

Installing the development version
----------------------------------

If installation via pip fails or if you want to use the most recent (development) version you can do::

    pip install --user git+https://gitlab.com/materials-modeling/calorine.git

Manual installation (primarily for developers)
----------------------------------------------

To manually install :program:`calorine`, you can do:

    git clone git@gitlab.com:materials-modeling/calorine.git
    cd calorine
    export PYTHONPATH=$PYTHONPATH:$PWD
    cd src/nepy
    c++ -O3 -Wall -shared -std=c++11 -fPIC -I/usr/include/python3.8 nepy.cpp -o _nepy$(python3-config --extension-suffix)
    export PYTHONPATH=$PYTHONPATH:$PWD

The last three lines are only necessary if you want to install the PyBind interface.
Note that `python3.8` should be replaced with the Python version installed on your machine.