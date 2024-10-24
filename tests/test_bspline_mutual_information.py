import pytest
from numpy import array
from numpy import array_equal

def test_import():
    try:
        import bspline_mutual_information
    except:
       pytest.fail("Could not import 'bspline_mutual_information'")
    assert hasattr(bspline_mutual_information, "bspline_bin")
    assert hasattr(bspline_mutual_information, "mutual_information")


def test_bspline_bin():

    from bspline_mutual_information import bspline_bin
    
    x = [1,2,3,4,5]
    expected_result = array([
        [1. , 0. , 0. ],
        [0.5, 0.5, 0. ],
        [0. , 1. , 0. ],
        [0. , 0.5, 0.5],
        [0. , 0. , 1. ]
        ])
    
    assert array_equal(bspline_bin(data=x, bins=3, order=2), expected_result)


def test_mutual_information():

    from bspline_mutual_information import mutual_information

    x = [1,2,3,4,5]
    y = [1,2,1,2,3]
    expected_result = .4740122135541802
    result = mutual_information(x, y, bins=5, spline_order=3)
    assert result == expected_result


def test_mutual_information_correct():
    
    from bspline_mutual_information import mutual_information

    x = [1,2,3,4,5]
    with pytest.raises(ValueError) as excinfo:
        mutual_information(x, x, spline_order=2, correct=True)
    assert excinfo.type is ValueError
