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

def test_transiting():
    """
    Travellers are transiting through KAN
    """

    # Visitor 1 is from III (transit visa required) and has valid visa - "Accept"
    # Visitor 1 is from III (transit visa required) and has invalid visa - "Reject"
    # Visitor 3 is from III (transit visa required) but coming from LUG with medical advisory - "Quarantine"
    # Visitor 4 is from KRA (no transit visa required) with no visa - "Accept"
    # Visitor 5 is from GOR (transit visa required) with no visa - "Reject"
    assert decide("test_transit_visitor.json", "countries.json") ==\
           ["Accept", "Reject", "Quarantine", "Accept", "Reject"]

def test_invalid_inputs():
    """
    All entries in the json file should trigger various invalid inputs
    :return:
    """

    # Visitor 1 has incomplete records (passport field missing)
    # Visitor 2 has invalid passport number
    # Visitor 3 has invalid birth date
    # Visitor 4 has invalid home location
    # Visitor 5 has invalid from location
    # Visitor 6 has invalid entry reason
    # Visitor 7 has invalid visa date
    # Visitor 8 has invalid visa code
    # Visitor 9 has invalid via location
    assert decide("test_invalid_visitor.json", "countries.json") ==\
           ["Reject", "Reject", "Reject", "Reject", "Reject", "Reject", "Reject", "Reject", "Reject"]


def test_valid_passport_format():
    """
    Tests passport format validation is being done properly
    """

    assert valid_passport_format("JMZ0S-89IA9-OTCLY-MQILJ-P7CTY") == True
    assert valid_passport_format("JMZ-89I-OTC-MQI-P7C") == False
    assert valid_passport_format("") == False
    assert valid_passport_format("jmz0s-89ia9-otcly-moilj-p7cty") == True

