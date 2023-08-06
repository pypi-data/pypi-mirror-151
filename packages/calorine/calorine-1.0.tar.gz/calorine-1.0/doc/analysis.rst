.. index::
   single: Function reference; Analysis

Analysis functions
==================

:program:`Calorine` provides a convenience function for calculating averages and errors over a time series of data (:func:`analyze_data` and others).

Furthermore, several functions are available for plotting results (see, e.g., :func:`calorine.analysis.plot_kappas_with_average`).
These functions are primarily intended to be used for quick visualizations, e.g., in a jupyter notebook::

    plot_kappas_with_average(kappas)

There is also a function to obtain averages over many runs (:func:`calorine.analysis.get_run_average`), which takes care of computing correlation lengths and producing error estimates::

    get_run_average(kappas, nequil=300)

Module
------

.. automodule:: calorine.data_analysis
   :members:
   :ignore-module-all:

.. currentmodule:: calorine.data_analysis

.. automodule:: calorine.analysis
   :members:
   :ignore-module-all:

.. currentmodule:: calorine.analysis
