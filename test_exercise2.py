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
    assert decide("test_returning_citizen.json", "countries.json") ==\
        ["Accept", "Accept", "Quarantine"]

