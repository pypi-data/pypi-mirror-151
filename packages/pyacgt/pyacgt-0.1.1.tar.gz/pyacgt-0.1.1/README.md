
# pyacgt
[![PyPI Versions Badge](https://img.shields.io/pypi/pyversions/pyacgt?style=for-the-badge)](https://pypi.org/project/pyacgt/)
[![PyPI Wheel Badge](https://img.shields.io/pypi/wheel/pyacgt?style=for-the-badge)](https://pypi.org/project/pyacgt/)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A Python 3.7+ interface for Havas and Ramsay's ACME package.
Currently only supports Windows and Linux. **If someone can build and send MacOS binaries for ACME, I can implement this!**

## License

## Contributors

- [Nicholas Meyer](https://www.nickmeyer.me)
    + [Email: nicholas.meyer2@huskers.unl.edu](mailto:nicholas.meyer2@huskers.unl.edu)


## Related Programs and Literature

 - Havas&ndash;Ramsay [ACME package](https://staff.itee.uq.edu.au/havas/ACME/)
 - Meier&ndash;Zupan [Generalized square knots and homotopy 4-spheres](https://arxiv.org/abs/1904.08527)
 - Scharlemann [Proposed Property 2R counterexamples examined](http://dx.doi.org/10.1215/ijm/1498032031)
 - Gompf&ndash;Scharlemann&ndash;Thompson: [Fibered knots and potential counterexamples to the Property 2R and Slice-Ribbon Conjectures](http://dx.doi.org/10.2140/gt.2010.14.2305)
  
## Installation

Install pyacgt with either pip or directly from github.

```bash
  git clone https://github.com/nick5435/pyacgt.git
  cd pyacgt
  python setup.py install
```
or
```bash
python -m pip install -U pyacgt
```
## TODO

  - [x] Add `options` as a dict to `makeACMEinput`. 
  - [ ] May want to Objectify the interface. 
