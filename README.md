# bspline_mutual_information

Utility to bin continuous variables and estimate mutual information based on B-Spline binning.

This is an adaption of Carsten Daub's R implementation[^1] of the algorithm described in Daub et.al 2004[^2].

## Dependencies:
- python >= 3.9
- numpy
- scipy

## Installation

### pip / git
The most up-to-date version of the package can be installed by cloning the repository to a local folder and install via `pip` from source:
```sh
git clone https://github.com/pnnl-predictive-phenomics/bspline_mutual_information.git
cd bspline_mutual_information
pip install .
```

## Usage
Once installed the module consits of two functions:
- `bspline_mutual_information.bspline_bin()`
- `bspline_mutual_information.mutual_information()`

`bspline_bin()` is both called internally in `mutual_information` but can also be used to manually bin continuous data into discrete bins if so desired.

For this example we will focus on `mutual_information()` since it is the primary use case of this package.

Below an example can be found how to use `mutual_information()` to estimate the mutual information between two vectors containing continuous data points. It assumes a python environment.

```python
>>> from bspline_mutual_information import mutual_information
>>> x = [1,2,3,4,5]
>>> y = [1,2,1,2,3]
>>> mutual_information(x, y, bins=5, spline_order=3)
0.4740122135541802
```

If mutual information for pairs of columns in a whole matrix or pandas DataFrame should be calculated this can be done by leveraging pandas `DataFrame.corr()` function. However, since `corr()` does not allow for keyword arguments a helper function needs to be defined first that specifies the arguments `mutual_information` should be executed with. Consider the example below where the helper function `mut_inf(x, y)` is defined as returning the mutual information calculated using the parameters `bins=5`, `spline_order=1` and `correct=True` (which corrects for the finit size effect if `spline_order==1`). Note that `DataFrame.corr()` will always fill the diagonal with `1` values independent of the chosen `method`.

```python
>>> import pandas as pd
>>> import bspline_mutual_information as bsp
>>> data = pd.DataFrame({
...     'a': [0, 1, 2, 3, 4],
...     'b': [5, 6, 7, 8, 9],
...     'c': [0, 1, 2, 1, 0],
...     'd': [3, 2, 1, 3, 2]
...     })
...
>>> def mut_inf(x, y):
...     mi = bsp.mutual_information(
...         x, y,
...         bins=5,
...         spline_order=1,
...         correct=True
...         )
...     return mi
...
>>> data.corr(method=mutual_info)
          a         b         c         d
a  1.000000  1.921928  1.121928  1.121928
b  1.921928  1.000000  1.121928  1.121928
c  1.121928  1.121928  1.000000  0.321928
d  1.121928  1.121928  0.321928  1.000000
```

## References

[^1]: [C. Daub's R implementation](https://gitlab.com/daub-lab/mutual_information)

[^2]: Daub CO, Steuer R, Selbig J, Kloska S. Estimating mutual information using B-spline functions--an improved similarity measure for analysing gene expression data. BMC Bioinformatics. 2004 Aug 31;5:118. doi: [10.1186/1471-2105-5-118](https://doi.org/10.1186/1471-2105-5-118). PMID: 15339346; PMCID: PMC516800.