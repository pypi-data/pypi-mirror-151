Source files for building pybind interface for use in the `nepy` module. Base on the CPU only implementation in `tools/nep_related/nep_cpu` in GPUMD.

The pybind interface is defined in `nepy`. These source files where copied from `tools/nep_related/nep_cpu` for enabling recompilation of the pybind interface.

The pybind interface can be compiled locally with the following command:

```bash
c++ -O3 -Wall -shared -std=c++11 -fPIC -I/usr/include/python3.8 nepy.cpp -o _nepy$(python3-config --extension-suffix) && export PYTHONPATH=$PWD:${PYTHONPATH}
```

The files where copied from gpumd-fork@2e0343340f5e67529e592776b6b72dd61840998c on master, on the 4/05/2022.

`expected_descriptors` contains reference descriptors from `nep_cpu`.
