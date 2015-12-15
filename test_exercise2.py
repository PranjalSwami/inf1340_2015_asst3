#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Pranjal, Billal, Hirra'


# imports one per line
import pytest
import os
from exercise2 import decide, valid_passport_format, valid_visa_format, valid_date_format


DIR = "test_jsons/"
os.chdir(DIR)


def test_returning():
    """
    Travellers are returning to KAN.
    """

    # Visitor 1 is from KAN (no visa required) and has no visa - "Accept"
    # Visitor 2 is from KAN (no visa required) and has no visa - "Accept"
    # Visitor 3 is from KAN (no visa required) but coming from LUG with medical advisory - "Quarantine"

    assert decide("test_returning_citizen.json", "countries.json") ==\
        ["Accept", "Accept", "Quarantine"]

def test_visiting():
    """
    Travellers are visiting KAN
    """

    # Visitor 1 is from KRA (visa required) with a valid visa - "Accept"
    # Visitor 2 is from LUG (visa required) with a valid visa but has a "Mumps" medical advisory - "Quarantine"
    # Visitor 3 is from HRJ (no visa required) with no visa - "Accept"
    # Visitor 4 is from HRJ (no visa required) but is coming via LUG which as medical advisory - "Quarantine"
    # Visitor 5 is from GOR (no visitor visa, but transit visa required) with no visa - "Accept"
    # Visitor 6 is from FRY (visa required) with no visa - "Reject"
    # Visitor 7 is from BRD (visa required) with visa
    assert decide("test_visitor.json", "countries.json") ==\
           ["Accept", "Quarantine", "Accept", "Quarantine", "Accept", "Reject", "Reject"]

