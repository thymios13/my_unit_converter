from unit_converter import *
from nose.tools import assert_raises, assert_equal

def test_different_units_for_equality():
    with assert_raises(IncompatibleUnitsError):
        Term(5)*'meters' == Term(2)*'seconds'

def test_different_units_for_adding():
    with assert_raises(IncompatibleUnitsError):
        Term(5)*'meters' + Term(2)*'seconds'

def test_if_the_conversion_is_correct():
    assert_equal(Term(5)*'meters', Term(0.005)*'kilometers')

def test_if_the_conversion_is_to_the_same_unit():
    assert_equal((Term(60)*'seconds').to('minutes').unit, 'minutes')

def test_if_the_conversion_result():
    assert_equal((Term(60)*'seconds').to('minutes').coefficient, 1)