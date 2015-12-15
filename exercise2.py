#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. Kanadia

Computer-based immigration office for Kanadia

"""

__author__ = 'Pranjal Swami, Billal Sarwar, and Hirra Sheikh'


import re
import datetime
import json
import re

######################
## global constants ##
######################
REQUIRED_FIELDS = ["passport", "first_name", "last_name",
                   "birth_date", "home", "entry_reason", "from"]

######################
## global variables ##
######################
'''
countries:
dictionary mapping country codes (lowercase strings) to dictionaries
containing the following keys:
"code","name","visitor_visa_required",
"transit_visa_required","medical_advisory"
'''
COUNTRIES = None

# Define valid immigration statuses
IMMIGRATION_ACCEPT = "Accept"
IMMIGRATION_REJECT = "Reject"
IMMIGRATION_QUARANTINE = "Quarantine"

PASSPORT_PATTERN = "[A-Za-z0-9]{5}-[A-Za-z0-9]{5}-[A-Za-z0-9]{5}-[A-Za-z0-9]{5}-[A-Za-z0-9]{5}"
passport_matcher = re.compile(PASSPORT_PATTERN, re.IGNORECASE)

VISA_PATTERN = "[A-Za-z0-9]{5}-[A-Za-z0-9]{5}-[A-Za-z0-9]{5}-[A-Za-z0-9]{5}-[A-Za-z0-9]{5}"
visa_matcher = re.compile(VISA_PATTERN, re.IGNORECASE)

DATE_PATTERN = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
date_matcher = re.compile(DATE_PATTERN)


#####################
# HELPER FUNCTIONS ##
#####################
def is_more_than_x_years_ago(x, date_string):
    """
    Check if date is less than x years ago.

    :param x: int representing years
    :param date_string: a date string in format "YYYY-mm-dd"
    :return: True if date is less than x years ago; False otherwise.
    """

    now = datetime.datetime.now()
    x_years_ago = now.replace(year=now.year - x)
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

    return (date - x_years_ago).total_seconds() < 0


def decide(input_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains
        cases to decide
    :param countries_file: The name of a JSON formatted file that contains
        country data, such as whether an entry or transit visa is required,
        and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are:
        "Accept", "Reject", and "Quarantine"
    """
    # Prepend root folder where json files can be found to all file paths
    # json_file_root = "test_jsons/"
    # input_file = json_file_root + input_file
    # countries_file = json_file_root + input_file

    immigration_statuses = []
    with open(input_file, "r") as input_file_obj, open(countries_file) as countries_file_obj:
        input_file_json = json.load(input_file_obj)
        countries_file_json = json.load(countries_file_obj)

        for citizen_record in input_file_json:
            # Default immigration status is 'Accept'. This should change if any verification fails
            immigration_status = IMMIGRATION_ACCEPT

            is_records_complete = verify_record_complete(citizen_record)
            if not is_records_complete:
                immigration_statuses.append(IMMIGRATION_REJECT)

                # If rejected, no need to process further. Continue to next applicant
                continue

            is_passport_number_valid = valid_passport_format(citizen_record["passport"])
            if not is_passport_number_valid:
                immigration_statuses.append(IMMIGRATION_REJECT)

                # If rejected, no need to process further. Continue to next applicant
                continue

            is_birth_date_valid = valid_date_format(citizen_record["birth_date"])
            if not is_birth_date_valid:
                immigration_statuses.append(IMMIGRATION_REJECT)

                 # If rejected, no need to process further. Continue to next applicant
                continue

            citizen_home = citizen_record["home"]
            citizen_home_country = citizen_home["country"]

            # If traveller is from "KAN", directly accept
            if citizen_home_country == "KAN":
                immigration_status = IMMIGRATION_ACCEPT

            # Not a citizen, check visiting credentials
            else:
                is_valid_location = valid_location(citizen_home_country, countries_file_json)
                if not is_valid_location:
                    immigration_statuses.append(IMMIGRATION_REJECT)

                    # If rejected, no need to process further. Continue to next applicant
                    continue

                # Check if visitor visa required. If so, check if visa is valid
                citizen_entry_reason = citizen_record["entry_reason"]
                if citizen_entry_reason == "visit":
                    visitor_country = countries_file_json[citizen_home_country]
                    if visitor_country["visitor_visa_required"] == '1':
                        visa = get_visa(citizen_record)
                        if not is_visa_valid(visa):
                            immigration_statuses.append(IMMIGRATION_REJECT)
                            # If rejected, no need to process further. Continue to next applicant
                            continue

                elif citizen_entry_reason == "transit":
                    visitor_country = countries_file_json[citizen_home_country]
                    if visitor_country["transit_visa_required"] == '1':
                        visa = get_visa(citizen_record)
                        if not is_visa_valid(visa):
                            immigration_statuses.append(IMMIGRATION_REJECT)

                            # If rejected, no need to process further. Continue to next applicant
                            continue
                else:
                    # Entry reason is invalid. Reject application
                    immigration_statuses.append(IMMIGRATION_REJECT)

                    # If rejected, no need to process further. Continue to next applicant
                    continue

            # Check for quarantine, regardless if citizen or visitor
            is_quarantine = is_quarantine_reqd(citizen_record, countries_file_json)
            if is_quarantine:
                immigration_status = IMMIGRATION_QUARANTINE

            immigration_statuses.append(immigration_status)

    return immigration_statuses

def verify_record_complete(citizen_record):
    """
    Checks whether all fields in an entry record are filled in
    :param citizen_record: The record of a citizen who is being checked
    :return: Boolean True if record is filled in, False if otherwise
    """
    is_valid_record = True
    for required_field in REQUIRED_FIELDS:
        try:
            if len(citizen_record[required_field]) <= 0:
                is_valid_record = False
                break
        except:
            is_valid_record = False
            break

    return is_valid_record




def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    match = passport_matcher.match(passport_number)
    if match is not None and len(match.group()) > 0:
        return True
    else:
        return False


def valid_visa_format(visa_code):
    """
    Checks whether a visa code is two groups of five alphanumeric characters
    :param visa_code: alphanumeric string
    :return: Boolean; True if the format is valid, False otherwise

    """

    match = visa_matcher.match(visa_code)
    if match is not None and len(match.group()) > 0:
        return True
    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    match = date_matcher.match(date_string)
    if match is not None and len(match.group()) > 0:
        return True
    else:
        return False

def valid_location(location, countries):
    """
    Checks if location is present in list of countries provided
    :param location: location being verified
    :param countries: list of valid countries
    :return: Boolean True if location is present in countries, False otherwise
    """
    try:
        if countries[location] is not None:
            return True
        else:
            return False
    except:
        return False




def get_visa(citizen_record):
    """
    Returns visa object from citizen record. If no visa object found, returns None
    :param citizen_record: record of citizen
    :return: Returns visa object from citizen record. If no visa object found, returns None
    """
    try:
        return citizen_record["visa"]
    except:
        return None