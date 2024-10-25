# bspline_mutual_information

Utility to bin continous variables and estimate mutual information based
on B-Spline binning.

This is an adaption of Carsten Daub's R implementation[^1] of the algorithm described in Daub et.al 2004[^2].

## Dependencies:
- python >= 3.9
- numpy
- scipy

## Installation
It is recommended to first generate a new virtual environment via `venv` or `conda` for testing. 
Clone the repository and install locally by executing `pip install -e .` from within the root folder of the cloned git repository.

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

## References

[^1]: [C. Daub's R implementation](https://gitlab.com/daub-lab/mutual_information)

[^2]: Daub CO, Steuer R, Selbig J, Kloska S. Estimating mutual information using B-spline functions--an improved similarity measure for analysing gene expression data. BMC Bioinformatics. 2004 Aug 31;5:118. doi: [10.1186/1471-2105-5-118](https://doi.org/10.1186/1471-2105-5-118). PMID: 15339346; PMCID: PMC516800.