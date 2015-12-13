#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. DBMS

This module performs table operations on database tables
implemented as lists of lists. """

__author__ = 'Pranjal Swami, Billal Sarwar, and Hirra Sheikh'



#####################
# HELPER FUNCTIONS ##
#####################

def remove_duplicates(l):
    """
    Removes duplicates from l, where l is a List of Lists.
    :param l: a List
    """

    d = {}
    result = []
    for row in l:
        if tuple(row) not in d:
            result.append(row)
            d[tuple(row)] = True

    return result


class UnknownAttributeException(Exception):
    """
    Raised when attempting set operations on a table
    that does not contain the named attribute
    """
    pass


def selection(t, f):
    """
    Perform select operation on table t that satisfy condition f.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    ># Define function f that returns True iff
    > # the last element in the row is greater than 3.
    > def f(row): row[-1] > 3
    > select(R, f)
    [["A", "B", "C"], [4, 5, 6]]
    :param f:
    :param t:

    """
    result_table = []
    for row in t:
        f_value = f(row)
        if f_value is True:
            result_table.append(row)

    return result_table





def projection(table, attributes):
    """
    Perform projection operation on table t
    using the attributes subset r.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    > projection(R, ["A", "C"])
    [["A", "C"], [1, 3], [4, 6]]

    """
    if len(table) <= 0:
        return []
    # This stores index positions of the attributes in the header row
    attribute_indexes = []

    # First row of table should contain table headers
    headers = table[0]

    # Calculate index positions on which attributes exist in header row
    for attribute in attributes:
        if attribute in headers:
            attribute_indexes.append(headers.index(attribute))
        else:
            raise UnknownAttributeException("Attribute: {0} not recognized".format(attribute))

    result_table = [attributes]
    for row in table[1:]:
        result_row = []

        for attribute_index in attribute_indexes:
            # Grab value from appropriate index in current row
            result_row.append(row[attribute_index])

        result_table.append(result_row)

    return result_table


def cross_product(t1, t2):
    """
    Return the cross-product of tables t1 and t2.

    Example:
    > R1 = [["A", "B"], [1,2], [3,4]]
    > R2 = [["C", "D"], [5,6]]
    [["A", "B", "C", "D"], [1, 2, 5, 6], [3, 4, 5, 6]]


    """

    if len(t1) == 0 and len(t2) == 0:
        return []
    elif len(t1) == 0:
        return t2
    elif len(t2) == 0:
        return t1

    header1 = t1[0]
    header2 = t2[0]

    # Initialize header table with headers from both tables
    result_table = [header1 + header2]

    # Skip first row in both tables since headers have already been processed above
    for r1 in t1[1:]:
        for r2 in t2[1:]:
            result_table.append(r1 + r2)

    return result_table

