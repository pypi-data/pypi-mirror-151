.. index::
   single: Function reference; IO

IO functions
============

There functions for reading and writing input and output files (see e.g., :func:`calorine.io.convert_gpumd_run_to_traj`, :func:`calorine.io.read_xyz`, :func:`calorine.io.write_xyz`).
There are also functions for reading individual ``kappa.out`` and ``thermo.out`` files (:func:`calorine.io.read_kappa` and :func:`calorine.io.read_thermo`), series of those files (:func:`calorine.io.read_kappas` and :func:`calorine.io.read_thermos`) as well as configuration files (:func:`calorine.io.read_settings`).

Thermal conductivity runs
-------------------------

When organizing results from many thermal conductivity runs it is recommended to use ASE databases.
:program:`calorine` provides specific functions for this purpose (:func:`calorine.io.update_database` and :func:`calorine.io.read_from_database`).
For these functions to operate smoothly the :program:`GPUMD` runs ought to be organized in a directory structured as follows::

    <runpath>
    ├── xyz.in
    ├── run.in
    ├── 01
    │   ├── kappa.out
    │   └── thermo.out
    ├── 02
    │   ├── kappa.out
    │   └── thermo.out
    ├── 03
    │   ├── kappa.out
    │   └── thermo.out
    ⋮

The subdirectory names (``01``, ``02`` ... in the example above) are imaterial.
Alternatively one can also read the settings from a Python module (named ``config``) instead of the :program:`GPUMD` configuration file (named ``run.in``).

The :func:`calorine.io.update_database` function parses such a directory structure and turns it into a database entry::

    index = update_database('runs.db', 'gpumd_runs/T300')

The entry can be subsequently read and unpacked using the :func:`calorine.io.read_from_database` function as follows::

   db = connect('runs.db')
   row = db.get(id=1)
   settings, kappas, thermos = read_from_database(row)

Module
------

.. automodule:: calorine.io
   :members:
   :ignore-module-all:

.. currentmodule:: calorine.io
