"""
Utility to bin continous variables and estimate mutual information based
on B-Spline binning.

This is an adaption of Carsten Daub's R implementation [1]_ of the algorithm
described in Daub et.al 2004 [2]_.

References
==========

.. [1] https://gitlab.com/daub-lab/mutual_information
.. [2] Daub CO, Steuer R, Selbig J, Kloska S. Estimating mutual 
    information using B-spline functions--an improved similarity 
    measure for analysing gene expression data. BMC Bioinformatics. 
    2004 Aug 31;5:118. doi: `10.1186/1471-2105-5-118 
    <https://doi.org/10.1186/1471-2105-5-118>`_. PMID: 15339346; 
    PMCID: PMC516800.
"""

import numpy as np
from numpy.typing import ArrayLike
from scipy.interpolate import BSpline

def bspline_bin(
        data: ArrayLike,
        bins: int=10,
        order: int=1
        ) -> np.ndarray:
    """
    This function enables adaptive binning of continous variables into
    a user defined number of bins with associated weights. The 
    underlying methodology relies on an extension of indicator functions
    of B-Splines described in [1]_.

    Parameters
    ----------
    data : ArrayLike
        1-dimensional array like, that contains the data / values that 
        should be binned
    bins : int, default = 10
        Number of bins that the values should be binned into. Defaults 
        to 10.
    order : int, default = 1
        Spline order of the B-spline function. An order of 1 (the
        default) represent standart binning, i.e. each value is assigned
        to one bin only. Higher values of spline order will assign the 
        data values up to the corresponding number of bins, i.e. a 
        spline order of 3 will assign the data value up to 3 bins with 
        respective weights as determined by the indicator function. Note
        that :math:`order = degree + 1`.

    Returns
    -------
    design_matrix : numpy.ndarray
        A matrix of size [n, b] where n is the number of values in / 
        size of ``data`` and b is the number of ``bins``.

    Example
    -------
    >>> from valpas.utils.b_spline import bspline_bin
    >>> x = [1,2,3,4,5]
    >>> bspline_bin(data=x, bins=3, order=2)
    array([[1. , 0. , 0. ],
           [0.5, 0.5, 0. ],
           [0. , 1. , 0. ],
           [0. , 0.5, 0.5],
           [0. , 0. , 1. ]])

    References
    ----------
    .. [1] Daub CO, Steuer R, Selbig J, Kloska S. Estimating mutual 
        information using B-spline functions--an improved similarity 
        measure for analysing gene expression data. BMC Bioinformatics. 
        2004 Aug 31;5:118. doi: `10.1186/1471-2105-5-118 
        <https://doi.org/10.1186/1471-2105-5-118>`. PMID: 15339346; 
        PMCID: PMC516800.

    """
    try:
        data = np.array(data)
    except Exception as e:
        raise e

    # TODO: add check if the array is 1 dimensional
    # TODO: add check if the array only contains floats

    degree = order - 1 # BSpline.design_matrix uses degree as argument
    knots = range(0, (bins + order), 1)
    
    # bspline_min & bspline_max are needed for the transformation of the
    # data values into the domain of B-Spline functions
    bspline_min = knots[degree]
    bspline_max = knots[bins]
    data_t = _transform_data(
        data=data,
        bspline_min=bspline_min,
        bspline_max=bspline_max
        )

    # the design matrix of a B-Spline that can be generated by defining
    # values at which the BSpline functions should be evaluated as well 
    # as the knots and the degree (order - 1) will yield the weighted 
    # bin associations that we are looking for
    design_matrix = BSpline.design_matrix(
        data_t, knots, degree).toarray()

    return design_matrix


def _transform_data(
        data: np.ndarray,
        bspline_min: int,
        bspline_max: int
        ) -> np.ndarray:
    """
    Internal helper function to transform values into the domain of 
    B-Spline functions for use in :func:`bspline_bin`.

    Parameters
    ----------
    data : numpy.ndarray
        Array containing values to be transformed into domain of
        B-spline functions
    bspline_min : int
        Required lower knot of the B-spline function definition. 
        Generally `bspline_min = knots[degree]` where 
        :math:`knots = {0, 1, ..., K}, K = bins + order` and
        :math:`degree = order - 1` 
    bspline_max : int
        Required upper know of the B-spline function definition.
        Generally `bspline_max = knots[bins]` where
        :math:`knots = {0, 1, ..., K}, K = bins + order`

    Returns
    -------
    data_t : numpy.ndarray
        1-dimensional array containing the transformed values of 
        ``data``
    """
    data_t = (
        (data - min(data))
        * (bspline_max - bspline_min)
        / (max(data) - min(data))
        + bspline_min
    )

    return data_t


