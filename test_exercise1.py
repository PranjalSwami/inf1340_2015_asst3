#!/usr/bin/env python

""" Assignment 3, Exercise 1, INF1340, Fall, 2015. DBMS

Test module for exercise3.py

"""
import pytest

__author__ = 'Pranjal, Billal, Hirra'


from exercise1 import selection, projection, cross_product, UnknownFunctionException, UnknownAttributeException


###########
# TABLES ##
###########

EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
             ["Smith", "Mary", 25, 2000],
             ["Black", "Lucy", 40, 3000],
             ["Verdi", "Nico", 36, 4500],
             ["Smith", "Mark", 40, 3900]]

R1 = [["Employee", "Department"],
      ["Smith", "sales"],
      ["Black", "production"],
      ["White", "production"]]

R2 = [["Department", "Head"],
      ["production", "Mori"],
      ["sales", "Brown"]]

R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]


#####################
# HELPER FUNCTIONS ##
#####################
def is_equal(t1, t2):

    t1.sort()
    t2.sort()

    return t1 == t2


#####################
# FILTER FUNCTIONS ##
#####################


def filter_employees(row):
    """
    Check if employee represented by row
    is AT LEAST 30 years old and makes
    MORE THAN 3500.
    :param row: A List in the format:
        [{Surname}, {FirstName}, {Age}, {Salary}]
    :return: True if the row satisfies the condition.
    """
    return row[-2] >= 30 and row[-1] > 3500


def last_elem_gt_three(row):
    """
    Returns true iff last element in row is greater than 3
    :param row:
    :return:
    """
    return row[-1] > 3


###################
# TEST FUNCTIONS ##
###################


def test_selection():
    """
    Test select operation.
    """
    # Test last_element_gt_three method selection
    result = [["A", "B", "C"], [4, 5, 6]]
    assert is_equal(result, selection(R, last_elem_gt_three))

    # Test empty table returned when no rows in result
    input_table = [[1, 1, 1], [2, 2, 2]]
    assert is_equal([], selection(input_table, last_elem_gt_three))

    # Test empty table returned when input table is null
    assert is_equal([], selection([], last_elem_gt_three))

    # Test filter employee method selection
    result = [["Surname", "FirstName", "Age", "Salary"],
              ["Verdi", "Nico", 36, 4500],
              ["Smith", "Mark", 40, 3900]]
    assert is_equal(result, selection(EMPLOYEES, filter_employees))

    # If selection function is not passed, should raise exception
    with pytest.raises(UnknownFunctionException):
        not_a_fn = []
        selection(R, not_a_fn)


def test_projection():
    """
    Test projection operation.
    """

    result = [["Surname", "FirstName"],
              ["Smith", "Mary"],
              ["Black", "Lucy"],
              ["Verdi", "Nico"],
              ["Smith", "Mark"]]
    assert is_equal(result, projection(EMPLOYEES, ["Surname", "FirstName"]))

    result = [["A", "C"], [1, 3], [4, 6]]
    assert is_equal(result, projection(R, ["A", "C"]))

    # If attributes passed in is empty, return empty table
    assert is_equal([], projection(EMPLOYEES, []))

    # Empty table as input should return empty table
    assert is_equal([], projection([], ["Surname", "FirstName"]))

    with pytest.raises(UnknownAttributeException):
        projection(EMPLOYEES, ["InvalidColumn"])

        # Mix of valid and invalid columns should still raise exception
        projection(EMPLOYEES, ["Surname", "InvalidColumn"])


def test_cross_product():

    result = [["Employee", "Department", "Department", "Head"],
              ["Smith", "sales", "production", "Mori"],
              ["Smith", "sales", "sales", "Brown"],
              ["Black", "production", "production", "Mori"],
              ["Black", "production", "sales", "Brown"],
              ["White", "production", "production", "Mori"],
              ["White", "production", "sales", "Brown"]]
    assert is_equal(result, cross_product(R1, R2))

    # Empty tables should give back original table
    assert is_equal(R1, cross_product(R1, []))
    assert is_equal(R2, cross_product([], R2))

    # If both tables empty, return
    assert cross_product([], []) is None

    # Test case with different schema
    table1 = [["First Name"],
              ["bat"],
              ["super"]]
    table2 = [["Last Name"],
              ["man"],
              ["girl"]]

    result = [["First Name", "Last Name"],
              ["bat", "man"],
              ["bat", "girl"],
              ["super", "man"],
              ["super", "girl"]]
    assert is_equal(result, cross_product(table1, table2))