def mutual_information(
        x: ArrayLike,
        y: ArrayLike,
        bins: int=10,
        spline_order: int=1,
        correct: bool=False,
        min_def: int=0,
    ) -> float | None:
    """
    Estimates Mutual Information between two arrays containing continous
    variables. Uses Daub et.al's approach [1]_ to estimate Mutual 
    Information using B-Spline functions.

    Parameters
    ----------
    x : ArrayLike
        1-dimensional array like object containing values
    y : ArrayLike
        1-dimensional array like object containing values
    bins : int, default = 10
        Number of bins to use for the B-Spline based binnig of the 
        continous values in ``x`` and ``y``. 
    spline_order : int, default = 1
        Spline order for the generation of B-Spline functions that are 
        used to extract bin associations. ``spline_order = 1`` will 
        result in basic binning. Higher values of ``spline_order`` will 
        assign the data values of ``x`` and ``y`` up to the 
        corresponding number of bins, i.e. a spline order of 3 will 
        assign the data values up to 3 bins with respective weights as 
        determined by the indicator function.
    min_def : int, default = 0
        Optional value that defines the minimal number of position i 
        that ``x`` and ``y`` must both be defined at, i.e. both values 
        at ``x[i]`` and ``y[i]`` must not be NaN. If less than 
        ``min_def`` positions are defined the return value ``mi`` will 
        be `None`.

    Returns
    -------
    mi : float
        Mutual Information estimate for ``x`` and ``y``
    
    Example
    -------
    >>> from valpas.utils.b_spline import mutual_information
    >>> x = [1,2,3,4,5]
    >>> y = [1,2,1,2,3]
    >>> mutual_information(x, y, bins=5, spline_order=3)
    0.4740122135541802

    If ``min_def`` is defined and less than ``min_def`` positions in 
    both ``x`` and ``y`` are defined the return value will be `None`

    >>> x = np.asarray([1,2,np.nan,4,np.nan])
    >>> y = np.asarray([1,2,1,None,5])
    >>> mi = mutual_information(x, y, bins=5, spline_order=3, min_def=3)
    >>> type(mi)
    NoneType 

    References
    ----------
    .. [1] Daub CO, Steuer R, Selbig J, Kloska S. Estimating mutual 
        information using B-spline functions--an improved similarity 
        measure for analysing gene expression data. BMC Bioinformatics. 
        2004 Aug 31;5:118. doi: `10.1186/1471-2105-5-118 
        <https://doi.org/10.1186/1471-2105-5-118>`. PMID: 15339346; 
        PMCID: PMC516800.
    """

    if spline_order > 1 and correct == True:
        raise ValueError(
            "The correction for the finite size effect is "
            "only available for 'spline_order = 1'"
            )

    try:
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
    except Exception as e:
        raise e

    # TODO: add check if the array is 1 dimensional
    # TODO: add check if the array only contains floats


    # checking / filtering x & y to positions where both of the arrays
    # contain values that are defined (not NaN)
    xy_defined = np.where(~np.isnan(x) & ~np.isnan(y))
    x_defined_vals = x[xy_defined]
    y_defined_vals = y[xy_defined]

    # min_def can be used as "reliability check" to not calculate mutual
    # information between two vectors with too little overlap
    if(len(xy_defined)/len(x) < min_def):
        mi = None
    else:
        try:
            x_bin_associations = bspline_bin(
                data=x_defined_vals,
                bins=bins,
                order=spline_order
            )
            y_bin_associations = bspline_bin(
                data=y_defined_vals,
                bins=bins,
                order=spline_order
            )
        except ValueError:
            # If all values in x or y are identical (e.g. x=[1,1,1,1])
            # the B-Spline binning can not produce a design_matrix. 
            # This is extremely unlikely to be the case in a real world
            # scenario. One could make the argument that the each value 
            # should then be assigned to all bins with the same weight. 
            # However, this is counter to the underlying idea of using 
            # b-splines since the spline_order dictates the maximum
            # number of bins a value can be assigned to. The previously 
            # suggested potential behaviour would only be possible if 
            # spline_order == bins, which for all intents and purposes
            # is unlikely to happen.
            # To compensate for this edge case we define the mutual
            # information to be 'None' if one of the two arrays contains
            # only indentical values.  
            mi = None
            return mi
        
        # calculation of probabilities x[i] and y[i] based of the bin(i) 
        # association probabilities as determined by the B-Spline
        # functions
        p_x = np.sum(x_bin_associations, axis=0) / len(x_defined_vals)
        p_y = np.sum(y_bin_associations, axis=0) / len(y_defined_vals)
        p_x_y = (
            np.matmul(
                np.transpose(x_bin_associations),
                y_bin_associations
                ) / len(x)
            ).flatten('F') 
        # calculation of the Shannon entropy H(A) where A = x & y
        h_x = -np.nansum(p_x * np.log2(p_x))
        h_y = -np.nansum(p_y * np.log2(p_y))
        # calculation of the joint entropy H(A,B)
        h_x_y = -np.nansum(p_x_y * np.log2(p_x_y))

        # mutual information based on calculated entropies
        mi = float(h_x + h_y - h_x_y)
        
        # correction for the finite size effect
        if correct == True:
            mi = mi - (bins - 1) / (2 * len(x_defined_vals))

    return mi
